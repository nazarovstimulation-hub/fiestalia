/*
 * Configuración del backend de Fiestalia.
 *
 * Sin rellenar → MODO DEMO: los álbumes y las fotos se guardan solo en el
 * navegador (IndexedDB). Sirve para probar el flujo completo sin servidor.
 *
 * Con Supabase → producción: álbumes en Postgres, fotos en Storage (región UE).
 *   1. Crea un proyecto en https://supabase.com (región: Frankfurt / eu-central-1).
 *   2. Ejecuta supabase/schema.sql en el editor SQL del proyecto.
 *   3. Copia aquí Project URL y la clave "anon public" (Settings → API).
 *
 * Pagos → Stripe Payment Links (Stripe Dashboard → Payment Links). Un enlace por
 * plan. El webhook supabase/functions/stripe-webhook marca el álbum como pagado.
 */
window.FIESTALIA_CONFIG = {
  supabaseUrl: "https://nffaughndygvzkrvkamq.supabase.co",
  supabaseAnonKey: "sb_publishable_eFgK8soBjxFI0AqxusAe1g_g-kztvjL",  // clave pública (publishable)
  storageBucket: "media",
  stripeLinks: {          // URL del Payment Link de cada plan (vacío = demo)
    basico: "",
    celebracion: "",
    "gran-evento": ""
  },
  // Límites de subida por archivo (MB)
  maxImageMB: 25,
  maxVideoMB: 200,
  // Lado mayor de la miniatura generada en el navegador (px)
  thumbSize: 480
};
