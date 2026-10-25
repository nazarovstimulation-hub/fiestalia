# -*- coding: utf-8 -*-
"""Genera sitemap.xml, robots.txt y la imagen Open Graph (assets/og-image.png).
Uso: python3 tools/gen_seo.py  (después de gen_pages.py y gen_pages_extra.py)"""
import os, sys, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_config import SITE_URL

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")

def sitemap():
    today = datetime.date.today().isoformat()
    pages = []
    for f in sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "blog", "*.html"))):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        if rel == "404.html": continue
        html = open(f, encoding="utf-8").read()
        if "noindex" in html: continue
        loc = SITE_URL + ("" if rel == "index.html" else rel)
        prio = "1.0" if rel == "index.html" else "0.9" if rel in ("precios.html", "bodas.html") else "0.6" if rel.startswith("blog/") else "0.8"
        freq = "weekly" if rel in ("index.html", "precios.html", "blog/index.html") else "monthly"
        pages.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(pages) + "\n</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    return len(pages)

def robots():
    txt = f"""User-agent: *
Allow: /
# Los álbumes y el panel son privados: no indexar
Disallow: /app/
# Páginas legales sin interés para buscadores
Disallow: /legal/

Sitemap: {SITE_URL}sitemap.xml
"""
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(txt)

def og_image():
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), (250, 245, 236))  # champán
    d = ImageDraw.Draw(im)
    # Mancha suave burdeos a la derecha y dorada abajo a la izquierda
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    g.ellipse([760, -220, 1500, 420], fill=(122, 18, 50, 38)); g.ellipse([-260, 420, 420, 900], fill=(201, 168, 76, 48))
    glow = glow.filter(ImageFilter.GaussianBlur(120)); im.paste(glow, (0, 0), glow)
    # Logo
    logo = Image.open(os.path.join(ROOT, "assets", "logo.png")).convert("RGBA")
    lw = 560; lh = round(logo.height * lw / logo.width); logo = logo.resize((lw, lh), Image.LANCZOS)
    im.paste(logo, (80, 92), logo)
    # Tipografías: Playfair/Manrope no están en el sistema; DejaVu como aproximación legible
    def font(size, bold=False):
        for p in ([ "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" ]):
            if os.path.exists(p): return ImageFont.truetype(p, size)
        return ImageFont.load_default()
    def sans(size, bold=False):
        p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()
    d.text((84, 250), "El álbum de tu evento,", font=font(54, True), fill=(42, 16, 22))
    d.text((84, 318), "hecho por tus invitados", font=font(54, True), fill=(122, 18, 50))
    d.text((86, 412), "Escanean un QR, suben fotos y vídeos sin app.", font=sans(26), fill=(94, 69, 75))
    d.text((86, 450), "Galería privada · Live Wall · Descarga en ZIP · 50 fotos gratis", font=sans(22), fill=(94, 69, 75))
    # Píldora dorada
    d.rounded_rectangle([84, 520, 470, 578], radius=29, fill=(201, 168, 76))
    d.text((112, 534), "fiestalia.com", font=sans(26, True), fill=(42, 16, 22))
    # QR decorativo a la derecha
    import random; random.seed(3)
    qx, qy, cell, n = 900, 300, 9, 25
    d.rounded_rectangle([qx - 28, qy - 28, qx + n * cell + 28, qy + n * cell + 28], radius=22, fill=(255, 255, 255))
    for r in range(n):
        for c in range(n):
            fin = (r < 7 and c < 7) or (r < 7 and c >= n - 7) or (r >= n - 7 and c < 7)
            if fin:
                edge = r in (0, 6) or c in (0, 6) or r in (n - 7, n - 1) or c in (n - 7, n - 1)
                inner = (2 <= r <= 4 and 2 <= c <= 4) or (2 <= r <= 4 and n - 5 <= c <= n - 3) or (n - 5 <= r <= n - 3 and 2 <= c <= 4)
                if edge or inner: d.rectangle([qx + c * cell, qy + r * cell, qx + c * cell + cell - 1, qy + r * cell + cell - 1], fill=(42, 16, 22))
            elif random.random() < 0.42:
                d.rectangle([qx + c * cell, qy + r * cell, qx + c * cell + cell - 1, qy + r * cell + cell - 1], fill=(42, 16, 22))
    im.save(os.path.join(ROOT, "assets", "og-image.png"), optimize=True)

if __name__ == "__main__":
    n = sitemap(); robots(); og_image()
    print(f"sitemap: {n} urls · robots.txt · og-image.png")
