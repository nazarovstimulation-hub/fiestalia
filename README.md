# Fiestalia.com — álbum QR para bodas y eventos

Landing page estática (HTML + CSS + JS, sin dependencias) de un servicio de álbum de fotos por código QR para bodas y eventos: los invitados escanean, suben fotos y vídeos sin app, con búsqueda por selfie, pantalla en directo (Live Wall) y descarga en ZIP.

## Estructura

```
site/
  index.html   # página completa en español
  styles.css   # estilos (tokens de color en :root)
  app.js       # calculador de planes, mockups animados, menú, FAQ
  brand.js     # ← nombre de marca, contacto, precios y planes
  assets/      # logo.png, mark.png, favicon.png, apple-touch-icon.png
docs/
  analisis-mercado-es.md   # análisis del mercado español y competidores (en ruso)
```

## Personalizar la marca

Edita `site/brand.js`: nombre, eslogan, dominio, correo, WhatsApp, ciudad, fotos gratis y la lista de planes (precio, fotos, GB, meses, Live Wall). Toda la página se actualiza sola. El tema de color se elige con `theme` en `site/brand.js` (por defecto `burdeos`: burdeos, champán y oro; también `fiesta`, `oro`, `noche`, `rosa`, `negro`, `esmeralda`, `medianoche`). Para previsualizar otro sin cambiar el archivo: `index.html?theme=oro`. Los tokens de cada tema están al final de `site/styles.css`.

## Ver en local

```bash
cd site && python3 -m http.server 8000
# abre http://localhost:8000
```

## Publicar

El sitio se publica solo en GitHub Pages con el workflow `.github/workflows/pages.yml`: cada push a `main` que toque `site/` despliega la carpeta `site/`. El workflow activa Pages automáticamente en el primer despliegue; si fallara por permisos, actívalo a mano en Settings → Pages → Build and deployment → Source: **GitHub Actions** y relanza el workflow. También puede lanzarse a mano desde la pestaña Actions (Run workflow). La URL queda en `https://nazarovstimulation-hub.github.io/fiestalia/` hasta que se conecte el dominio fiestalia.com (Settings → Pages → Custom domain).

## Pendiente antes de lanzar

- Conectar los botones «Crear álbum» / «Elegir plan» al backend o a la pasarela de pago.
- Sustituir las opiniones de ejemplo por testimonios reales.
- Redactar aviso legal, política de privacidad (incluida la base jurídica del reconocimiento facial, RGPD art. 9) y cookies; hoy son enlaces vacíos.

## La app (álbum, subida por QR, galería, panel, Live Wall)

```
site/app/
  crear.html    # crear álbum → QR + enlace de invitados + enlace privado del panel
  album.html    # vista de invitado: nombre, subida de fotos/vídeos, galería en tiempo real
  panel.html    # panel del organizador: estadísticas, QR, moderación, ZIP, ajustes, plan y pago
  live.html     # Live Wall a pantalla completa para el proyector del salón
  config.js     # ← conexión con Supabase y enlaces de pago de Stripe
  js/store.js   # capa de datos: IndexedDB (demo) o Supabase (producción)
  js/ui.js      # QR, miniaturas, lightbox, toasts
supabase/
  schema.sql                       # tablas, RLS, funciones, bucket "media"
  functions/stripe-webhook/        # activa el plan al completarse el pago
```

**Modo demo.** Sin configurar `config.js`, todo funciona guardando los datos en el navegador (IndexedDB): sirve para probar el flujo completo, pero los álbumes no se ven desde otros móviles.

**Producción.**
1. Crea un proyecto en [Supabase](https://supabase.com) (región Frankfurt), ejecuta `supabase/schema.sql` en el SQL Editor y activa Realtime para la tabla `photos`.
2. Copia Project URL y la clave `anon` en `site/app/config.js`.
3. En Stripe crea un Payment Link por plan (19 €, 39 €, 69 €) con el metadato `plan` = `basico` | `celebracion` | `gran-evento`; pega las URL en `config.js`.
4. Despliega el webhook: `supabase functions deploy stripe-webhook --no-verify-jwt` y configura en Stripe el evento `checkout.session.completed`.

Pendiente para después del MVP: búsqueda por selfie (requiere evaluación de impacto y proveedor de reconocimiento facial en la UE), correos transaccionales (enlace del panel, aviso de caducidad), limpieza automática de Storage.
