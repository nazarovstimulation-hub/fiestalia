/* Utilidades compartidas de la app: tema, marca, QR, miniaturas, formato, toasts, lightbox */
window.UI = (function () {
  const B = window.BRAND || {};
  const CFG = window.FIESTALIA_CONFIG || {};

  // Tema de color igual que en la landing
  const theme = new URLSearchParams(location.search).get("theme") || B.theme;
  if (theme && theme !== "fiesta") document.documentElement.setAttribute("data-theme", theme);
  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = B.name));
  const yr = document.getElementById("year"); if (yr) yr.textContent = new Date().getFullYear();

  const qs = (s, r) => (r || document).querySelector(s);
  const qsa = (s, r) => Array.from((r || document).querySelectorAll(s));
  const params = new URLSearchParams(location.search);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmtInt = (n) => new Intl.NumberFormat("es-ES").format(n);
  const fmtDate = (iso) => iso ? new Date(iso).toLocaleDateString("es-ES", { day: "numeric", month: "long", year: "numeric" }) : "";
  const fmtBytes = (b) => b > 1e9 ? (b / 1e9).toFixed(1) + " GB" : b > 1e6 ? (b / 1e6).toFixed(1) + " MB" : Math.round(b / 1e3) + " KB";
  const timeAgo = (iso) => {
    const s = Math.max(0, (Date.now() - new Date(iso)) / 1000);
    if (s < 60) return "ahora mismo"; if (s < 3600) return `hace ${Math.floor(s / 60)} min`;
    if (s < 86400) return `hace ${Math.floor(s / 3600)} h`; return `hace ${Math.floor(s / 86400)} d`;
  };

  // URLs de la app (relativas a /app/)
  const base = location.href.replace(/[^/]*$/, "");
  const albumUrl = (code) => `${base}album.html?a=${code}`;
  const panelUrl = (code, key) => `${base}panel.html?a=${code}&k=${key}`;
  const liveUrl = (code) => `${base}live.html?a=${code}`;

  // Toast
  function toast(msg, kind) {
    let box = qs("#toasts"); if (!box) { box = document.createElement("div"); box.id = "toasts"; document.body.appendChild(box); }
    const t = document.createElement("div"); t.className = "toast " + (kind || ""); t.textContent = msg; box.appendChild(t);
    setTimeout(() => { t.classList.add("out"); setTimeout(() => t.remove(), 300); }, 3600);
  }

  // QR en SVG (qrcode-generator)
  function qrSvg(text, size) {
    if (!window.qrcode) return "";
    const q = window.qrcode(0, "M"); q.addData(text); q.make();
    const n = q.getModuleCount(); const cell = (size || 256) / (n + 8);
    let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n + 8} ${n + 8}" width="${size || 256}" height="${size || 256}" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="#fff"/>`;
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (q.isDark(r, c)) s += `<rect x="${c + 4}" y="${r + 4}" width="1" height="1" fill="#1a0a10"/>`;
    return s + "</svg>";
  }
  function qrPngDataUrl(text, size) {
    return new Promise((res) => {
      const svg = qrSvg(text, size || 1024); const img = new Image();
      img.onload = () => { const c = document.createElement("canvas"); c.width = c.height = size || 1024; c.getContext("2d").drawImage(img, 0, 0); res(c.toDataURL("image/png")); };
      img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
    });
  }

  // Miniatura JPEG + dimensiones para imágenes; póster para vídeos
  function readImage(file) {
    return new Promise((res, rej) => { const img = new Image(); img.onload = () => res(img); img.onerror = rej; img.src = URL.createObjectURL(file); });
  }
  function canvasToBlob(canvas, q) { return new Promise((res) => canvas.toBlob(res, "image/jpeg", q || 0.82)); }
  async function makeThumb(file) {
    const max = CFG.thumbSize || 480;
    if (file.type.startsWith("image/")) {
      const img = await readImage(file);
      const scale = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight));
      const c = document.createElement("canvas"); c.width = Math.round(img.naturalWidth * scale); c.height = Math.round(img.naturalHeight * scale);
      c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(img.src);
      return { thumb: await canvasToBlob(c), width: img.naturalWidth, height: img.naturalHeight };
    }
    if (file.type.startsWith("video/")) {
      return new Promise((res) => {
        const v = document.createElement("video"); v.preload = "metadata"; v.muted = true; v.playsInline = true;
        v.onloadeddata = () => { v.currentTime = Math.min(1, (v.duration || 2) / 2); };
        v.onseeked = async () => {
          const scale = Math.min(1, max / Math.max(v.videoWidth, v.videoHeight));
          const c = document.createElement("canvas"); c.width = Math.round(v.videoWidth * scale); c.height = Math.round(v.videoHeight * scale);
          c.getContext("2d").drawImage(v, 0, 0, c.width, c.height);
          const thumb = await canvasToBlob(c); URL.revokeObjectURL(v.src);
          res({ thumb, width: v.videoWidth, height: v.videoHeight, duration: v.duration });
        };
        v.onerror = () => res({ thumb: null });
        v.src = URL.createObjectURL(file);
      });
    }
    return { thumb: null };
  }

  // Lightbox sencillo
  function lightbox(items, index) {
    let i = index || 0;
    const el = document.createElement("div"); el.className = "lightbox";
    el.innerHTML = `<button class="lb-close" aria-label="Cerrar">✕</button><button class="lb-prev" aria-label="Anterior">‹</button><div class="lb-body"></div><button class="lb-next" aria-label="Siguiente">›</button><div class="lb-cap"></div>`;
    document.body.appendChild(el); document.body.style.overflow = "hidden";
    const body = qs(".lb-body", el), cap = qs(".lb-cap", el);
    async function show() {
      const it = items[i]; const url = await window.store.photoUrl(it);
      body.innerHTML = it.type === "video" ? `<video src="${url}" controls autoplay playsinline></video>` : `<img src="${url}" alt="">`;
      cap.innerHTML = `<b>${esc(it.uploader_name)}</b> · ${timeAgo(it.created_at)} · <a href="${url}" download>Descargar</a>`;
    }
    const close = () => { el.remove(); document.body.style.overflow = ""; document.removeEventListener("keydown", key); };
    const prev = () => { i = (i - 1 + items.length) % items.length; show(); };
    const next = () => { i = (i + 1) % items.length; show(); };
    const key = (e) => { if (e.key === "Escape") close(); if (e.key === "ArrowLeft") prev(); if (e.key === "ArrowRight") next(); };
    qs(".lb-close", el).onclick = close; qs(".lb-prev", el).onclick = prev; qs(".lb-next", el).onclick = next;
    el.addEventListener("click", (e) => { if (e.target === el) close(); });
    document.addEventListener("keydown", key);
    let sx = 0; el.addEventListener("touchstart", (e) => (sx = e.touches[0].clientX), { passive: true });
    el.addEventListener("touchend", (e) => { const dx = e.changedTouches[0].clientX - sx; if (dx > 60) prev(); if (dx < -60) next(); });
    show();
  }

  function copy(text) { return navigator.clipboard.writeText(text).then(() => toast("Copiado")); }

  // Banner de modo demo
  function demoBanner() {
    if (window.store && window.store.mode === "demo") {
      const d = document.createElement("div"); d.className = "demo-banner";
      d.innerHTML = `<b>Modo demo:</b> los álbumes y las fotos se guardan solo en este navegador. Para abrirlos desde otros móviles hay que conectar el servidor (ver <code>app/config.js</code>).`;
      document.body.prepend(d);
    }
  }

  return { qs, qsa, params, esc, fmtInt, fmtDate, fmtBytes, timeAgo, albumUrl, panelUrl, liveUrl, toast, qrSvg, qrPngDataUrl, makeThumb, lightbox, copy, demoBanner, theme };
})();
