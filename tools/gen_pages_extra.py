# -*- coding: utf-8 -*-
"""Genera guías, álbum de ejemplo, 404 y blog. Reutiliza la plantilla de gen_pages.py.
Uso: python3 tools/gen_pages_extra.py"""
import os, re, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_pages import HEAD, header, FOOTER, CHECK, faq_html, faq_jsonld, cta_block, OUT, EVENTS
from site_config import SITE_URL

def rebase(html_str, prefix):
    """Convierte rutas locales (href/src) para páginas en subcarpetas (p. ej. blog/)."""
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:|tel:|#|data:|//|\./)', url) or url.startswith(prefix):
            return m.group(0)
        return f'{attr}="{prefix}{url}"'
    return re.sub(r'\b(href|src)="([^"]+)"', fix, html_str)

def page(file, title, desc, body, jsonld="", active="", prefix=""):
    html_str = HEAD.format(site=SITE_URL, title=title, desc=desc, file=file, jsonld=jsonld) + header(active) + body + FOOTER
    if prefix:
        html_str = rebase(html_str, prefix)
        html_str = html_str.replace(f'"{prefix}{SITE_URL}', f'"{SITE_URL}')
    return html_str

def write(path, content):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

# ───────────────────────────── Guía para invitados ─────────────────────────────
def guia_invitados():
    steps = [("📷", "Abre la cámara del móvil", "Apunta al código QR de la mesa o de la tarjeta, como si fueras a hacerle una foto. No hace falta ninguna aplicación especial: la cámara del iPhone y de cualquier Android ya lee códigos QR."),
             ("👆", "Toca el aviso que aparece", "En la pantalla saldrá un pequeño cartel con una dirección web. Tócalo y se abrirá el álbum en el navegador. Si no aparece, mantén la cámara quieta un segundo más."),
             ("✍️", "Escribe tu nombre", "Solo tu nombre o un apodo, para que los anfitriones sepan quién subió cada foto. No pedimos correo ni teléfono ni ninguna cuenta."),
             ("⬆️", "Pulsa «Subir fotos y vídeos»", "Es el botón grande de color. Se abre tu galería: elige una o varias fotos y confirma. Puedes repetirlo tantas veces como quieras durante el evento y los días siguientes."),
             ("👀", "Mira las fotos de los demás", "En el mismo álbum verás las fotos que suben los otros invitados. Toca una para verla en grande y descargarla.")]
    steps_html = "".join(f'<li class="guide-step"><div class="guide-icon">{i}</div><div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in steps)
    faq = [("No me sale nada al apuntar con la cámara", "Comprueba que el código QR está bien iluminado y entero en la pantalla. En algunos Android antiguos la lectura de QR está en la aplicación de Google Lens o en el buscador. Si no funciona, pide a quien organiza el evento que te mande el enlace por WhatsApp: funciona igual."),
           ("¿Tengo que instalar algo o crear una cuenta?", "No. Todo pasa en el navegador del móvil. Si alguna página te pide instalar una aplicación, no es la nuestra."),
           ("¿Quién ve mis fotos?", "Solo las personas que tienen el enlace o el QR del álbum: los anfitriones y los demás invitados. El álbum no se publica en ninguna red social ni en buscadores."),
           ("¿Puedo subir vídeos?", "Sí, el mismo botón sirve para fotos y vídeos. Si el vídeo es muy largo y tienes poca cobertura, espera a tener wifi."),
           ("He subido una foto por error", "Avisa a quien organiza el evento: desde su panel puede ocultarla o borrarla al momento."),
           ("¿Hasta cuándo puedo subir fotos?", "Normalmente durante el evento y las semanas siguientes, hasta que los anfitriones cierren el álbum. Si ves el aviso «Las subidas están cerradas», ya no se admiten fotos nuevas, pero puedes seguir viéndolas.")]
    body = f"""
<main id="top">
<section class="hero hero-page hero-compact">
  <div class="container narrow-text">
    <span class="eyebrow">Guía para invitados</span>
    <h1 style="margin-top:16px">Cómo subir tus fotos al álbum, <em>en cinco pasos</em></h1>
    <p class="lead">Te han dado un código QR o un enlace en una boda, un cumpleaños o una fiesta. Así se usa. No hay que instalar nada ni crear ninguna cuenta: tarda menos de un minuto.</p>
  </div>
</section>
<section class="section-tight">
  <div class="container narrow-text">
    <ol class="guide-steps">{steps_html}</ol>
    <div class="warn" style="margin-top:28px"><b>Consejo:</b> si tienes poca cobertura en el salón, sube las fotos más tarde desde casa. El enlace sigue funcionando y las fotos se ordenan por la hora en que se hicieron, no por la hora en que se suben.</div>
  </div>
</section>
<section class="section-tight">
  <div class="container">
    <div class="center"><span class="eyebrow">Problemas habituales</span><h2 class="h2">Si algo no funciona</h2></div>
    {faq_html(faq)}
  </div>
</section>
<section class="section-tight">
  <div class="container narrow-text center">
    <p class="lead">¿Organizas tú el evento? Lee la <a href="guia-organizadores.html">guía para organizadores</a> o <a href="app/crear.html">crea tu álbum gratis</a>.</p>
  </div>
</section>
</main>
"""
    return page("guia-invitados.html", "Cómo subir fotos al álbum QR: guía para invitados — Fiestalia", "Guía paso a paso para invitados: cómo escanear el código QR del evento y subir tus fotos y vídeos desde el móvil sin instalar nada.", body, faq_jsonld(faq))

# ───────────────────────────── Guía para organizadores ─────────────────────────────
def guia_organizadores():
    sections = [
        ("Antes del evento", [
            ("Crea el álbum con tiempo", "Hazlo la semana anterior. Pon el nombre del evento tal y como lo conocen los invitados («Boda de Lucía y Marcos», no «Evento 12/06») y un mensaje de bienvenida corto y cálido."),
            ("Decide si quieres moderación", "Con la moderación previa cada foto queda oculta hasta que la apruebes. Es útil en eventos con niños o de empresa. En una boda normal la mayoría la desactiva: la gracia es ver las fotos al momento."),
            ("Imprime las tarjetas QR", "Desde el panel, «Imprimir tarjetas QR» saca cuatro por hoja A4. Papel de 200 g o más para que se mantengan de pie. Para un cartel grande, descarga el QR en PNG y llévalo a cualquier copistería: con 1024 píxeles se imprime nítido hasta A2."),
            ("Mete el QR en la invitación", "El mismo código en la invitación digital o en la web de la boda recoge las fotos de la preboda y la despedida."),
            ("Guarda el enlace del panel", "Es tu llave: no lo compartas con los invitados. Guárdalo en el gestor de contraseñas o envíatelo por correo."),
        ]),
        ("Dónde colocar el QR", [
            ("Una tarjeta en cada mesa", "Junto al menú o al número de mesa. Es el sitio donde más se escanea: la gente se sienta, mira la mesa y tiene el móvil en la mano."),
            ("Un cartel en la entrada o el photocall", "Tamaño A3 o mayor, a la altura de los ojos. Añade una frase: «Escanea y sube tus fotos»."),
            ("En la barra y en los baños", "Suena raro, pero funciona: son los dos sitios donde todo el mundo mira el móvil."),
            ("En la pantalla", "Si tienes Live Wall, el QR ya aparece en la esquina de la pantalla todo el tiempo."),
        ]),
        ("Durante el evento", [
            ("Que alguien lo anuncie", "El maestro de ceremonias, el DJ o los propios anfitriones. Una frase después del primer baile o antes del primer plato: «Tenéis un QR en la mesa: subid ahí vuestras fotos y las veremos en la pantalla». Repítelo una vez a mitad de la fiesta."),
            ("Enciende el Live Wall", "Abre el enlace del Live Wall en el portátil conectado al proyector o en el navegador de la Smart TV y pulsa F11 para pantalla completa. Se actualiza solo."),
            ("Pide a dos o tres personas que empiecen", "Los padrinos, los testigos, los amigos de confianza. Cuando aparecen las primeras fotos en la pantalla, el resto se anima solo."),
            ("Vigila el límite", "El panel muestra cuántas fotos quedan en tu plan. Si se acerca al límite, amplía el plan desde el panel: las fotos en espera se publican automáticamente."),
        ]),
        ("Después del evento", [
            ("Manda un recordatorio al día siguiente", "Un mensaje al grupo de WhatsApp con el enlace del álbum: «Subid lo que grabasteis anoche». Llega otra oleada de fotos."),
            ("Descarga el ZIP", "Desde el panel, «Descargar todo». Guárdalo en dos sitios. Es tu copia maestra en calidad original."),
            ("Comparte el álbum", "Deja el enlace abierto para los invitados durante el tiempo que dure tu plan. Les encanta volver a verlo."),
            ("Antes de que caduque", "Te avisaremos por correo. Amplía el plan si quieres que siga disponible o asegúrate de tener el ZIP descargado."),
        ]),
    ]
    sec_html = ""
    for title, items in sections:
        li = "".join(f'<li>{CHECK}<div><b>{t}</b><p>{d}</p></div></li>' for t, d in items)
        sec_html += f'<section class="section-tight"><div class="container narrow-text"><h2 class="h2">{title}</h2><ul class="guide-list">{li}</ul></div></section>'
    live = """<section class="section livewall"><div class="container livewall-grid"><div><span class="eyebrow">Live Wall</span><h2 class="h2">Cómo conectar la pantalla del salón</h2><p class="lead">El Live Wall es una página web. Cualquier cosa con navegador y salida a la pantalla sirve.</p><ul class="checks">
<li>%s <b>Portátil + HDMI al proyector o la TV.</b> La opción más fiable. Abre el enlace del Live Wall en Chrome y pulsa F11.</li>
<li>%s <b>Smart TV.</b> Abre el navegador de la tele y escribe el enlace corto que te da el panel. Algunas teles no tienen navegador: usa un portátil o un Chromecast.</li>
<li>%s <b>Chromecast o Apple TV.</b> Abre el Live Wall en tu móvil o portátil y envía la pantalla a la tele.</li>
<li>%s <b>Pantalla LED del salón.</b> Pide al técnico del salón una entrada HDMI y conecta un portátil. Avísales el día antes.</li>
<li>%s <b>Wifi.</b> El Live Wall necesita conexión estable. Si el salón no tiene wifi, comparte datos desde un móvil con buena cobertura.</li>
</ul></div><div class="screen"><div class="screen-bar"><b>Boda de Lucía &amp; Marcos</b><span class="live"><i></i> EN DIRECTO</span></div><div class="wall"><div class="big" style="--c:#f2b5a0"></div><div style="--c:#e8c9a0"></div><div style="--c:#c9d6c3"></div><div style="--c:#b8c7dd"></div><div style="--c:#e4b7d1"></div><div class="big" style="--c:#f5d58a"></div><div style="--c:#a9c7c0"></div><div style="--c:#d9b3a3"></div><div style="--c:#c8bfe0"></div><div style="--c:#f0a287"></div><div style="--c:#bcd4a8"></div></div><div class="screen-foot">Escanea el QR de tu mesa y <b>aparece aquí</b></div></div></div></section>""" % ((CHECK,) * 5)
    body = f"""
<main id="top">
<section class="hero hero-page hero-compact">
  <div class="container narrow-text">
    <span class="eyebrow">Guía para organizadores</span>
    <h1 style="margin-top:16px">Cómo conseguir que el álbum <em>se llene solo</em></h1>
    <p class="lead">Crear el álbum son dos minutos. Que los invitados lo usen depende de cuatro cosas: dónde pones el QR, quién lo anuncia, si hay pantalla y si mandas un recordatorio al día siguiente. Esta guía lo resume.</p>
    <div class="hero-actions"><a class="btn btn-primary btn-lg" href="app/crear.html">Crear mi álbum gratis</a><a class="btn btn-ghost btn-lg" href="guia-invitados.html">Guía para invitados</a></div>
  </div>
</section>
{sec_html}
{live}
<section class="section-tight"><div class="container narrow-text">
  <h2 class="h2">Texto para informar a los invitados</h2>
  <p class="lead">Para la tarjeta QR, la invitación o el grupo de WhatsApp. Cumple con la obligación de informar de que el evento se fotografía y se comparte en un álbum privado.</p>
  <div class="card-plain" style="margin-top:18px"><p style="color:var(--ink-2);line-height:1.7">«Durante la celebración haremos fotos y vídeos y los compartiremos en un álbum privado al que solo acceden los invitados con este código QR. Si prefieres no aparecer, díselo a los novios y retiraremos tus fotos. Las imágenes se alojan en servidores de la Unión Europea y se eliminan al caducar el álbum.»</p></div>
</div></section>
{cta_block("Tu álbum, listo en dos minutos", "Crea el álbum, imprime las tarjetas y sigue esta guía el día del evento.")}
</main>
"""
    return page("guia-organizadores.html", "Guía para organizadores: dónde poner el QR, qué anunciar y cómo conectar el Live Wall — Fiestalia", "Consejos prácticos para que el álbum QR de tu evento se llene de fotos: dónde colocar el código, qué decir desde el micrófono, cómo conectar la pantalla y qué hacer después.", body)

# ───────────────────────────── Álbum de ejemplo ─────────────────────────────
def demo():
    caps = open(os.path.join(OUT, "assets/demo/captions.txt"), encoding="utf-8").read().splitlines()
    names = ["Ana", "Carlos", "Marta", "Jorge", "Lucía", "Pablo", "Elena", "Sergio", "Nuria", "David", "Irene", "Raúl"]
    tiles = "".join(f'<button class="ph" type="button" data-i="{i}"><img src="assets/demo/demo-{i+1:02d}_t.jpg" alt="{c}" loading="lazy"><span class="who">{names[i]} · {c}</span></button>' for i, c in enumerate(caps))
    data = json.dumps([{"src": f"assets/demo/demo-{i+1:02d}.jpg", "who": names[i], "cap": c} for i, c in enumerate(caps)], ensure_ascii=False)
    body = f"""
<main id="top">
<section class="hero hero-page hero-compact">
  <div class="container narrow-text center">
    <span class="eyebrow">Álbum de ejemplo</span>
    <h1 style="margin-top:16px">Boda de Lucía y Marcos</h1>
    <p class="lead">Así ve el álbum un invitado: las fotos de todos, ordenadas por hora, con el nombre de quien las subió. Toca una para verla en grande. Esta es una muestra con fotos de ejemplo; en tu álbum estarán las de tus invitados.</p>
    <p class="muted" style="font-size:14px">12 fotos · 8 invitados · 12 de junio de 2027</p>
  </div>
</section>
<section class="section-tight"><div class="container">
  <div class="grid demo-grid" id="demoGrid">{tiles}</div>
  <div class="upload-bar"><a class="btn btn-primary btn-lg" href="app/crear.html">Crear mi álbum gratis</a></div>
</div></section>
<section class="section-tight"><div class="container narrow-text center">
  <span class="eyebrow">Lo que no se ve en la muestra</span>
  <h2 class="h2">Y además</h2>
  <div class="features" style="text-align:left">
    <article class="feature"><div class="icon">📺</div><h3>Live Wall</h3><p>Las mismas fotos apareciendo en la pantalla del salón según se suben. <a href="guia-organizadores.html">Cómo conectarla</a>.</p></article>
    <article class="feature"><div class="icon">🛠️</div><h3>Panel del organizador</h3><p>Estadísticas, moderación, descarga en ZIP, tarjetas QR y cambio de plan desde una sola página.</p></article>
    <article class="feature"><div class="icon">⬆️</div><h3>Subida en dos toques</h3><p>Sin app ni registro, desde la cámara del móvil. <a href="guia-invitados.html">Guía para invitados</a>.</p></article>
  </div>
</div></section>
{cta_block("¿Te gusta cómo queda?", "Crea el tuyo en dos minutos. Las primeras 50 fotos son gratis.")}
</main>
<script>window.DEMO_PHOTOS = {data};</script>
"""
    return page("demo.html", "Álbum de ejemplo — Fiestalia", "Mira cómo queda un álbum QR de boda tal y como lo ven los invitados: galería, nombres y lightbox. Muestra con fotos de ejemplo.", body)

# ───────────────────────────── 404 ─────────────────────────────
def not_found():
    body = """
<main id="top">
<section class="hero hero-page" style="min-height:60vh;display:grid;align-items:center">
  <div class="container narrow-text center">
    <span class="eyebrow">Error 404</span>
    <h1 style="margin-top:16px">Esta página <em>no está en el álbum</em></h1>
    <p class="lead">El enlace no existe o ha cambiado. Si buscabas un álbum de un evento, pide el enlace o el QR a quien lo organiza: los álbumes son privados y no aparecen en ningún listado.</p>
    <div class="hero-actions" style="justify-content:center"><a class="btn btn-primary btn-lg" href="/fiestalia/index.html" data-home>Ir al inicio</a><a class="btn btn-ghost btn-lg" href="/fiestalia/contacto.html" data-contact>Contacto</a></div>
  </div>
</section>
</main>
<script>
// En GitHub Pages el sitio cuelga de /fiestalia/; con dominio propio, de la raíz.
(function(){ var base = location.pathname.indexOf('/fiestalia/') === 0 ? '/fiestalia/' : '/';
  document.querySelector('[data-home]').href = base + 'index.html'; document.querySelector('[data-contact]').href = base + 'contacto.html';
  document.querySelectorAll('a[href], link[href], script[src], img[src]').forEach(function(el){ var a = el.href !== undefined && el.tagName !== 'A' ? 'href' : (el.src !== undefined ? 'src' : 'href'); var v = el.getAttribute(a); if (v && !/^(https?:|mailto:|tel:|#|\\/|data:)/.test(v)) el.setAttribute(a, base + v); }); })();
</script>
"""
    return page("404.html", "Página no encontrada — Fiestalia", "La página que buscas no existe.", body)

# ───────────────────────────── Blog ─────────────────────────────
ARTICLES = [
dict(slug="como-recoger-las-fotos-de-tu-boda", date="2026-10-20", read="7 min",
     title="Cómo recoger todas las fotos de tu boda que hacen los invitados",
     desc="Seis formas de reunir las fotos que hacen tus invitados en la boda, de la más casera a la más cómoda, con lo bueno y lo malo de cada una.",
     h1="Cómo recoger todas las fotos de tu boda que hacen los invitados",
     intro="En una boda de 120 personas se hacen entre mil y dos mil fotos con el móvil. Al día siguiente, a la pareja le llegan veinte. El resto se queda en los móviles de los invitados y no se recupera nunca. Estas son las formas de evitarlo, ordenadas de la más artesanal a la más cómoda, con lo que funciona y lo que no de cada una.",
     sections=[
        ("1. Pedirlas por WhatsApp", "Es lo que hace casi todo el mundo y lo que peor funciona. Hay que escribir a cada persona, muchas no contestan, las fotos llegan comprimidas (WhatsApp reduce la calidad y recorta los vídeos) y acaban desperdigadas en veinte conversaciones. Sirve para cinco invitados, no para cien."),
        ("2. Un grupo de WhatsApp de la boda", "Mejor que escribir uno a uno, pero con los mismos problemas de calidad. Además, expone el número de teléfono de todos los invitados a todos los demás, y mucha gente no quiere estar en un grupo de ochenta desconocidos. Las fotos siguen comprimidas y no hay forma de descargarlas todas a la vez."),
        ("3. Una carpeta compartida de Google Drive o Google Fotos", "Soluciona la calidad: las fotos llegan en resolución original. Pero obliga a los invitados a tener cuenta de Google e iniciar sesión desde el móvil, cosa que en una boda frena a la mitad de la gente, sobre todo a los mayores. Y si abres la carpeta a «cualquiera con el enlace» para evitar el inicio de sesión, cualquiera con el enlace puede también borrar."),
        ("4. Cámaras desechables en las mesas", "Tienen encanto y funcionan como juego. Pero son caras (revelar 10 cámaras ronda los 150 €), las fotos salen como salen y no hay vídeos. Muchas parejas las combinan con una solución digital: las desechables para la gracia, el álbum QR para las fotos de verdad."),
        ("5. Una app de boda", "Apps como WedShoots piden a cada invitado descargar una aplicación, crear una cuenta e introducir un código. En la práctica la instala una minoría: la barrera es demasiado alta para alguien que solo quiere compartir tres fotos. Si la mayoría de tus invitados no la instala, el álbum se queda vacío."),
        ("6. Un álbum QR sin app", "El invitado escanea un código QR con la cámara, escribe su nombre y sube las fotos desde el navegador. Sin instalar nada, sin cuentas, en calidad original, con un enlace privado y con todo descargable en un ZIP. Es la opción que hemos construido con Fiestalia y la que mejor resultado da en bodas, porque elimina la fricción: si saben hacer una foto, saben subirla. Añade un Live Wall en la pantalla del banquete y el álbum se llena solo."),
        ("Lo que de verdad marca la diferencia", "Sea cual sea el método, estas tres cosas multiplican las fotos recibidas: que alguien lo anuncie por el micrófono después del primer baile, que el QR o el enlace esté en cada mesa y no solo en la entrada, y que mandes un recordatorio al día siguiente por la mañana, cuando la gente revisa lo que grabó de madrugada."),
     ],
     cta="Prueba el álbum QR gratis en tu boda"),
dict(slug="codigo-qr-para-fotos-de-boda", date="2026-10-18", read="6 min",
     title="Código QR para las fotos de tu boda: cómo hacerlo y dónde ponerlo",
     desc="Qué es un código QR para fotos de boda, cómo crearlo gratis, qué tamaño imprimir y los seis sitios donde colocarlo para que los invitados lo usen.",
     h1="Código QR para las fotos de tu boda: cómo hacerlo y dónde ponerlo",
     intro="Un código QR en las mesas es la forma más sencilla de que tus invitados compartan las fotos de la boda. Pero un QR solo es un enlace: lo importante es a dónde lleva, cómo se imprime y dónde se coloca. Aquí va todo lo práctico.",
     sections=[
        ("Qué es exactamente un «QR para fotos de boda»", "Es un código que, al escanearlo con la cámara del móvil, abre una página web donde los invitados suben sus fotos y ven las de los demás. El QR no guarda las fotos; solo abre el álbum. Por eso lo importante no es el QR sino el álbum al que apunta: si pide instalar una app o crear una cuenta, perderás a la mitad de los invitados antes de empezar."),
        ("Cómo crearlo gratis en dos minutos", "Con Fiestalia creas el álbum (nombre de la boda, fecha, un mensaje) y el QR se genera solo, junto con una tarjeta lista para imprimir y el QR en alta resolución en PNG. Las primeras 50 fotos son gratis, así que puedes probarlo antes de decidir el plan. Evita los generadores de QR genéricos con suscripción: muchos caducan el código si dejas de pagar, y el día de la boda el QR dejaría de funcionar."),
        ("Qué tamaño imprimir", "Para una tarjeta de mesa, un QR de 4 a 5 centímetros de lado se escanea sin problema desde la silla. Para un cartel en la entrada, al menos 15 centímetros. Regla práctica: la distancia de escaneo cómoda es unas diez veces el tamaño del código. Imprime en papel mate, no brillante, para evitar reflejos, y deja un margen blanco alrededor del código."),
        ("Los seis sitios donde funciona", "Una tarjeta en cada mesa, junto al menú o al número de mesa. Un cartel en el photocall o la entrada. En la barra. En la invitación digital o la web de la boda, para las fotos de la preboda. En el seating plan. Y en la pantalla del salón, si tienes Live Wall: el QR aparece en la esquina todo el tiempo."),
        ("Qué poner en la tarjeta", "Una frase corta y clara: «Escanea y sube tus fotos». Debajo, «Sin app, sin registro», porque es la objeción que todos tienen. Y una línea informando de que las fotos se comparten en un álbum privado: además de amable, es obligatorio por protección de datos."),
        ("El error más común", "Imprimir el QR y no decir nada. Un QR en la mesa sin que nadie lo anuncie se escanea poco. Pide al maestro de ceremonias o al DJ que lo mencione una vez después del primer baile. Con esa frase, el número de fotos se multiplica."),
     ],
     cta="Crea tu QR de boda gratis"),
dict(slug="alternativas-a-wedshoots", date="2026-10-15", read="8 min",
     title="Alternativas a WedShoots para compartir las fotos de tu boda (2026)",
     desc="Comparamos WedShoots con las alternativas sin app disponibles en España: Fiestalia, Eventocam, Momentshare y Google Fotos. Precios, límites y para quién es cada una.",
     h1="Alternativas a WedShoots para compartir las fotos de tu boda",
     intro="WedShoots, la app de Bodas.net, es la opción más conocida en España para reunir las fotos de los invitados. Pero obliga a cada invitado a instalar una aplicación, y eso en una boda es un problema. Estas son las alternativas que no lo exigen, con sus precios y límites según sus propias webs en octubre de 2026. Si algo ha cambiado, agradecemos el aviso.",
     sections=[
        ("El problema de WedShoots", "La app es gratuita y está integrada en Bodas.net, lo que la hace muy visible. Pero los invitados tienen que descargarla desde la tienda, crear una cuenta e introducir el código del álbum. Los vídeos están limitados a 30 segundos. En la práctica, una parte importante de los invitados, especialmente los mayores, nunca llega a instalarla, y las fotos que no se suben en la boda rara vez se suben después."),
        ("Fiestalia", "Nuestro servicio, así que juzga con esa información. Sin app: los invitados escanean el QR y suben desde el navegador. Álbum privado, calidad original, Live Wall para la pantalla del salón, descarga en ZIP y pago único por evento: gratis hasta 50 fotos, 19 € (500 fotos), 39 € (1.500 fotos y Live Wall) o 69 € (5.000 fotos). Los datos se alojan en la Unión Europea. Lo que aún no tenemos: la búsqueda por selfie está en desarrollo."),
        ("Eventocam", "Startup de Barcelona, también sin app. Planes de pago único desde 4,95 € hasta 39,95 € según su web. Es la opción más barata para un evento pequeño. Según las comparativas que hemos leído, la ventana de subida para los invitados es corta y no incluye pantalla en directo; comprueba esos puntos en su web antes de decidir."),
        ("Momentshare", "Servicio europeo con versión en español. Pago único de 19, 39 o 49 € por evento, con galería privada, QR e invitados ilimitados; la presentación en directo y los vídeos grandes entran en los planes superiores. Buena alternativa si buscas algo parecido a lo nuestro y quieres comparar."),
        ("Google Fotos o Google Drive", "Gratis y con calidad original, pero requiere cuenta de Google y que los invitados inicien sesión desde el móvil. Para un grupo pequeño de amigos funciona; para una boda con abuelos y tíos, no. Y no tiene nada de lo demás: ni QR propio, ni Live Wall, ni moderación."),
        ("Cómo elegir", "Si tus invitados son jóvenes y ya usan Bodas.net, WedShoots puede bastar. Si quieres que participe todo el mundo, incluidos los mayores, necesitas una opción sin app. Si tienes pantalla en el salón, el Live Wall es la función que más fotos genera. Y si te importa dónde se guardan las fotos, mira que el servicio aloje en la Unión Europea y lo diga en su política de privacidad."),
     ],
     cta="Prueba Fiestalia gratis con 50 fotos"),
dict(slug="live-wall-boda-pantalla-fotos-en-directo", date="2026-10-12", read="5 min",
     title="Live Wall en la boda: las fotos de los invitados en la pantalla, en directo",
     desc="Qué es un Live Wall o muro de fotos en directo, por qué multiplica las fotos que suben los invitados y qué necesitas para montarlo en el salón.",
     h1="Live Wall en la boda: las fotos de los invitados en la pantalla, en directo",
     intro="Un invitado hace una foto, la sube y tres segundos después aparece en la pantalla del salón. Los de la mesa de al lado la ven, se ríen y sacan el móvil. Así funciona un Live Wall, y es la razón por la que algunos álbumes acaban con 200 fotos y otros con 1.500.",
     sections=[
        ("Qué es", "Una página web a pantalla completa que muestra las últimas fotos del álbum según se suben, con el nombre de quien las subió y el código QR en una esquina para que quien lo vea pueda participar. No hace falta ningún equipo especial: cualquier cosa con navegador y salida a la pantalla sirve."),
        ("Por qué funciona tan bien", "Por tres motivos. Da una recompensa inmediata: subes y te ves. Recuerda constantemente que existe el álbum, sin que nadie tenga que repetirlo por el micrófono. Y crea una competición amable entre mesas. En las bodas en que lo hemos visto funcionar, el número de fotos subidas se multiplica por tres o más respecto al mismo álbum sin pantalla."),
        ("Qué necesitas", "Una pantalla o proyector con entrada HDMI, un portátil con Chrome y conexión a internet. Abres el enlace del Live Wall que te da el panel, pulsas F11 para pantalla completa y ya está. Si el salón tiene Smart TV con navegador, puedes abrirlo directamente en la tele. Un Chromecast o un Apple TV también sirven para enviar la pantalla desde el móvil."),
        ("Consejos prácticos", "Avisa al salón o al DJ el día antes para tener acceso al HDMI. Comprueba el wifi; si es flojo, comparte datos desde un móvil con buena cobertura. Enciende el Live Wall antes de que lleguen los invitados al banquete, con el álbum vacío: el mensaje «escanea el QR y sé el primero» invita a empezar. Y si quieres control, activa la moderación previa: solo aparecerá en pantalla lo que apruebes."),
        ("Cuándo apagarlo", "Durante la cena y el baile, encendido. Durante los discursos y el primer baile, muchas parejas prefieren apagarlo para que la atención esté en lo que pasa. Es un clic: cierra la pestaña y vuelve a abrirla después."),
     ],
     cta="Activa el Live Wall en tu álbum"),
]

def article_page(a):
    secs = "".join(f'<h2>{t}</h2><p>{d}</p>' for t, d in a["sections"])
    others = "".join(f'<li><a href="./{o["slug"]}.html">{o["title"]}</a></li>' for o in ARTICLES if o["slug"] != a["slug"])
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": a["date"], "inLanguage": "es", "author": {"@type": "Organization", "name": "Fiestalia"}, "publisher": {"@type": "Organization", "name": "SYNTH MASHI, S.L."}}, ensure_ascii=False) + '</script>'
    body = f"""
<main id="top">
<article class="post">
  <header class="post-head container narrow-text">
    <a class="eyebrow" href="./index.html">Blog</a>
    <h1>{a['h1']}</h1>
    <p class="post-meta">{fmt_date(a['date'])} · {a['read']} de lectura</p>
    <p class="lead">{a['intro']}</p>
  </header>
  <div class="container narrow-text post-body">{secs}
    <div class="post-cta"><b>{a['cta']}</b><p>Sin app, sin registro, pago único. Las primeras 50 fotos son gratis.</p><a class="btn btn-primary" href="app/crear.html">Crear mi álbum</a></div>
    <h3>Más artículos</h3><ul class="post-others">{others}</ul>
  </div>
</article>
</main>
"""
    return page(f"blog/{a['slug']}.html", a["title"] + " — Fiestalia", a["desc"], body, ld, prefix="../")

def fmt_date(iso):
    y, m, d = iso.split("-"); meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{int(d)} de {meses[int(m) - 1]} de {y}"

def blog_index():
    cards = "".join(f'<a class="post-card" href="./{a["slug"]}.html"><span class="post-meta">{fmt_date(a["date"])} · {a["read"]}</span><h3>{a["title"]}</h3><p>{a["desc"]}</p><span class="more">Leer →</span></a>' for a in ARTICLES)
    body = f"""
<main id="top">
<section class="hero hero-page hero-compact"><div class="container narrow-text">
  <span class="eyebrow">Blog</span>
  <h1 style="margin-top:16px">Guías y consejos para <em>no perder ni una foto</em></h1>
  <p class="lead">Cómo recoger las fotos de los invitados, dónde poner el QR, qué pantalla usar y qué alternativas existen. Escrito desde la experiencia de montar álbumes en bodas y eventos reales.</p>
</div></section>
<section class="section-tight"><div class="container"><div class="post-grid">{cards}</div></div></section>
{cta_block("Pon en práctica lo que has leído", "Crea tu álbum en dos minutos. Las primeras 50 fotos son gratis.")}
</main>
"""
    return page("blog/index.html", "Blog — Fiestalia", "Guías y consejos para recoger las fotos de los invitados en bodas y eventos: QR, Live Wall, alternativas y buenas prácticas.", body, prefix="../")

EXTRA_CSS = """
/* Guías */
.guide-steps { list-style: none; padding: 0; margin: 8px 0 0; display: grid; gap: 14px; counter-reset: g; }
.guide-step { display: flex; gap: 18px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px 22px; counter-increment: g; }
.guide-step .guide-icon { flex: none; width: 56px; height: 56px; border-radius: 16px; background: var(--brand-soft); display: grid; place-items: center; font-size: 26px; position: relative; }
.guide-step .guide-icon::after { content: counter(g); position: absolute; top: -8px; left: -8px; width: 22px; height: 22px; border-radius: 50%; background: var(--brand); color: #fff; font-size: 12px; font-weight: 800; display: grid; place-items: center; }
.guide-step h3 { font-size: 18px; font-weight: 800; }
.guide-step p { color: var(--ink-2); margin-top: 6px; }
.guide-list { list-style: none; padding: 0; margin: 20px 0 0; display: grid; gap: 12px; }
.guide-list li { display: flex; gap: 12px; align-items: flex-start; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius-sm); padding: 14px 16px; }
.guide-list li svg { flex: none; color: var(--accent); margin-top: 3px; }
.guide-list b { display: block; }
.guide-list p { color: var(--ink-2); margin-top: 4px; font-size: 15px; }
.warn { background: var(--purple-soft); border-left: 4px solid var(--accent); padding: 14px 16px; border-radius: 10px; font-size: 15px; color: var(--ink-2); }
.warn b { color: var(--ink); }
/* Demo */
.demo-grid { grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); }
.grid { display: grid; gap: 6px; margin-top: 20px; }
.grid .ph { position: relative; aspect-ratio: 1; border-radius: 10px; overflow: hidden; background: var(--bg-2); cursor: pointer; border: 0; padding: 0; }
.grid .ph img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform .25s; }
.grid .ph:hover img { transform: scale(1.04); }
.grid .ph .who { position: absolute; left: 0; right: 0; bottom: 0; padding: 18px 8px 6px; font-size: 12px; color: #fff; background: linear-gradient(transparent, rgba(0,0,0,.6)); text-align: left; }
.upload-bar { display: flex; justify-content: center; margin-top: 28px; }
.lightbox { position: fixed; inset: 0; background: rgba(10, 3, 6, .94); z-index: 100; display: grid; grid-template-rows: 1fr auto; }
.lightbox .lb-body { display: grid; place-items: center; padding: 56px 64px 10px; }
.lightbox .lb-body img { max-width: 100%; max-height: calc(100vh - 120px); border-radius: 8px; }
.lightbox .lb-cap { text-align: center; color: #ddd; padding: 10px 16px 20px; font-size: 14px; }
.lightbox button { position: absolute; background: rgba(255,255,255,.12); color: #fff; border: 0; width: 44px; height: 44px; border-radius: 50%; font-size: 26px; cursor: pointer; }
.lightbox .lb-close { top: 14px; right: 14px; font-size: 18px; }
.lightbox .lb-prev { left: 12px; top: 50%; transform: translateY(-50%); }
.lightbox .lb-next { right: 12px; top: 50%; transform: translateY(-50%); }
/* Blog */
.post-head { padding: 56px 0 10px; }
.post-head h1 { font-family: var(--font-display); font-size: clamp(30px, 4.2vw, 46px); font-weight: 700; margin-top: 14px; }
.post-meta { color: var(--ink-3); font-size: 14px; margin-top: 10px; display: block; }
.post-body { padding: 10px 0 60px; }
.post-body h2 { font-family: var(--font-display); font-size: 26px; font-weight: 700; margin: 36px 0 10px; }
.post-body p { color: var(--ink-2); font-size: 17px; line-height: 1.75; }
.post-body h3 { font-size: 18px; font-weight: 800; margin: 40px 0 10px; }
.post-others { display: grid; gap: 8px; margin: 0; padding: 0; list-style: none; }
.post-others a { color: var(--brand); font-weight: 700; }
.post-cta { margin-top: 36px; background: var(--card); border: 1.5px solid var(--accent); border-radius: var(--radius); padding: 24px 26px; display: grid; gap: 6px; justify-items: start; }
.post-cta b { font-size: 20px; }
.post-cta p { margin: 0 0 8px; font-size: 15px; }
.post-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 10px; }
.post-card { display: block; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px; color: inherit; transition: transform .2s, box-shadow .2s; }
.post-card:hover { transform: translateY(-3px); box-shadow: var(--shadow); }
.post-card h3 { font-family: var(--font-display); font-size: 22px; font-weight: 700; margin-top: 8px; }
.post-card p { color: var(--ink-2); margin-top: 10px; font-size: 15px; }
.post-card .more { display: inline-block; margin-top: 14px; color: var(--brand); font-weight: 800; }
@media (max-width: 820px) { .post-grid { grid-template-columns: 1fr; } .guide-step { padding: 16px; gap: 14px; } .lightbox .lb-body { padding: 56px 8px 10px; } .demo-grid { grid-template-columns: repeat(3, 1fr); gap: 3px; } }
"""

EXTRA_JS = """
// Álbum de ejemplo: lightbox
(function () {
  const photos = window.DEMO_PHOTOS; const grid = document.getElementById("demoGrid");
  if (!photos || !grid) return;
  grid.addEventListener("click", (e) => {
    const btn = e.target.closest(".ph"); if (!btn) return;
    let i = +btn.dataset.i;
    const el = document.createElement("div"); el.className = "lightbox";
    el.innerHTML = '<button class="lb-close" aria-label="Cerrar">✕</button><button class="lb-prev" aria-label="Anterior">‹</button><div class="lb-body"></div><button class="lb-next" aria-label="Siguiente">›</button><div class="lb-cap"></div>';
    document.body.appendChild(el); document.body.style.overflow = "hidden";
    const show = () => { const p = photos[i]; el.querySelector(".lb-body").innerHTML = `<img src="${p.src}" alt="${p.cap}">`; el.querySelector(".lb-cap").innerHTML = `<b>${p.who}</b> · ${p.cap}`; };
    const close = () => { el.remove(); document.body.style.overflow = ""; document.removeEventListener("keydown", key); };
    const prev = () => { i = (i - 1 + photos.length) % photos.length; show(); }, next = () => { i = (i + 1) % photos.length; show(); };
    const key = (ev) => { if (ev.key === "Escape") close(); if (ev.key === "ArrowLeft") prev(); if (ev.key === "ArrowRight") next(); };
    el.querySelector(".lb-close").onclick = close; el.querySelector(".lb-prev").onclick = prev; el.querySelector(".lb-next").onclick = next;
    el.addEventListener("click", (ev) => { if (ev.target === el) close(); }); document.addEventListener("keydown", key); show();
  });
})();
"""

def main():
    write("guia-invitados.html", guia_invitados())
    write("guia-organizadores.html", guia_organizadores())
    write("demo.html", demo())
    write("404.html", not_found())
    write("blog/index.html", blog_index())
    for a in ARTICLES: write(f"blog/{a['slug']}.html", article_page(a))
    css = open(os.path.join(OUT, "pages.css"), encoding="utf-8").read()
    if "/* Guías */" not in css: open(os.path.join(OUT, "pages.css"), "a", encoding="utf-8").write(EXTRA_CSS)
    js = open(os.path.join(OUT, "pages.js"), encoding="utf-8").read()
    if "Álbum de ejemplo: lightbox" not in js: open(os.path.join(OUT, "pages.js"), "a", encoding="utf-8").write(EXTRA_JS)
    print("extra pages generated:", 5 + len(ARTICLES))

if __name__ == "__main__":
    main()

# ───────────────────────────── Precios ─────────────────────────────
def precios():
    faq = [("¿Es una suscripción?", "No. Cada álbum se paga una sola vez y ya está. Sin renovaciones automáticas, sin cuotas mensuales. Si organizas otro evento, creas otro álbum y eliges su plan."),
           ("¿Qué pasa si me quedo sin fotos a mitad del evento?", "Las nuevas subidas quedan en espera y el panel te avisa. Amplías el plan en un clic desde el móvil y las fotos en espera se publican automáticamente. Nadie pierde nada."),
           ("¿Puedo empezar gratis y pagar después?", "Sí, es lo habitual. Creas el álbum gratis, imprimes el QR y, si ves que la fiesta va a superar las 50 fotos, pagas el plan cuando quieras, incluso el mismo día."),
           ("¿El precio incluye IVA?", "Sí, todos los precios se muestran con el IVA incluido. Emitimos factura por cada pago, con tus datos o los de tu empresa."),
           ("¿Hay límite de invitados?", "No. Pagas por volumen de fotos y gigabytes, no por personas. El número de invitados junto a cada plan es solo una orientación: calculamos unas 25 fotos por invitado."),
           ("¿Qué medios de pago aceptáis?", "Tarjeta de crédito o débito, Bizum, Apple Pay y Google Pay, a través de una pasarela de pago certificada. No guardamos los datos de tu tarjeta."),
           ("¿Puedo pedir la devolución?", "Si eres consumidor tienes 14 días para desistir. Como el servicio empieza al momento, si ya has usado el plan de pago podemos descontar la parte proporcional. Los detalles están en las <a href='legal/condiciones.html'>condiciones de uso</a>."),
           ("Organizo muchos eventos, ¿hay descuento?", "Sí: los <a href='profesionales.html'>packs para profesionales</a> bajan el precio por álbum hasta 20 € e incluyen tu logo en las tarjetas QR y el Live Wall.")]
    body = f"""
<main id="top">
<section class="hero hero-page hero-compact"><div class="container narrow-text center">
  <span class="eyebrow">Precios</span>
  <h1 style="margin-top:16px">Pago único. <em>Sin suscripciones.</em> Sin sorpresas.</h1>
  <p class="lead">Empieza gratis y amplía solo si tu álbum lo necesita. Pagas por volumen de fotos, no por número de invitados. IVA incluido.</p>
</div></section>

<section class="section-tight pricing-bg" id="precios"><div class="container">
  <div class="calc">
    <div class="calc-row"><label for="guests">¿Cuántos invitados tendrás?</label><output id="guestsOut" for="guests">60 invitados</output></div>
    <input type="range" id="guests" min="5" max="300" step="5" value="60">
    <p class="calc-result" id="calcResult"></p>
  </div>
  <div class="plans" id="plans"></div>
  <p class="pricing-foot">Precios con IVA incluido. Pago seguro con tarjeta, Bizum, Apple Pay o Google Pay. El álbum se activa al instante tras el pago.</p>
</div></section>

<section class="section-tight"><div class="container">
  <div class="center"><span class="eyebrow">Qué incluye cada plan</span><h2 class="h2">Compara los planes</h2></div>
  <div class="compare"><table>
    <thead><tr><th></th><th>Gratis</th><th>Básico</th><th class="us">Celebración</th><th>Gran evento</th></tr></thead>
    <tbody>
      <tr><td>Precio</td><td>0 €</td><td>19 €</td><td class="us">39 €</td><td>69 €</td></tr>
      <tr><td>Fotos y vídeos</td><td>50</td><td>500</td><td class="us">1.500</td><td>5.000</td></tr>
      <tr><td>Almacenamiento</td><td>500 MB</td><td>5 GB</td><td class="us">20 GB</td><td>60 GB</td></tr>
      <tr><td>Álbum disponible</td><td>1 mes</td><td>6 meses</td><td class="us">12 meses</td><td>24 meses</td></tr>
      <tr><td>Invitados</td><td colspan="4" style="text-align:center">Sin límite en todos los planes</td></tr>
      <tr><td>Galería privada con QR y enlace</td><td class="yes">✓</td><td class="yes">✓</td><td class="us yes">✓</td><td class="yes">✓</td></tr>
      <tr><td>Subida sin app ni registro</td><td class="yes">✓</td><td class="yes">✓</td><td class="us yes">✓</td><td class="yes">✓</td></tr>
      <tr><td>Calidad original y descarga en ZIP</td><td class="yes">✓</td><td class="yes">✓</td><td class="us yes">✓</td><td class="yes">✓</td></tr>
      <tr><td>Moderación previa</td><td class="yes">✓</td><td class="yes">✓</td><td class="us yes">✓</td><td class="yes">✓</td></tr>
      <tr><td>Tarjetas QR imprimibles</td><td class="yes">✓</td><td class="yes">✓</td><td class="us yes">✓</td><td class="yes">✓</td></tr>
      <tr><td>Live Wall en pantalla</td><td class="no">—</td><td class="no">—</td><td class="us yes">✓</td><td class="yes">✓</td></tr>
      <tr><td>Tamaño máximo por vídeo</td><td>200 MB</td><td>200 MB</td><td class="us">200 MB</td><td>200 MB</td></tr>
      <tr><td>Búsqueda por selfie</td><td colspan="4" style="text-align:center" class="so">Próximamente, con consentimiento del invitado</td></tr>
      <tr><td>Factura</td><td class="so">—</td><td class="yes">✓</td><td class="us yes">✓</td><td class="yes">✓</td></tr>
    </tbody>
  </table></div>
</div></section>

<section class="section-tight"><div class="container narrow-text center">
  <span class="eyebrow">Para profesionales</span>
  <h2 class="h2">¿Más de cinco eventos al año?</h2>
  <p class="lead">Los packs para wedding planners, fotógrafos, salones y agencias bajan el precio por álbum hasta 20 € e incluyen tu logo en las tarjetas y el Live Wall.</p>
  <div class="actions" style="justify-content:center"><a class="btn btn-primary" href="profesionales.html">Ver packs profesionales</a></div>
</div></section>

<section class="section-tight"><div class="container">
  <div class="center"><span class="eyebrow">Preguntas sobre precios y pago</span><h2 class="h2">Lo que suelen preguntar</h2></div>
  {faq_html(faq)}
</div></section>
{cta_block("Empieza gratis hoy", "Crea el álbum, imprime el QR y decide el plan cuando lo necesites.")}
</main>
"""
    html_str = page("precios.html", "Precios — Fiestalia: álbum QR desde 0 €, pago único sin suscripción", "Planes de Fiestalia: gratis hasta 50 fotos, Básico 19 €, Celebración 39 € con Live Wall y Gran evento 69 €. Pago único con IVA, sin suscripción ni límite de invitados.", body, faq_jsonld(faq), active="precios.html")
    # Esta página reutiliza el calculador y las tarjetas de planes de la landing (app.js) en lugar de pages.js
    return html_str.replace('<script src="pages.js"></script>', '<script src="app.js"></script>')

# ───────────────────────────── Preguntas frecuentes ─────────────────────────────
GENERAL_FAQ = [
    ("¿Mis invitados tienen que instalar algo o registrarse?", "No. Escanean el QR con la cámara del móvil, se abre el álbum en el navegador y ya pueden subir fotos y vídeos. Solo les pedimos un nombre para saber quién ha subido cada foto."),
    ("¿Hay límite de invitados?", "No. Pagas solo por el volumen del álbum (fotos y gigabytes), no por personas. El número de invitados que aparece junto a cada plan es una orientación: calculamos unas 25 fotos por invitado."),
    ("¿Cómo funciona la búsqueda por selfie? ¿Es seguro?", "El invitado se hace una selfie y le mostramos las fotos del álbum en las que aparece. La comparación se hace solo dentro del álbum, no identificamos a nadie ni cruzamos datos con otros eventos. Es opcional, requiere consentimiento expreso y la selfie se elimina al terminar. Está en desarrollo; más detalles en la <a href='legal/privacidad.html#biometria'>política de privacidad</a>."),
    ("¿Qué pasa cuando llego a las 50 fotos gratis?", "El álbum sigue visible, pero las nuevas subidas quedan en espera hasta que amplías el plan. Puedes ampliar en cualquier momento, incluso durante el evento, y las fotos en espera se publican automáticamente."),
    ("¿Cuánto tiempo se guarda el álbum?", "Depende del plan: de 1 a 24 meses. Antes de que caduque te avisamos por correo para que descargues el ZIP completo o amplíes el almacenamiento."),
    ("¿Puedo subir vídeos?", "Sí. Fotos y vídeos cuentan igual como elementos del álbum, hasta 200 MB por vídeo. Se guardan en calidad original, sin compresión."),
    ("¿Cómo pongo el Live Wall en la pantalla del salón?", "Abre el enlace de presentación en cualquier portátil, Smart TV o reproductor conectado al proyector. Es una página web a pantalla completa que se actualiza sola. Hay una <a href='guia-organizadores.html'>guía detallada</a>."),
    ("¿Dónde se almacenan las fotos?", "En servidores dentro de la Unión Europea, cifradas y accesibles únicamente mediante el enlace de tu álbum. Cumplimos el RGPD y la LOPDGDD."),
    ("¿Es legal recoger las fotos de los invitados?", "Sí, siempre que les informes de que el evento se fotografía y se comparte en un álbum privado. En la <a href='guia-organizadores.html'>guía para organizadores</a> hay un texto modelo para la tarjeta QR."),
    ("He perdido el enlace del panel, ¿qué hago?", "Si creaste el álbum desde este mismo navegador, en <a href='app/crear.html'>Crear álbum</a> verás la lista de tus álbumes con el acceso al panel. Si no, escríbenos desde la página de <a href='contacto.html'>contacto</a> con el correo que usaste al crearlo y te ayudamos a recuperarlo."),
]

def faq_page():
    groups = [("general", "Sobre el servicio", GENERAL_FAQ)]
    for ev in EVENTS:
        groups.append((ev["file"].replace(".html", ""), ev["eyebrow"].replace("Álbum QR para ", "").capitalize(), ev["faq"]))
    all_items = [q for _, _, items in groups for q in items]
    toc = "".join(f'<a href="#{gid}">{title}</a>' for gid, title, _ in groups)
    secs = "".join(f'<section class="faq-group" id="{gid}"><h2 class="h2">{title}</h2>{faq_html(items, open_first=False)}</section>' for gid, title, items in groups)
    body = f"""
<main id="top">
<section class="hero hero-page hero-compact"><div class="container narrow-text center">
  <span class="eyebrow">Preguntas frecuentes</span>
  <h1 style="margin-top:16px">Todo lo que querrás saber, <em>en un solo sitio</em></h1>
  <p class="lead">Las preguntas que nos hacen parejas, familias, empresas y profesionales. Si la tuya no está, <a href="contacto.html">escríbenos</a> y la añadimos.</p>
  <nav class="faq-toc" aria-label="Secciones">{toc}</nav>
</div></section>
<section class="section-tight"><div class="container narrow-text">{secs}</div></section>
{cta_block("¿Resuelto? Pues a por el álbum", "Crea el tuyo en dos minutos. Las primeras 50 fotos son gratis.")}
</main>
"""
    return page("faq.html", "Preguntas frecuentes — Fiestalia", "Respuestas a las dudas más habituales sobre el álbum QR de Fiestalia: invitados, límites, privacidad, Live Wall, vídeos, caducidad y casos por tipo de evento.", body, faq_jsonld(all_items), active="faq.html")

FAQ_CSS = """
/* FAQ */
.faq-toc { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 22px; }
.faq-toc a { font-size: 14px; font-weight: 700; padding: 8px 14px; border-radius: 999px; border: 1.5px solid var(--line); background: var(--card); color: var(--ink-2); }
.faq-toc a:hover { border-color: var(--brand); color: var(--brand); }
.faq-group + .faq-group { margin-top: 48px; }
.faq-group .h2 { margin-bottom: 8px; }
.faq-group .faq { margin-top: 16px; }
"""

def main_more():
    write("precios.html", precios())
    write("faq.html", faq_page())
    css = open(os.path.join(OUT, "pages.css"), encoding="utf-8").read()
    if "/* FAQ */" not in css: open(os.path.join(OUT, "pages.css"), "a", encoding="utf-8").write(FAQ_CSS)
    print("precios.html, faq.html generated")

if __name__ == "__main__":
    main_more()
