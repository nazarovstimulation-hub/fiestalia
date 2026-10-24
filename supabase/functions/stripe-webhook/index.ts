// Fiestalia · Webhook de Stripe → activa el plan del álbum tras el pago.
//
// Despliegue:
//   supabase functions deploy stripe-webhook --no-verify-jwt
//   supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_... STRIPE_SECRET_KEY=sk_live_...
// En Stripe: Developers → Webhooks → Add endpoint →
//   URL: https://<proyecto>.functions.supabase.co/stripe-webhook
//   Evento: checkout.session.completed
// En cada Payment Link (Stripe → Payment Links → editar → After payment):
//   redirigir a https://fiestalia.com/app/panel.html?a={CHECKOUT_SESSION_ID}&paid=1
//   (la app ignora ese valor y usa client_reference_id; ver nota al final)
// El plan se identifica por el metadato "plan" del Payment Link (basico | celebracion | gran-evento)
// o, si falta, por el importe pagado.

import Stripe from "https://esm.sh/stripe@16.12.0?target=deno";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const stripe = new Stripe(Deno.env.get("STRIPE_SECRET_KEY")!, { apiVersion: "2024-06-20" });
const supabase = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

// Debe coincidir con BRAND.plans de site/brand.js
const PLANS: Record<string, { limit: number; months: number; cents: number }> = {
  "basico":      { limit: 500,  months: 6,  cents: 1900 },
  "celebracion": { limit: 1500, months: 12, cents: 3900 },
  "gran-evento": { limit: 5000, months: 24, cents: 6900 },
};

Deno.serve(async (req) => {
  const sig = req.headers.get("stripe-signature");
  const body = await req.text();
  let event: Stripe.Event;
  try {
    event = await stripe.webhooks.constructEventAsync(body, sig!, Deno.env.get("STRIPE_WEBHOOK_SECRET")!);
  } catch (e) {
    return new Response(`Firma no válida: ${(e as Error).message}`, { status: 400 });
  }

  if (event.type === "checkout.session.completed") {
    const s = event.data.object as Stripe.Checkout.Session;
    if (s.payment_status !== "paid") return new Response("ok (no pagado)", { status: 200 });
    const code = s.client_reference_id;
    if (!code) return new Response("sin client_reference_id", { status: 200 });

    let planId = (s.metadata?.plan as string) || "";
    if (!PLANS[planId]) {
      const paid = s.amount_total ?? 0;
      planId = Object.keys(PLANS).find((k) => PLANS[k].cents === paid) || "";
    }
    const plan = PLANS[planId];
    if (!plan) return new Response(`plan desconocido para ${s.amount_total}`, { status: 200 });

    const { error } = await supabase.rpc("album_set_plan", {
      p_code: code, p_plan: planId, p_limit: plan.limit, p_months: plan.months, p_session: s.id,
    });
    if (error) return new Response(`error BD: ${error.message}`, { status: 500 });
  }
  return new Response("ok", { status: 200 });
});

// Nota sobre la redirección tras el pago: Stripe no permite insertar client_reference_id en la
// URL de retorno, así que el panel usa el enlace guardado en el navegador (localStorage) o el que
// el organizador tenga a mano; la activación la hace este webhook, no la redirección.
