# -*- coding: utf-8 -*-
"""Genera las páginas públicas de Fiestalia (eventos, profesionales, sobre nosotros, contacto)
a partir de una plantilla común. Salida: site/*.html"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import SITE_URL

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")

HEAD = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{site}{file}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{site}{file}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{site}assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Fiestalia">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{site}assets/og-image.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
  <link rel="stylesheet" href="pages.css">
  <link rel="icon" type="image/png" href="assets/favicon.png">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  {jsonld}
</head>
<body>
"""

NAV_LINKS = [("index.html#como-funciona", "Cómo funciona"), ("precios.html", "Precios"), ("bodas.html", "Bodas"), ("profesionales.html", "Profesionales"), ("faq.html", "Preguntas")]

def header(active=""):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV_LINKS)
    return f"""<header class="header">
  <div class="container nav" id="nav">
    <a class="logo" href="index.html" aria-label="Fiestalia, inicio"><img src="assets/logo.png" alt="Fiestalia.com" width="900" height="169" class="logo-img"></a>
    <nav class="nav-links" aria-label="Principal">{links}</nav>
    <div class="nav-cta">
      <a class="btn btn-ghost btn-sm" href="contacto.html">Contacto</a>
      <a class="btn btn-primary btn-sm" href="app/crear.html">Crear álbum gratis</a>
      <button class="nav-toggle" id="navToggle" aria-label="Abrir menú" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-grid footer-grid-5">
      <div>
        <a class="logo logo-footer" href="index.html" aria-label="Fiestalia, inicio"><img src="assets/logo.png" alt="Fiestalia.com" width="900" height="169" class="logo-img"></a>
        <p style="margin-top:14px;max-width:320px" data-brand-tagline>El álbum de tu evento, hecho por tus invitados.</p>
        <p class="muted" style="margin-top:10px;font-size:14px" data-brand-city>Alcobendas, Madrid, España</p>
      </div>
      <div>
        <h4>Producto</h4>
        <ul>
          <li><a href="index.html#como-funciona">Cómo funciona</a></li>
          <li><a href="index.html#funciones">Funciones</a></li>
          <li><a href="index.html#demo">Live Wall</a></li>
          <li><a href="precios.html">Precios</a></li>
          <li><a href="demo.html">Álbum de ejemplo</a></li>
          <li><a href="guia-invitados.html">Guía para invitados</a></li>
          <li><a href="guia-organizadores.html">Guía para organizadores</a></li>
          <li><a href="blog/index.html">Blog</a></li>
        </ul>
      </div>
      <div>
        <h4>Para</h4>
        <ul>
          <li><a href="bodas.html">Bodas</a></li>
          <li><a href="cumpleanos.html">Cumpleaños</a></li>
          <li><a href="comuniones.html">Comuniones y bautizos</a></li>
          <li><a href="quinceaneras.html">Quinceañeras</a></li>
          <li><a href="empresas.html">Eventos de empresa</a></li>
          <li><a href="profesionales.html">Profesionales</a></li>
        </ul>
      </div>
      <div>
        <h4>Empresa</h4>
        <ul>
          <li><a href="sobre-nosotros.html">Sobre nosotros</a></li>
          <li><a href="contacto.html">Contacto</a></li>
          <li><a data-brand-email href="mailto:exp.span.group@gmail.com">exp.span.group@gmail.com</a></li>
          <li><a data-brand-whatsapp href="#">WhatsApp</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>
          <li><a href="legal/aviso-legal.html">Aviso legal</a></li>
          <li><a href="legal/privacidad.html">Política de privacidad</a></li>
          <li><a href="legal/cookies.html">Política de cookies</a></li>
          <li><a href="legal/condiciones.html">Condiciones de uso</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span id="year"></span> <span data-brand>Fiestalia</span> · SYNTH MASHI, S.L. Todos los derechos reservados.</span>
      <span>Hecho con cariño en España 🇪🇸</span>
    </div>
  </div>
</footer>
<script src="brand.js"></script>
<script src="pages.js"></script>
</body>
</html>
"""

CHECK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>'

def faq_html(items, open_first=True):
    out = ['<div class="faq">']
    for i, (q, a) in enumerate(items):
        out.append(f'<details{" open" if (i == 0 and open_first) else ""}><summary>{q}</summary><p>{a}</p></details>')
    out.append("</div>")
    return "\n".join(out)

def faq_jsonld(items):
    import json
    return '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in items]
    }, ensure_ascii=False) + "</script>"

def cta_block(title, text, btn="Crear mi álbum gratis", href="app/crear.html"):
    return f"""<section class="section">
  <div class="container"><div class="cta"><h2>{title}</h2><p>{text}</p><a class="btn btn-light btn-lg" href="{href}">{btn}</a></div></div>
</section>
"""

OTHER_EVENTS = [("bodas.html", "💍", "Bodas"), ("cumpleanos.html", "🎂", "Cumpleaños"), ("comuniones.html", "🕊️", "Comuniones y bautizos"), ("quinceaneras.html", "👑", "Quinceañeras"), ("empresas.html", "🏢", "Eventos de empresa")]

def others_block(current):
    cards = "".join(f'<a class="event" href="{h}"><div class="emoji">{e}</div><h3>{t}</h3></a>' for h, e, t in OTHER_EVENTS if h != current)
    return f"""<section class="section-tight">
  <div class="container"><div class="center"><span class="eyebrow">También para</span><h2 class="h2">Otras celebraciones</h2></div><div class="events events-4">{cards}</div></div>
</section>
"""

# ───────────────────────────── Páginas de eventos ─────────────────────────────
def event_page(p):
    benefits = "".join(f'<article class="feature"><div class="icon">{ic}</div><h3>{t}</h3><p>{d}</p></article>' for ic, t, d in p["benefits"])
    steps = "".join(f'<article class="step"><h3>{t}</h3><p>{d}</p></article>' for t, d in p["steps"])
    ideas = "".join(f'<li>{CHECK}<span>{i}</span></li>' for i in p["ideas"])
    stats = "".join(f'<div class="hero-stat"><b>{n}</b><span>{l}</span></div>' for n, l in p["stats"])
    plan = p["plan"]
    body = HEAD.format(site=SITE_URL, title=p["title"], desc=p["desc"], file=p["file"], jsonld=faq_jsonld(p["faq"])) + header(p["file"] if p["file"] == "bodas.html" else "") + f"""
<main id="top">
<section class="hero hero-page">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">{p['eyebrow']}</span>
      <h1 style="margin-top:16px">{p['h1']}</h1>
      <p class="lead">{p['lead']}</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="app/crear.html">Crear mi álbum gratis</a>
        <a class="btn btn-ghost btn-lg" href="#como">Ver cómo funciona</a>
      </div>
      <ul class="hero-note">
        <li>{CHECK} <span>Las primeras <b>50</b> fotos gratis</span></li>
        <li>{CHECK} Sin app ni registro</li>
        <li>{CHECK} Pago único</li>
      </ul>
    </div>
    <div class="hero-visual">
      <div class="hero-emoji">{p['emoji']}</div>
      <div class="hero-stats">{stats}</div>
      <p class="hero-visual-note">{p['visual_note']}</p>
    </div>
  </div>
</section>

<section class="section features-bg">
  <div class="container">
    <div class="center"><span class="eyebrow">Por qué</span><h2 class="h2">{p['why_title']}</h2><p class="lead">{p['why_lead']}</p></div>
    <div class="features">{benefits}</div>
  </div>
</section>

<section class="section" id="como">
  <div class="container">
    <div class="center"><span class="eyebrow">Cómo funciona</span><h2 class="h2">{p['how_title']}</h2></div>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section-tight">
  <div class="container ideas-grid">
    <div><span class="eyebrow">Ideas</span><h2 class="h2">{p['ideas_title']}</h2><p class="lead">{p['ideas_lead']}</p></div>
    <ul class="ideas">{ideas}</ul>
  </div>
</section>

<section class="section pricing-bg">
  <div class="container narrow-text center">
    <span class="eyebrow">Plan recomendado</span>
    <h2 class="h2">{plan['title']}</h2>
    <p class="lead">{plan['text']}</p>
    <div class="plan-callout">
      <div><b>{plan['name']}</b><span>{plan['detail']}</span></div>
      <div class="plan-callout-price">{plan['price']}</div>
      <a class="btn btn-primary" href="app/crear.html?plan={plan['id']}">Elegir {plan['name']}</a>
    </div>
    <p class="muted" style="margin-top:14px;font-size:14px">Pago único con IVA incluido. Empiezas gratis y amplías solo si lo necesitas. <a href="precios.html">Ver todos los planes</a>.</p>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="center"><span class="eyebrow">Preguntas frecuentes</span><h2 class="h2">{p['faq_title']}</h2></div>
    {faq_html(p['faq'])}
  </div>
</section>

{cta_block(p['cta_title'], p['cta_text'])}
{others_block(p['file'])}
</main>
""" + FOOTER
    return body

EVENTS = [
dict(file="bodas.html", emoji="💍", eyebrow="Álbum QR para bodas",
     title="Álbum de fotos QR para bodas: todas las fotos de tus invitados — Fiestalia",
     desc="Recoge todas las fotos y vídeos de tu boda con un código QR. Tus invitados suben desde el móvil sin app. Galería privada, Live Wall y descarga en ZIP. 50 fotos gratis.",
     h1="Todas las fotos de tu boda, <em>también las que no hace el fotógrafo</em>",
     lead="El fotógrafo no puede estar en todas partes. Tus invitados sí. Pon un código QR en las mesas y recoge sus fotos y vídeos en un álbum privado, sin que nadie instale nada ni te los pase por WhatsApp.",
     stats=[("1.200+", "fotos en una boda de 120 invitados"), ("0", "apps que instalar"), ("2 min", "para crear el álbum")],
     visual_note="Cifra orientativa: unas 10 fotos por invitado durante la celebración.",
     why_title="Lo que te pierdes sin un álbum compartido",
     why_lead="La mitad de los mejores momentos de una boda están en los móviles de los invitados. La mayoría no te llegan nunca.",
     benefits=[("📱", "Sin app, sin excusas", "Hasta tu tía abuela sabe escanear un QR con la cámara. Se abre el álbum y sube las fotos en dos toques. Con las apps de boda, la mitad de los invitados no las instala."),
               ("📸", "Calidad original", "WhatsApp comprime las fotos y los vídeos. Aquí llegan tal cual salieron del móvil, listas para imprimir o para el álbum físico."),
               ("🔒", "Privado de verdad", "Solo quien tiene el QR o el enlace entra. Nada de grupos con 80 números de teléfono ni enlaces públicos de Google."),
               ("📺", "Live Wall en el banquete", "Las fotos aparecen en la pantalla del salón según se suben. Los invitados se ven, se ríen y siguen haciendo fotos."),
               ("🤳", "Búsqueda por selfie", "Cada invitado encuentra sus fotos con una selfie, sin repasar mil imágenes. Función opcional, con consentimiento, próximamente."),
               ("⬇️", "Todo en un ZIP", "Al día siguiente descargas el álbum entero en calidad original. Para el fotógrafo, para el vídeo, para los abuelos.")],
     how_title="De la invitación a la tornaboda",
     steps=[("Crea el álbum", "Nombre de la boda, fecha y un mensaje para los invitados. Tienes tu QR en dos minutos."),
            ("Imprime el QR", "Descarga las tarjetas listas para imprimir. Ponlas en las mesas, en el photocall, en el seating plan o en la invitación."),
            ("El maestro de ceremonias lo anuncia", "Una frase basta: «escanead el QR de la mesa y subid vuestras fotos». Si tienes pantalla, activa el Live Wall."),
            ("Descarga y comparte", "A la mañana siguiente, descarga todo en ZIP o deja el álbum abierto para que los invitados sigan subiendo y viendo durante meses.")],
     ideas_title="Dónde poner el QR para que funcione",
     ideas_lead="Lo que mejor nos cuentan las parejas que ya lo han usado.",
     ideas=["Una tarjeta QR en cada mesa, junto al menú o al número de mesa.",
            "Un cartel grande en el photocall o la entrada del banquete.",
            "El QR en la invitación digital o en la web de la boda, para las fotos de la preboda.",
            "Que el DJ o el maestro de ceremonias lo anuncie después del primer baile, cuando todo el mundo tiene el móvil en la mano.",
            "El Live Wall en la pantalla del salón: el mejor incentivo para que la gente suba fotos.",
            "Un último recordatorio en el autobús de vuelta o al día siguiente por WhatsApp con el enlace."],
     plan=dict(id="celebracion", name="Celebración", title="Para una boda de 50 a 150 invitados", text="El plan que eligen la mayoría de las parejas. Suficiente para toda la celebración, con Live Wall incluido y el álbum disponible un año para revivirlo en el aniversario.", detail="1.500 fotos y vídeos · 20 GB · Live Wall · 12 meses", price="39 €"),
     faq_title="Lo que preguntan las parejas",
     faq=[("¿Mis invitados tienen que instalar algo?", "No. Escanean el QR con la cámara del móvil, se abre el álbum en el navegador y ya pueden subir fotos y vídeos. Solo les pedimos un nombre para saber quién subió cada foto."),
          ("¿Y si tengo más de 150 invitados?", "El plan Gran evento llega a 5.000 fotos. Y no hay límite de invitados en ningún plan: pagas por volumen de fotos, no por personas. Puedes ampliar incluso durante la boda."),
          ("¿Puedo ver las fotos antes de que las vean todos?", "Sí. Activa la moderación previa y cada foto nueva queda oculta hasta que la apruebes desde el panel. Útil si prefieres filtrar."),
          ("¿Cuánto tiempo se guarda el álbum?", "Según el plan, de 1 a 24 meses. Te avisamos por correo antes de que caduque para que descargues el ZIP o lo amplíes."),
          ("¿Sustituye al fotógrafo?", "No, lo complementa. El fotógrafo hace las fotos buenas; los invitados hacen las espontáneas, las de su mesa, las del final de la noche. Las dos cosas juntas son la boda completa."),
          ("¿Es legal recoger las fotos de los invitados?", "Sí, siempre que les informes de que el evento se fotografía y se comparte en un álbum privado. Te damos un texto modelo para la tarjeta QR. Más detalles en nuestra <a href='legal/privacidad.html'>política de privacidad</a>.")],
     cta_title="Que no se pierda ni una foto de vuestra boda", cta_text="Crea el álbum ahora, imprime el QR y olvídate del resto. Las primeras 50 fotos son gratis."),

dict(file="cumpleanos.html", emoji="🎂", eyebrow="Álbum QR para cumpleaños",
     title="Álbum de fotos QR para cumpleaños y fiestas — Fiestalia",
     desc="Recoge las fotos y vídeos de tu cumpleaños o fiesta con un código QR. Los invitados suben desde el móvil sin app. Álbum privado, Live Wall y descarga en ZIP. Gratis hasta 50 fotos.",
     h1="Las fotos de tu fiesta, <em>sin perseguir a nadie al día siguiente</em>",
     lead="Un 40, un 50, un 18, el primer cumpleaños del peque o una fiesta sorpresa. Pon el QR en la mesa de la tarta y recoge todas las fotos y vídeos de los invitados en un solo sitio.",
     stats=[("300+", "fotos en una fiesta de 30 personas"), ("0", "grupos de WhatsApp"), ("Gratis", "hasta 50 fotos")],
     visual_note="Ideal para cumpleaños redondos, fiestas sorpresa y celebraciones familiares.",
     why_title="Mejor que el grupo de WhatsApp",
     why_lead="El grupo se llena de «¿me pasas las fotos?» y las que llegan vienen comprimidas y sin orden.",
     benefits=[("🎉", "Fiesta sorpresa a prueba de filtraciones", "Comparte el QR solo con los invitados el día de la fiesta. El homenajeado descubre el álbum entero al final: sus caras de sorpresa incluidas."),
               ("👶", "Primer cumpleaños, todas las miradas", "Todos fotografían al peque. Con el álbum, todas esas fotos acaban en el mismo sitio y en calidad original para el álbum de recuerdos."),
               ("🎥", "Vídeos sin comprimir", "El cumpleaños feliz, el soplo de velas, el discurso. Llegan en la calidad en que se grabaron, no en la papilla de WhatsApp."),
               ("📺", "Live Wall en la tele del salón", "Conecta el móvil o el portátil a la tele y las fotos van apareciendo según se suben. Funciona en cualquier casa, bar o local."),
               ("🔒", "Privado", "Solo quien tiene el QR entra. Nada se publica en redes salvo que alguien lo quiera."),
               ("⬇️", "Descarga todo de una vez", "Al día siguiente, un clic y tienes el ZIP con todo. Para el homenajeado, para los abuelos, para el vídeo-resumen.")],
     how_title="Tres pasos y a soplar las velas",
     steps=[("Crea el álbum", "Nombre, fecha y un mensaje. Gratis hasta 50 fotos; amplía si la fiesta se anima."),
            ("Pon el QR donde se vea", "En la mesa de la tarta, en la barra, pegado en la nevera. Descarga la tarjeta e imprímela, o enséñalo desde tu móvil."),
            ("Anúncialo", "«Las fotos, al QR». Con el Live Wall en la tele no hará falta repetirlo."),
            ("Descarga y comparte", "Todas las fotos en ZIP y el álbum abierto para que los invitados lo sigan viendo.")],
     ideas_title="Ideas que funcionan en una fiesta",
     ideas_lead="Pequeños trucos para que el álbum se llene solo.",
     ideas=["El QR impreso en las servilletas o en una tarjeta junto a la tarta.",
            "Un reto: «la foto más fea con el cumpleañero». Los invitados se motivan y el álbum se llena.",
            "Live Wall en la tele del salón durante toda la fiesta.",
            "Para una sorpresa: envía el QR por WhatsApp a los invitados la mañana de la fiesta, nunca antes.",
            "Al día siguiente, comparte el enlace para que suban lo que grabaron de madrugada."],
     plan=dict(id="basico", name="Básico", title="Para fiestas de hasta 40 personas", text="Para un cumpleaños en casa o en un local, el plan Básico sobra. Si vienen más de 40 personas o quieres el Live Wall en la tele, el plan Celebración es el tuyo.", detail="500 fotos y vídeos · 5 GB · 6 meses", price="19 €"),
     faq_title="Preguntas sobre fiestas y cumpleaños",
     faq=[("¿Sirve para una fiesta pequeña, de 10 personas?", "Sí, y gratis: el plan gratuito incluye 50 fotos. Si se queda corto, amplías en un clic, incluso durante la fiesta."),
          ("¿Se puede usar en un bar o restaurante?", "Claro. Solo necesitas el QR impreso o en tu móvil. Para el Live Wall, cualquier tele con un navegador o un portátil conectado con HDMI."),
          ("¿Pueden subir vídeos largos?", "Sí. El tamaño máximo por vídeo depende del plan; en el Básico hasta 200 MB por archivo, suficiente para varios minutos en calidad móvil."),
          ("¿Puedo hacer que el homenajeado no vea el álbum hasta el final?", "Sí: simplemente no le des el QR hasta que quieras. Es un enlace privado, no aparece en ningún sitio."),
          ("¿Y para una fiesta infantil con muchos niños?", "Funciona igual, pero recuerda que son los padres quienes suben y que debes informarles de que las fotos se comparten en un álbum privado. Puedes activar la moderación previa para revisar antes de publicar.")],
     cta_title="Una fiesta, un álbum, cero persecuciones", cta_text="Crea el álbum en dos minutos y pon el QR junto a la tarta. Gratis hasta 50 fotos."),

dict(file="comuniones.html", emoji="🕊️", eyebrow="Álbum QR para comuniones y bautizos",
     title="Álbum de fotos QR para comuniones y bautizos — Fiestalia",
     desc="Recoge las fotos de la comunión o el bautizo de toda la familia con un código QR. Sin app, álbum privado, calidad original y descarga en ZIP. Gratis hasta 50 fotos.",
     h1="La comunión entera, <em>con las fotos de toda la familia</em>",
     lead="Abuelos, tíos, padrinos, los amigos del cole. Todos hacen fotos y ninguna llega. Pon el QR en la mesa del restaurante y recógelas todas en un álbum privado y ordenado.",
     stats=[("4", "generaciones subiendo a la vez"), ("0", "apps que explicar a los abuelos"), ("1 ZIP", "con todo al día siguiente")],
     visual_note="Pensado para celebraciones familiares: comuniones, bautizos, confirmaciones.",
     why_title="Hecho para celebraciones familiares",
     why_lead="En una comunión las fotos buenas están repartidas entre veinte móviles de tres generaciones distintas.",
     benefits=[("👵", "Tan fácil que lo usan los abuelos", "Cámara, QR, subir. Sin cuentas, sin contraseñas, sin descargar nada. Si saben hacer una foto, saben subirla."),
               ("⛪", "De la iglesia al restaurante", "Un solo álbum para la ceremonia, el reportaje en el jardín y el banquete. Las fotos se ordenan solas por hora."),
               ("📖", "Calidad para el álbum impreso", "Las fotos llegan en resolución original, perfectas para el álbum físico o el fotolibro de la comunión."),
               ("🔒", "Solo la familia", "Álbum privado, sin redes sociales. Nadie ajeno a la celebración ve las fotos de los niños."),
               ("✅", "Moderación si la quieres", "Activa la aprobación previa y decide tú qué fotos ven los demás, útil cuando hay muchos niños."),
               ("⬇️", "Reparte sin esfuerzo", "Comparte el enlace del álbum con la familia que no pudo venir, o descárgalo todo en ZIP para enviarlo.")],
     how_title="Un álbum para toda la familia",
     steps=[("Crea el álbum", "El nombre del niño o la niña, la fecha, un mensaje cariñoso para la familia."),
            ("Imprime la tarjeta QR", "Una en cada mesa del restaurante y otra en el photocall o la mesa de regalos."),
            ("Que alguien lo anuncie", "Los padres, los padrinos o el restaurante: «subid las fotos al QR de la mesa»."),
            ("Guarda y reparte", "Descarga todo en ZIP para el álbum impreso y deja el enlace abierto para la familia.")],
     ideas_title="Consejos para comuniones y bautizos",
     ideas_lead="Para que no falte ninguna foto importante.",
     ideas=["Pon el QR también en el recordatorio o la estampita de la comunión.",
            "Pide a los padrinos que suban primero: cuando alguien empieza, los demás siguen.",
            "Haz una tarjeta QR grande para la mesa de los niños con un dibujo; suben fotos divertidísimas.",
            "Activa la moderación previa si prefieres revisar las fotos de los menores antes de publicarlas.",
            "Al terminar, manda el enlace del álbum a la familia que vive lejos."],
     plan=dict(id="basico", name="Básico", title="Para una comunión de 30 a 60 personas", text="Con 500 fotos y seis meses de álbum el plan Básico cubre la mayoría de las comuniones y bautizos. Si sois más de 60 o queréis el Live Wall en el restaurante, el plan Celebración.", detail="500 fotos y vídeos · 5 GB · 6 meses", price="19 €"),
     faq_title="Preguntas frecuentes en comuniones",
     faq=[("¿Pueden usarlo los abuelos sin ayuda?", "Sí. Es la pregunta que más nos hacen y la respuesta es que sí: escanear un QR con la cámara es algo que ya hacen en los restaurantes. El álbum se abre solo y el botón de subir es grande y claro."),
          ("¿Hay que informar a los otros padres?", "Sí, basta con una frase en la invitación o en la tarjeta QR: «las fotos se comparten en un álbum privado de la familia». Te damos un texto modelo. Si algún padre prefiere que su hijo no aparezca, puedes ocultar esas fotos desde el panel."),
          ("¿Cómo lo uso para el fotolibro?", "Descarga el ZIP completo en calidad original y súbelo al servicio de impresión que uses. Las fotos de los invitados complementan las del fotógrafo."),
          ("¿Puedo juntar la ceremonia y el banquete en un álbum?", "Sí, es lo habitual. Las fotos se ordenan por hora, así que la iglesia aparece antes que el banquete."),
          ("¿Cuánto cuesta?", "Gratis hasta 50 fotos. Para una comunión completa, el plan Básico cuesta 19 € una sola vez, sin suscripción.")],
     cta_title="Las fotos de la comunión, todas en un sitio", cta_text="Crea el álbum, imprime el QR para las mesas y deja que la familia haga el resto."),

dict(file="quinceaneras.html", emoji="👑", eyebrow="Álbum QR para quinceañeras",
     title="Álbum de fotos QR para fiestas de quince años — Fiestalia",
     desc="Recoge todas las fotos y vídeos de la fiesta de quince años con un código QR. Los invitados suben desde el celular sin app. Álbum privado, pantalla en vivo y descarga completa.",
     h1="Los quince de tu hija, <em>en las fotos de todos sus invitados</em>",
     lead="El vals, la entrada, el cambio de zapatillas, la hora loca. Cada invitado graba algo distinto. Con el QR en las mesas, todo acaba en el mismo álbum, en calidad original y sin que nadie instale nada.",
     stats=[("100%", "de los invitados con celular"), ("0", "apps que descargar"), ("Live", "en la pantalla del salón")],
     visual_note="Funciona igual en España y en Latinoamérica: solo hace falta un navegador.",
     why_title="Una fiesta hecha para las fotos",
     why_lead="Los quince son el evento con más fotos por invitado que existe. Que no se queden en cien celulares distintos.",
     benefits=[("📱", "Los adolescentes lo entienden al instante", "Escanear, subir, listo. Y los adultos también: no hay nada que instalar ni cuentas que crear."),
               ("📺", "Pantalla en vivo durante la fiesta", "Las fotos aparecen en la pantalla del salón según se suben. Nadie se resiste a verse en grande: el álbum se llena solo."),
               ("🎬", "Vídeos del vals y la hora loca", "Los vídeos llegan sin comprimir, listos para el vídeo-resumen que verá toda la familia."),
               ("🔒", "Privado y bajo control", "Solo entra quien tiene el QR. Y con la moderación previa, los padres deciden qué se publica."),
               ("🤳", "Búsqueda por selfie", "Cada invitado encuentra sus fotos con una selfie, sin repasar todo el álbum. Opcional y con consentimiento, próximamente."),
               ("⬇️", "Todo para la quinceañera", "Al día siguiente descarga el ZIP con todo. El mejor regalo: la fiesta entera vista por sus amigos.")],
     how_title="Del ensayo a la última canción",
     steps=[("Crea el álbum", "El nombre de la quinceañera, la fecha y un mensaje para los invitados."),
            ("Imprime el QR", "Tarjetas en las mesas, un cartel en la entrada y el QR en la invitación digital."),
            ("Que el DJ lo anuncie", "Después del vals, con todo el mundo con el celular en la mano. Activa la pantalla en vivo."),
            ("Descarga y revive", "Todo el álbum en ZIP y el enlace abierto para que los invitados lo sigan viendo durante meses.")],
     ideas_title="Ideas para unos quince inolvidables",
     ideas_lead="Lo que mejor funciona en estas fiestas.",
     ideas=["Un reto fotográfico por mesa: la mesa con más fotos subidas gana algo en la hora loca.",
            "La pantalla en vivo en grande, junto a la pista: es el momento en que todos empiezan a subir.",
            "El QR en la invitación digital para recoger también las fotos de la sesión previa y el ensayo.",
            "Un cartel con el QR en el photocall.",
            "Moderación previa activada si los padres quieren revisar antes de publicar."],
     plan=dict(id="celebracion", name="Celebración", title="Para una fiesta de 80 a 150 invitados", text="Las fiestas de quince suelen ser grandes y con muchos vídeos. El plan Celebración incluye la pantalla en vivo y 20 GB para los vídeos de toda la noche.", detail="1.500 fotos y vídeos · 20 GB · Live Wall · 12 meses", price="39 €"),
     faq_title="Preguntas sobre fiestas de quince",
     faq=[("¿Funciona fuera de España?", "Sí. Solo hace falta un navegador y conexión a internet. Los precios se muestran en euros; el pago con tarjeta funciona desde cualquier país."),
          ("¿Cómo pongo la pantalla en vivo en el salón?", "Abre el enlace del Live Wall en un portátil o un reproductor conectado al proyector o la pantalla del salón. Es una página web a pantalla completa, no hay que instalar nada."),
          ("¿Pueden los padres controlar lo que se publica?", "Sí. Con la moderación previa, cada foto queda oculta hasta que la aprobéis desde el panel. También podéis cerrar las subidas cuando queráis."),
          ("¿Hay límite de invitados?", "No. Pagas por volumen de fotos, no por personas. Si el álbum se llena, amplías el plan en un clic, incluso durante la fiesta."),
          ("¿Los invitados menores pueden subir fotos?", "Sí, los adolescentes son quienes más suben. Pedimos solo un nombre o apodo, sin datos personales. La búsqueda por selfie no está disponible para menores de 14 años.")],
     cta_title="Que los quince queden en un solo álbum", cta_text="Crea el álbum hoy, imprime el QR y deja que los invitados llenen la fiesta de fotos."),

dict(file="empresas.html", emoji="🏢", eyebrow="Álbum QR para eventos de empresa",
     title="Álbum de fotos QR para eventos de empresa, cenas y congresos — Fiestalia",
     desc="Recoge las fotos de tu evento corporativo con un código QR: cena de Navidad, team building, convención o congreso. Sin app, galería privada, Live Wall y descarga completa para comunicación interna.",
     h1="Las fotos del evento de empresa, <em>sin pedirlas por correo a 200 personas</em>",
     lead="Cena de Navidad, team building, convención anual, congreso. Pon el QR en las mesas y en la pantalla y recoge en un solo álbum lo que graban los asistentes. Para comunicación interna, redes y el recuerdo del equipo.",
     stats=[("200+", "asistentes sin límite de personas"), ("0", "apps que aprobar con IT"), ("ZIP", "para comunicación interna")],
     visual_note="Álbum privado con enlace único: solo los asistentes acceden.",
     why_title="Pensado para organizadores de eventos",
     why_lead="Lo que necesita el equipo de comunicación y lo que agradecen los asistentes.",
     benefits=[("🖥️", "Live Wall en la pantalla principal", "Las fotos de los asistentes aparecen en directo en la pantalla del evento. Rompe el hielo en la cena y da vida a los descansos del congreso."),
               ("🛡️", "Sin instalar apps corporativas", "Nada que aprobar con sistemas ni que instalar en móviles de empresa. Un navegador basta. Datos alojados en la Unión Europea."),
               ("✅", "Moderación antes de publicar", "El equipo de comunicación aprueba cada foto antes de que se vea en el álbum o en la pantalla. Cero sorpresas."),
               ("🏷️", "Tu marca en el álbum", "Nombre del evento, mensaje de bienvenida y, para profesionales, tarjetas QR con vuestro logo."),
               ("⬇️", "Material para comunicación interna", "Descarga todo en ZIP en calidad original para la intranet, la newsletter o LinkedIn, con la atribución de quién hizo cada foto."),
               ("📊", "Un álbum por evento", "Crea un álbum por cada evento del año. Los asistentes solo ven el suyo.")],
     how_title="Montaje en cinco minutos",
     steps=[("Crea el álbum", "Nombre del evento, fecha y un mensaje de bienvenida. Activa la moderación si queréis revisar antes de publicar."),
            ("QR en mesas y pantallas", "Descarga las tarjetas y el QR en alta resolución para la presentación, los roll-ups y las mesas."),
            ("Anuncio desde el escenario", "El presentador invita a subir fotos al QR. El Live Wall en la pantalla hace el resto."),
            ("Descarga y publica", "Al terminar, ZIP completo para comunicación interna y el enlace del álbum para los asistentes.")],
     ideas_title="Ideas para eventos corporativos",
     ideas_lead="Probadas en cenas de empresa, convenciones y ferias.",
     ideas=["Reto por equipos o departamentos: el que más fotos sube, gana algo en la cena.",
            "El QR en la primera y la última diapositiva de la presentación.",
            "Live Wall durante el cóctel y los descansos del congreso.",
            "Moderación previa activada: comunicación aprueba antes de que nada aparezca en pantalla.",
            "Cierra las subidas al terminar el evento y comparte el álbum con todos los asistentes por correo.",
            "Para ferias: un álbum por stand o por día, con su propio QR."],
     plan=dict(id="gran-evento", name="Gran evento", title="Para eventos de 150 a 500 asistentes", text="Para convenciones, cenas de empresa grandes y congresos: 5.000 fotos, 60 GB para los vídeos y el álbum disponible dos años. Para eventos más pequeños, el plan Celebración es suficiente.", detail="5.000 fotos y vídeos · 60 GB · Live Wall · 24 meses", price="69 €"),
     faq_title="Preguntas de empresas y organizadores",
     faq=[("¿Emitís factura a nombre de la empresa?", "Sí. Al contratar un plan de pago se emite factura con los datos fiscales que indiques. Para varios eventos al año, consulta los packs para <a href='profesionales.html'>profesionales y empresas</a>."),
          ("¿Dónde se alojan las fotos?", "En servidores dentro de la Unión Europea, cifradas y accesibles solo con el enlace del álbum. Cumplimos el RGPD; consulta la <a href='legal/privacidad.html'>política de privacidad</a>."),
          ("¿Podemos revisar las fotos antes de que se publiquen?", "Sí, con la moderación previa. Cada foto queda oculta hasta que alguien del equipo la apruebe en el panel. Varias personas pueden compartir el enlace del panel."),
          ("¿Necesitamos aprobar algo con el departamento de IT?", "No. Los asistentes usan el navegador de su móvil; no hay app ni cuentas. El Live Wall es una página web a pantalla completa en cualquier portátil o reproductor."),
          ("¿Podemos usar nuestro logo?", "El álbum lleva el nombre de vuestro evento y vuestro mensaje. Las tarjetas QR y la pantalla con vuestro logo están disponibles en los packs para profesionales y empresas."),
          ("¿Cuántos eventos podemos hacer?", "Los que queráis: cada álbum es independiente y se paga una sola vez. Para más de cinco eventos al año, los packs profesionales salen más a cuenta.")],
     cta_title="Vuestro próximo evento, con las fotos de todos", cta_text="Crea el álbum, pon el QR en la pantalla y recoge el material para comunicación sin pedírselo a nadie."),
]

# ───────────────────────────── Profesionales ─────────────────────────────
def profesionales_page():
    faq = [("¿Cómo funcionan los packs?", "Compras un número de álbumes por adelantado a precio reducido y los vas creando cuando los necesitas, sin caducidad del pack. Cada álbum tiene las características del plan Celebración o Gran evento, según el pack."),
           ("¿Puedo poner mi logo?", "Sí. En los packs profesionales las tarjetas QR, la pantalla del Live Wall y el álbum pueden llevar tu logo y tus colores en lugar de los nuestros, o junto a ellos."),
           ("¿Mis clientes tienen que pagar algo?", "No. Tú incluyes el álbum en tu servicio y les entregas el QR. Ellos solo ven tu marca y, si quieres, la nuestra como proveedor tecnológico."),
           ("¿Las fotos de los invitados son mías?", "Las fotos son de quien las hace. Como profesional, puedes descargar el álbum completo con la autorización del cliente para el reportaje o el vídeo. Las condiciones de uso regulan la licencia en detalle."),
           ("¿Emitís factura?", "Sí, con tus datos fiscales, por cada pack. Somos SYNTH MASHI, S.L., NIF B05675947, con sede en Alcobendas (Madrid)."),
           ("¿Hay API o integración?", "Todavía no. Si necesitas crear álbumes automáticamente desde tu CRM o tu web, cuéntanoslo: estamos definiendo la hoja de ruta con los primeros profesionales.")]
    packs = [("Pack 5", "5 álbumes Celebración", "145 €", "29 € por álbum", ["1.500 fotos y Live Wall por álbum", "Tarjetas QR con tu logo", "Sin caducidad del pack"]),
             ("Pack 10", "10 álbumes Celebración", "250 €", "25 € por álbum", ["Todo lo del Pack 5", "Pantalla Live Wall con tu logo", "Soporte prioritario por WhatsApp"], True),
             ("Pack 25", "25 álbumes a elegir", "500 €", "20 € por álbum", ["Celebración o Gran evento", "Marca blanca completa", "Panel con todos tus eventos", "Factura única anual"])]
    packs_html = "".join(f"""<article class="plan{' featured' if len(p) > 5 else ''}">{'<span class="plan-badge">Más elegido</span>' if len(p) > 5 else ''}
      <h3>{p[0]}</h3><p class="guests">{p[1]}</p><div class="price"><b>{p[2]}</b></div><p class="guests">{p[3]}</p>
      <ul>{''.join(f'<li>{CHECK}<span>{x}</span></li>' for x in p[4])}</ul><div class="plan-spacer"></div>
      <a class="btn {'btn-primary' if len(p) > 5 else 'btn-ghost'}" href="contacto.html?asunto=pack&pack={p[0].replace(' ', '')}">Solicitar {p[0]}</a></article>""" for p in packs)
    segs = [("💐", "Wedding planners", "Incluye el álbum QR en tu servicio y entrega a cada pareja algo que recordarán: todas las fotos de sus invitados, con tu marca. Un extra que se vende solo."),
            ("📷", "Fotógrafos y videógrafos", "Complementa tu reportaje con las fotos espontáneas de los invitados y usa el material para el vídeo. Más valor para el cliente, sin trabajo extra para ti."),
            ("🏛️", "Salones, fincas y restaurantes", "Ofrece el Live Wall en tu pantalla como parte del banquete. Cada evento genera cientos de fotos de tu espacio, hechas por los propios clientes."),
            ("🎤", "DJ y maestros de ceremonias", "Anuncia el QR, enciende el Live Wall y mira cómo la pista se anima. Añádelo a tu tarifa como servicio premium."),
            ("🏢", "Agencias de eventos", "Un álbum por evento, moderación previa para comunicación y descarga completa para el cliente. Factura única por pack."),
            ("🎪", "Organizadores de fiestas y festivales", "Para fiestas grandes, graduaciones o festivales: recoge el contenido del público y proyéctalo en directo.")]
    segs_html = "".join(f'<article class="feature"><div class="icon">{i}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in segs)
    body = HEAD.format(site=SITE_URL, title="Fiestalia para profesionales: wedding planners, fotógrafos, salones y agencias", desc="Packs de álbumes QR con tu marca para wedding planners, fotógrafos, salones de bodas y agencias de eventos. Desde 20 € por álbum, sin caducidad, con Live Wall y soporte prioritario.", file="profesionales.html", jsonld=faq_jsonld(faq)) + header("profesionales.html") + f"""
<main id="top">
<section class="hero hero-page">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">Para profesionales</span>
      <h1 style="margin-top:16px">El álbum QR como parte de tu servicio, <em>con tu marca</em></h1>
      <p class="lead">Wedding planners, fotógrafos, salones y agencias: ofrece a tus clientes el álbum de fotos de sus invitados y el Live Wall en la pantalla, con tu logo y a precio de pack. Nosotros ponemos la tecnología; tú te llevas el mérito.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="#packs">Ver packs</a>
        <a class="btn btn-ghost btn-lg" href="contacto.html?asunto=profesional">Hablar con nosotros</a>
      </div>
      <ul class="hero-note">
        <li>{CHECK} Desde 20 € por álbum</li>
        <li>{CHECK} Tarjetas QR y Live Wall con tu logo</li>
        <li>{CHECK} Packs sin caducidad</li>
      </ul>
    </div>
    <div class="hero-visual">
      <div class="hero-emoji">🤝</div>
      <div class="hero-stats"><div class="hero-stat"><b>+1</b><span>servicio que vender sin coste operativo</span></div><div class="hero-stat"><b>0</b><span>trabajo extra el día del evento</span></div><div class="hero-stat"><b>100%</b><span>de las fotos de los invitados para el cliente</span></div></div>
      <p class="hero-visual-note">Prueba gratis con tu primer evento: el plan gratuito está disponible para todos.</p>
    </div>
  </div>
</section>

<section class="section features-bg">
  <div class="container">
    <div class="center"><span class="eyebrow">Para quién</span><h2 class="h2">Un extra que tus clientes recuerdan</h2><p class="lead">Cada perfil lo usa de una forma distinta. Todos tienen algo en común: el cliente se va con todas las fotos de su evento.</p></div>
    <div class="features">{segs_html}</div>
  </div>
</section>

<section class="section" id="como">
  <div class="container">
    <div class="center"><span class="eyebrow">Cómo funciona</span><h2 class="h2">Tú entregas el QR, nosotros el resto</h2></div>
    <div class="steps">
      <article class="step"><h3>Eliges un pack</h3><p>Compras 5, 10 o 25 álbumes por adelantado a precio reducido. Factura a tu nombre.</p></article>
      <article class="step"><h3>Creas el álbum de cada evento</h3><p>Dos minutos por evento, con tu logo en las tarjetas QR y en el Live Wall. Los packs no caducan.</p></article>
      <article class="step"><h3>Entregas el QR al cliente</h3><p>Tarjetas impresas, el QR para la invitación y el enlace del Live Wall para el salón.</p></article>
      <article class="step"><h3>El cliente se lleva todo</h3><p>Panel propio para descargar el ZIP y gestionar el álbum. Tú puedes descargar también para el reportaje o el vídeo.</p></article>
    </div>
  </div>
</section>

<section class="section pricing-bg" id="packs">
  <div class="container">
    <div class="center"><span class="eyebrow">Packs</span><h2 class="h2">Precios para profesionales</h2><p class="lead">Pago único por pack, IVA incluido, sin suscripción ni caducidad. Los álbumes se crean cuando los necesitas.</p></div>
    <div class="plans plans-3">{packs_html}</div>
    <p class="pricing-foot">¿Más de 25 eventos al año o necesidades especiales (marca blanca total, dominio propio, integración)? <a href="contacto.html?asunto=profesional">Escríbenos</a> y preparamos una propuesta.</p>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="center"><span class="eyebrow">Preguntas frecuentes</span><h2 class="h2">Lo que preguntan los profesionales</h2></div>
    {faq_html(faq)}
  </div>
</section>

{cta_block("Prueba con tu próximo evento", "Crea un álbum gratuito, pruébalo con un cliente y, si te convence, elige tu pack.", "Crear álbum de prueba")}
</main>
""" + FOOTER
    return body

# ───────────────────────────── Sobre nosotros ─────────────────────────────
def sobre_page():
    values = [("🇪🇺", "Datos en Europa", "Las fotos de tus invitados se alojan en servidores de la Unión Europea, cifradas y accesibles solo con el enlace del álbum. Cumplimos el RGPD y la LOPDGDD, y lo explicamos con claridad en nuestra política de privacidad."),
              ("📱", "Sin app, por principio", "Creemos que pedir a un invitado que instale una aplicación para compartir una foto es pedir demasiado. Todo funciona en el navegador del móvil, en cualquier móvil."),
              ("💶", "Pago único, sin letra pequeña", "Un evento es un evento. Pagas una vez por el álbum y ya está: sin suscripciones, sin renovaciones automáticas, sin sorpresas."),
              ("🤝", "Cerca", "Somos una empresa pequeña de Madrid. Nos escribes y te responde una persona, en español, normalmente el mismo día.")]
    values_html = "".join(f'<article class="feature"><div class="icon">{i}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in values)
    body = HEAD.format(site=SITE_URL, title="Sobre nosotros — Fiestalia", desc="Fiestalia es un servicio español de álbumes de fotos QR para bodas y eventos, creado por SYNTH MASHI, S.L. en Madrid. Datos en Europa, sin app, pago único.", file="sobre-nosotros.html", jsonld="") + header() + f"""
<main id="top">
<section class="hero hero-page hero-compact">
  <div class="container narrow-text">
    <span class="eyebrow">Sobre nosotros</span>
    <h1 style="margin-top:16px">Nacimos en una boda, <em>buscando las fotos</em></h1>
    <p class="lead">Después de una boda de 120 invitados recibimos 14 fotos por WhatsApp. Catorce. Sabíamos que había cientos más en los móviles de todos, pero nunca llegaron. Fiestalia existe para que eso no vuelva a pasar en ningún evento.</p>
  </div>
</section>

<section class="section features-bg">
  <div class="container">
    <div class="center"><span class="eyebrow">Qué hacemos</span><h2 class="h2">Un álbum compartido que de verdad se llena</h2><p class="lead">Un código QR en las mesas, un álbum privado en el navegador y la pantalla del salón mostrando las fotos en directo. Sin apps, sin registros, sin grupos de WhatsApp. Tan sencillo que lo usan los abuelos, y tan completo que lo usan las agencias de eventos.</p></div>
    <div class="features features-4">{values_html}</div>
  </div>
</section>

<section class="section">
  <div class="container about-grid">
    <div>
      <span class="eyebrow">La empresa</span>
      <h2 class="h2">SYNTH MASHI, S.L.</h2>
      <p class="lead">Fiestalia es una marca de SYNTH MASHI, S.L., sociedad española con sede en Alcobendas, Madrid. Desarrollamos el producto desde España, para el mercado español y latinoamericano, con la privacidad de los invitados como punto de partida y no como añadido.</p>
      <div class="actions"><a class="btn btn-primary" href="contacto.html">Contactar</a><a class="btn btn-ghost" href="profesionales.html">Para profesionales</a></div>
    </div>
    <div class="card-plain">
      <h3>Datos de la empresa</h3>
      <dl class="dl">
        <dt>Razón social</dt><dd>SYNTH MASHI, S.L.</dd>
        <dt>NIF</dt><dd>B05675947</dd>
        <dt>Domicilio</dt><dd>Travesía Huesca, 8, Piso 0, Puerta 3<br>28100 Alcobendas, Madrid, España</dd>
        <dt>Registro</dt><dd>Registro Mercantil de Madrid, hoja M-898556</dd>
        <dt>Correo</dt><dd><a href="mailto:exp.span.group@gmail.com">exp.span.group@gmail.com</a></dd>
        <dt>Teléfono</dt><dd><a href="tel:+34634118579">+34 634 118 579</a></dd>
      </dl>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container narrow-text center">
    <span class="eyebrow">Hoja de ruta</span>
    <h2 class="h2">En qué estamos trabajando</h2>
    <ul class="roadmap">
      <li><b>Búsqueda por selfie.</b> Cada invitado encuentra sus fotos con una selfie. La función está diseñada; antes de activarla completamos la evaluación de impacto exigida por el RGPD para datos biométricos.</li>
      <li><b>Avisos por correo.</b> Enlace del panel al crear el álbum y recordatorio antes de que caduque.</li>
      <li><b>Retos fotográficos.</b> Misiones para los invitados: «el primer baile», «la mesa de los primos», «la foto más fea con el novio».</li>
      <li><b>Packs y marca blanca</b> para wedding planners, fotógrafos y salones.</li>
    </ul>
    <p class="muted" style="margin-top:18px">¿Echas algo en falta? <a href="contacto.html?asunto=sugerencia">Cuéntanoslo</a>: las primeras funciones las decidimos con nuestros primeros clientes.</p>
  </div>
</section>

{cta_block("Pruébalo en tu próximo evento", "Las primeras 50 fotos son gratis. Sin tarjeta, sin registro.")}
</main>
""" + FOOTER
    return body

# ───────────────────────────── Contacto ─────────────────────────────
def contacto_page():
    body = HEAD.format(site=SITE_URL, title="Contacto — Fiestalia", desc="Escríbenos por WhatsApp o correo. Respondemos en español, normalmente el mismo día. SYNTH MASHI, S.L., Alcobendas, Madrid.", file="contacto.html", jsonld="") + header() + f"""
<main id="top">
<section class="hero hero-page hero-compact">
  <div class="container narrow-text">
    <span class="eyebrow">Contacto</span>
    <h1 style="margin-top:16px">Hablamos cuando quieras, <em>en español</em></h1>
    <p class="lead">Dudas sobre un álbum, un evento grande, un pack para profesionales o una sugerencia. Te responde una persona, normalmente el mismo día laborable.</p>
  </div>
</section>

<section class="section-tight">
  <div class="container contact-grid">
    <div class="card-plain">
      <h3>Escríbenos</h3>
      <form id="contactForm" novalidate>
        <div class="field"><label for="cName">Tu nombre *</label><input id="cName" required maxlength="80" autocomplete="name"></div>
        <div class="field"><label for="cEmail">Tu correo *</label><input id="cEmail" type="email" required autocomplete="email"></div>
        <div class="field"><label for="cSubject">Asunto</label>
          <select id="cSubject">
            <option value="duda">Tengo una duda sobre el servicio</option>
            <option value="evento">Quiero usarlo en mi evento</option>
            <option value="profesional">Soy profesional (planner, fotógrafo, salón, agencia)</option>
            <option value="pack">Quiero un pack para profesionales</option>
            <option value="empresa">Evento de empresa / factura</option>
            <option value="privacidad">Protección de datos / eliminar fotos</option>
            <option value="sugerencia">Sugerencia o problema técnico</option>
          </select></div>
        <div class="field"><label for="cMsg">Mensaje *</label><textarea id="cMsg" required maxlength="2000" rows="6" placeholder="Cuéntanos qué necesitas: fecha del evento, número de invitados, lo que te preocupa…"></textarea></div>
        <label class="check"><input type="checkbox" id="cAccept" required> <span>He leído la <a href="legal/privacidad.html" target="_blank">política de privacidad</a>. Usaremos tus datos solo para responderte. *</span></label>
        <div class="actions">
          <button class="btn btn-primary" type="submit">Enviar por correo</button>
          <button class="btn btn-ghost" type="button" id="sendWa">Enviar por WhatsApp</button>
        </div>
        <p class="muted" style="margin-top:12px;font-size:13px">El botón de correo abre tu aplicación de correo con el mensaje preparado. El de WhatsApp abre un chat con nosotros con el texto listo para enviar.</p>
      </form>
    </div>
    <div>
      <div class="contact-card">
        <h3>WhatsApp</h3>
        <p>La forma más rápida. Lunes a viernes de 9 a 19 h, y durante los fines de semana de evento.</p>
        <a class="btn btn-primary" href="https://wa.me/34634118579?text=Hola%2C%20tengo%20una%20consulta%20sobre%20Fiestalia" target="_blank" rel="noopener">+34 634 118 579</a>
      </div>
      <div class="contact-card">
        <h3>Correo electrónico</h3>
        <p>Para presupuestos, facturas y protección de datos.</p>
        <a class="btn btn-ghost" href="mailto:exp.span.group@gmail.com">exp.span.group@gmail.com</a>
      </div>
      <div class="contact-card">
        <h3>Dirección</h3>
        <p>SYNTH MASHI, S.L.<br>Travesía Huesca, 8, Piso 0, Puerta 3<br>28100 Alcobendas, Madrid, España<br><span class="muted">NIF B05675947</span></p>
      </div>
      <div class="contact-card">
        <h3>¿Eres invitado y buscas un álbum?</h3>
        <p>Pide el enlace o el QR a quien organiza el evento. Nosotros no podemos darte acceso a un álbum privado.</p>
      </div>
    </div>
  </div>
</section>
</main>
""" + FOOTER
    return body

PAGES_CSS = """/* Páginas públicas (eventos, profesionales, sobre nosotros, contacto) */
.nav-links a.active { color: var(--brand); }
.hero-page { padding: 64px 0 56px; }
.hero-page h1 { font-family: var(--font-display); font-size: clamp(34px, 4.8vw, 56px); font-weight: 700; letter-spacing: 0; }
.hero-page h1 em { font-style: italic; color: var(--brand); }
.hero-compact { padding: 56px 0 24px; }
.hero-compact h1 { font-size: clamp(32px, 4.4vw, 50px); }
.narrow-text { max-width: 760px; margin-inline: auto; }
.hero-visual { background: var(--card); border: 1px solid var(--line); border-radius: 28px; padding: 32px; box-shadow: var(--shadow-lg); text-align: center; }
.hero-emoji { font-size: 72px; line-height: 1; }
.hero-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 24px; }
.hero-stat { background: var(--bg); border: 1px solid var(--line); border-radius: 14px; padding: 14px 10px; }
.hero-stat b { display: block; font-family: var(--font-display); font-size: 26px; color: var(--brand); }
.hero-stat span { font-size: 12px; color: var(--ink-3); display: block; margin-top: 4px; line-height: 1.3; }
.hero-visual-note { margin-top: 18px; font-size: 13px; color: var(--ink-3); }
.ideas-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 48px; align-items: start; }
.ideas { display: grid; gap: 12px; margin-top: 8px; }
.ideas li { display: flex; gap: 12px; align-items: flex-start; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius-sm); padding: 14px 16px; color: var(--ink-2); }
.ideas li svg { flex: none; color: var(--accent); margin-top: 3px; }
.plan-callout { display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap; background: var(--card); border: 1.5px solid var(--accent); border-radius: var(--radius); padding: 22px 26px; margin-top: 28px; text-align: left; }
.plan-callout b { display: block; font-size: 20px; }
.plan-callout span { color: var(--ink-3); font-size: 14px; }
.plan-callout-price { font-family: var(--font-display); font-size: 40px; font-weight: 700; color: var(--brand); }
.events-4 { grid-template-columns: repeat(4, 1fr); }
.events .event { display: block; color: inherit; transition: transform .2s, box-shadow .2s; }
.events a.event:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.plans-3 { grid-template-columns: repeat(3, 1fr); max-width: 980px; margin-inline: auto; }
.features-4 { grid-template-columns: repeat(4, 1fr); }
.footer-grid-5 { grid-template-columns: 1.4fr 1fr 1fr 1fr 1fr; }
.about-grid { display: grid; grid-template-columns: 1.1fr .9fr; gap: 48px; align-items: start; }
.card-plain { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 28px; }
.card-plain h3 { font-size: 20px; font-weight: 800; margin-bottom: 14px; }
.dl { display: grid; grid-template-columns: auto 1fr; gap: 10px 18px; font-size: 15px; color: var(--ink-2); }
.dl dt { font-weight: 800; color: var(--ink); }
.dl dd { margin: 0; }
.dl a { color: var(--brand); font-weight: 700; }
.roadmap { text-align: left; display: grid; gap: 12px; margin-top: 24px; }
.roadmap li { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius-sm); padding: 14px 18px; color: var(--ink-2); }
.roadmap b { color: var(--ink); }
.actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px; }
.contact-grid { display: grid; grid-template-columns: 1.2fr .8fr; gap: 28px; align-items: start; }
.contact-card { background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 22px 24px; }
.contact-card + .contact-card { margin-top: 14px; }
.contact-card h3 { font-size: 17px; font-weight: 800; }
.contact-card p { color: var(--ink-2); margin: 8px 0 14px; font-size: 15px; }
.field { display: grid; gap: 6px; margin-top: 16px; }
.field label { font-weight: 800; font-size: 14px; }
.field input, .field select, .field textarea { font: inherit; padding: 12px 14px; border-radius: var(--radius-sm); border: 1.5px solid var(--line); background: var(--bg); color: var(--ink); width: 100%; }
.field input:focus, .field select:focus, .field textarea:focus { outline: none; border-color: var(--brand); box-shadow: 0 0 0 4px var(--brand-soft); }
.check { display: flex; gap: 12px; align-items: flex-start; margin-top: 16px; font-size: 14px; color: var(--ink-2); }
.check input { margin-top: 3px; accent-color: var(--brand); width: 18px; height: 18px; flex: none; }
.check a { color: var(--brand); font-weight: 700; }
@media (max-width: 1000px) { .features-4, .events-4 { grid-template-columns: repeat(2, 1fr); } .plans-3 { grid-template-columns: 1fr; max-width: 480px; } .footer-grid-5 { grid-template-columns: 1fr 1fr; } }
@media (max-width: 820px) { .ideas-grid, .about-grid, .contact-grid { grid-template-columns: 1fr; gap: 28px; } .hero-page { padding: 44px 0 40px; } .hero-visual { padding: 22px; } .hero-stats { grid-template-columns: repeat(3, 1fr); gap: 8px; } .hero-stat b { font-size: 20px; } }
@media (max-width: 560px) { .features-4 { grid-template-columns: 1fr; } .footer-grid-5 { grid-template-columns: 1fr; } .plan-callout { flex-direction: column; align-items: flex-start; } }
"""

PAGES_JS = """/* Páginas públicas: marca, tema, menú móvil, FAQ, formulario de contacto */
(function () {
  const B = window.BRAND || {};
  const theme = new URLSearchParams(location.search).get("theme") || B.theme;
  if (theme && theme !== "fiesta") document.documentElement.setAttribute("data-theme", theme);
  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = B.name));
  document.querySelectorAll("[data-brand-tagline]").forEach((el) => (el.textContent = B.tagline + "."));
  document.querySelectorAll("[data-brand-city]").forEach((el) => (el.textContent = B.city));
  document.querySelectorAll("[data-brand-email]").forEach((el) => { el.textContent = B.email; el.href = "mailto:" + B.email; });
  document.querySelectorAll("[data-brand-whatsapp]").forEach((el) => { el.textContent = "WhatsApp " + B.whatsapp; el.href = "https://wa.me/" + B.whatsapp.replace(/\\D/g, ""); });
  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();

  const nav = document.getElementById("nav"), toggle = document.getElementById("navToggle");
  if (toggle) toggle.addEventListener("click", () => { const open = nav.classList.toggle("open"); toggle.setAttribute("aria-expanded", String(open)); });

  const faqs = document.querySelectorAll(".faq details");
  faqs.forEach((d) => d.addEventListener("toggle", () => { if (d.open) faqs.forEach((o) => { if (o !== d) o.open = false; }); }));

  // Contacto: preselección por ?asunto= y envío por correo / WhatsApp
  const form = document.getElementById("contactForm");
  if (form) {
    const p = new URLSearchParams(location.search);
    const sel = document.getElementById("cSubject");
    if (p.get("asunto") && [...sel.options].some((o) => o.value === p.get("asunto"))) sel.value = p.get("asunto");
    if (p.get("pack")) document.getElementById("cMsg").value = `Me interesa el ${p.get("pack").replace("Pack", "Pack ")} para profesionales. `;
    const compose = () => {
      const name = document.getElementById("cName").value.trim(), email = document.getElementById("cEmail").value.trim(), msg = document.getElementById("cMsg").value.trim();
      if (!name || !email || !msg) { form.reportValidity(); return null; }
      if (!document.getElementById("cAccept").checked) { alert("Marca la casilla de la política de privacidad, por favor."); return null; }
      const subject = `[Fiestalia] ${sel.options[sel.selectedIndex].text}`;
      const body = `${msg}\\n\\n— ${name}\\n${email}`;
      return { subject, body };
    };
    form.addEventListener("submit", (e) => { e.preventDefault(); const c = compose(); if (!c) return; location.href = `mailto:${(B.legal && B.legal.email) || B.email}?subject=${encodeURIComponent(c.subject)}&body=${encodeURIComponent(c.body)}`; });
    document.getElementById("sendWa").addEventListener("click", () => { const c = compose(); if (!c) return; window.open(`https://wa.me/${B.whatsapp.replace(/\\D/g, "")}?text=${encodeURIComponent(c.subject + "\\n" + c.body)}`, "_blank", "noopener"); });
  }
})();
"""

def main():
    for p in EVENTS:
        open(os.path.join(OUT, p["file"]), "w", encoding="utf-8").write(event_page(p))
    open(os.path.join(OUT, "profesionales.html"), "w", encoding="utf-8").write(profesionales_page())
    open(os.path.join(OUT, "sobre-nosotros.html"), "w", encoding="utf-8").write(sobre_page())
    open(os.path.join(OUT, "contacto.html"), "w", encoding="utf-8").write(contacto_page())
    open(os.path.join(OUT, "pages.css"), "w", encoding="utf-8").write(PAGES_CSS)
    open(os.path.join(OUT, "pages.js"), "w", encoding="utf-8").write(PAGES_JS)
    print("generated", len(EVENTS) + 3, "pages")

if __name__ == "__main__":
    main()
