/* Páginas públicas: marca, tema, menú móvil, FAQ, formulario de contacto */
(function () {
  const B = window.BRAND || {};
  const theme = new URLSearchParams(location.search).get("theme") || B.theme;
  if (theme && theme !== "fiesta") document.documentElement.setAttribute("data-theme", theme);
  document.querySelectorAll("[data-brand]").forEach((el) => (el.textContent = B.name));
  document.querySelectorAll("[data-brand-tagline]").forEach((el) => (el.textContent = B.tagline + "."));
  document.querySelectorAll("[data-brand-city]").forEach((el) => (el.textContent = B.city));
  document.querySelectorAll("[data-brand-email]").forEach((el) => { el.textContent = B.email; el.href = "mailto:" + B.email; });
  document.querySelectorAll("[data-brand-whatsapp]").forEach((el) => { el.textContent = "WhatsApp " + B.whatsapp; el.href = "https://wa.me/" + B.whatsapp.replace(/\D/g, ""); });
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
      const body = `${msg}\n\n— ${name}\n${email}`;
      return { subject, body };
    };
    form.addEventListener("submit", (e) => { e.preventDefault(); const c = compose(); if (!c) return; location.href = `mailto:${(B.legal && B.legal.email) || B.email}?subject=${encodeURIComponent(c.subject)}&body=${encodeURIComponent(c.body)}`; });
    document.getElementById("sendWa").addEventListener("click", () => { const c = compose(); if (!c) return; window.open(`https://wa.me/${B.whatsapp.replace(/\D/g, "")}?text=${encodeURIComponent(c.subject + "\n" + c.body)}`, "_blank", "noopener"); });
  }
})();

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
