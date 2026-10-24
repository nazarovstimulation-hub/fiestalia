/* Lógica de la landing: marca, calculador de planes, mockups animados, menú. */
(function () {
  const B = window.BRAND || {};

  /* ── Tema de color: ?theme=oro|noche|rosa o BRAND.theme ─ */
  const themeParam = new URLSearchParams(location.search).get("theme");
  const theme = themeParam || B.theme;
  if (theme && theme !== "fiesta") document.documentElement.setAttribute("data-theme", theme);
  const fmtInt = (n) => new Intl.NumberFormat("es-ES").format(n);
  const fmtEur = (n) => n === 0 ? "0" : new Intl.NumberFormat("es-ES", { maximumFractionDigits: 0 }).format(n);

  /* ── Marca ──────────────────────────────────────────────── */
  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = B.name));
  document.querySelectorAll("[data-brand-tagline]").forEach((el) => (el.textContent = B.tagline + "."));
  document.querySelectorAll("[data-brand-city]").forEach((el) => (el.textContent = B.city));
  document.querySelectorAll("[data-brand-free]").forEach((el) => (el.textContent = B.freePhotos));
  document.querySelectorAll("[data-brand-ppg]").forEach((el) => (el.textContent = B.photosPerGuest));
  document.querySelectorAll("[data-brand-email]").forEach((el) => { el.textContent = B.email; el.href = "mailto:" + B.email; });
  document.querySelectorAll("[data-brand-whatsapp]").forEach((el) => {
    el.textContent = "WhatsApp " + B.whatsapp;
    el.href = "https://wa.me/" + B.whatsapp.replace(/\D/g, "");
  });
  document.querySelectorAll("[data-brand-title]").forEach((el) => {
    const t = `${B.name} — Álbum QR de tu evento con búsqueda por selfie`;
    if (el.tagName === "TITLE") el.textContent = t; else el.setAttribute("content", t);
  });
  const desc = document.querySelector("[data-brand-desc]");
  if (desc) desc.setAttribute("content", `Tus invitados escanean un QR y suben fotos y vídeos sin instalar nada. Búsqueda por selfie, pantalla en directo y descarga en ZIP. Las primeras ${B.freePhotos} fotos, gratis.`);
  document.getElementById("year").textContent = new Date().getFullYear();

  /* ── Planes ─────────────────────────────────────────────── */
  const check = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>';
  const plansEl = document.getElementById("plans");
  const plans = B.plans || [];

  function renderPlans() {
    plansEl.innerHTML = plans.map((p) => `
      <article class="plan ${p.featured ? "featured" : ""}" data-plan="${p.id}">
        ${p.featured ? '<span class="plan-badge">Más elegido</span>' : ""}
        <h3>${p.name}</h3>
        <div class="price"><b>${fmtEur(p.price)} €</b><span>${p.price === 0 ? "para siempre" : "pago único"}</span></div>
        <p class="guests">≈ ${fmtInt(p.guests)} invitados</p>
        <ul>
          <li>${check}<span><b>${fmtInt(p.photos)}</b> fotos y vídeos</span></li>
          <li>${check}<span>${p.gb < 1 ? Math.round(p.gb * 1000) + " MB" : p.gb + " GB"} de almacenamiento</span></li>
          <li>${check}<span>Galería privada con QR</span></li>
          <li class="${p.selfie ? "" : "off"}">${check}<span>Búsqueda por selfie</span></li>
          <li class="${p.liveWall ? "" : "off"}">${check}<span>Live Wall en pantalla</span></li>
          <li>${check}<span>Descarga en ZIP</span></li>
          <li>${check}<span>Álbum disponible ${p.months} ${p.months === 1 ? "mes" : "meses"}</span></li>
        </ul>
        <div class="plan-spacer"></div>
        <a class="btn ${p.featured ? "btn-primary" : "btn-ghost"}" href="app/crear.html?plan=${p.id}">${p.price === 0 ? "Empezar gratis" : "Elegir " + p.name}</a>
      </article>`).join("");
  }
  renderPlans();

  /* ── Calculador ─────────────────────────────────────────── */
  const range = document.getElementById("guests");
  const out = document.getElementById("guestsOut");
  const result = document.getElementById("calcResult");

  function recommend(guests) {
    const needed = guests * (B.photosPerGuest || 25);
    const plan = plans.find((p) => p.photos >= needed) || plans[plans.length - 1];
    out.textContent = `${guests} invitados`;
    result.innerHTML = `Con unas ${B.photosPerGuest} fotos por persona necesitarás alrededor de <b>${fmtInt(needed)} fotos</b>. Te recomendamos el plan <b>${plan.name}</b>${plan.price ? ` (${fmtEur(plan.price)} € pago único)` : " (gratis)"}.`;
    document.querySelectorAll(".plan").forEach((el) => el.classList.toggle("recommended", el.dataset.plan === plan.id));
  }
  range.addEventListener("input", () => recommend(+range.value));
  recommend(+range.value);

  /* ── Mockups: feed del móvil y Live Wall ────────────────── */
  const palette = ["#f2b5a0", "#e8c9a0", "#c9d6c3", "#b8c7dd", "#e4b7d1", "#f5d58a", "#a9c7c0", "#d9b3a3", "#c8bfe0", "#f0a287", "#bcd4a8", "#e9d3b5"];
  const pick = (i) => palette[i % palette.length];

  const feed = document.getElementById("feed");
  if (feed) {
    for (let i = 0; i < 12; i++) { const d = document.createElement("div"); d.style.setProperty("--c", pick(i)); feed.appendChild(d); }
    let n = 12;
    setInterval(() => {
      const d = document.createElement("div");
      d.style.setProperty("--c", pick(n++)); d.className = "new";
      feed.prepend(d);
      if (feed.children.length > 12) feed.lastElementChild.remove();
    }, 2600);
  }

  const wall = document.getElementById("wall");
  if (wall) {
    const layout = ["big", "", "", "", "", "", "", "big", "", "", ""];
    layout.forEach((cls, i) => { const d = document.createElement("div"); d.className = cls; d.style.setProperty("--c", pick(i + 3)); wall.appendChild(d); });
    let k = 20;
    setInterval(() => {
      const cells = [...wall.children].filter((c) => !c.classList.contains("big"));
      const cell = cells[Math.floor(Math.random() * cells.length)];
      cell.classList.remove("new"); void cell.offsetWidth;
      cell.style.setProperty("--c", pick(k++)); cell.classList.add("new");
    }, 1800);
  }

  /* ── QR decorativo (patrón pseudoaleatorio, no escaneable) ─ */
  const qr = document.getElementById("qr");
  if (qr) {
    let seed = 7; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
    const N = 29; let s = "";
    const finder = (x, y) => `<rect x="${x}" y="${y}" width="7" height="7" fill="#1d1a19"/><rect x="${x + 1}" y="${y + 1}" width="5" height="5" fill="#fff"/><rect x="${x + 2}" y="${y + 2}" width="3" height="3" fill="#1d1a19"/>`;
    const inFinder = (x, y) => (x < 8 && y < 8) || (x > N - 9 && y < 8) || (x < 8 && y > N - 9);
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      if (inFinder(x, y)) continue;
      if (rnd() < 0.45) s += `<rect x="${x}" y="${y}" width="1" height="1" fill="#1d1a19"/>`;
    }
    qr.innerHTML = `<rect width="${N}" height="${N}" fill="#fff"/>` + s + finder(0, 0) + finder(N - 7, 0) + finder(0, N - 7);
  }

  /* ── Menú móvil ─────────────────────────────────────────── */
  const nav = document.getElementById("nav");
  const toggle = document.getElementById("navToggle");
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  nav.querySelectorAll(".nav-links a").forEach((a) => a.addEventListener("click", () => nav.classList.remove("open")));

  /* ── FAQ: solo una abierta ──────────────────────────────── */
  const faqs = document.querySelectorAll(".faq details");
  faqs.forEach((d) => d.addEventListener("toggle", () => { if (d.open) faqs.forEach((o) => { if (o !== d) o.open = false; }); }));
})();
