/* Rellena los datos del titular y de la marca en las páginas legales desde ../brand.js */
(function () {
  const B = window.BRAND || {};
  const L = B.legal || {};
  const theme = new URLSearchParams(location.search).get("theme") || B.theme;
  if (theme && theme !== "fiesta") document.documentElement.setAttribute("data-theme", theme);

  const map = {
    "brand": B.name,
    "domain": B.domain,
    "titular": L.titular,
    "nif": L.nif,
    "domicilio": L.domicilio,
    "registro": L.registro,
    "telefono": L.telefono,
    "actualizado": L.actualizado,
    "free": B.freePhotos
  };
  Object.entries(map).forEach(([k, v]) => {
    if (v === undefined) return;
    document.querySelectorAll(`[data-l="${k}"]`).forEach((el) => (el.textContent = v));
  });
  document.querySelectorAll("[data-l='email']").forEach((el) => {
    el.textContent = L.email || B.email;
    if (el.tagName === "A") el.href = "mailto:" + (L.email || B.email);
  });
  document.querySelectorAll("[data-l='web']").forEach((el) => {
    el.textContent = "https://" + B.domain;
    if (el.tagName === "A") el.href = "https://" + B.domain;
  });
  const y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Marca la página actual en la navegación legal
  const here = location.pathname.split("/").pop();
  document.querySelectorAll(".legal-nav a").forEach((a) => {
    if (a.getAttribute("href") === here) a.classList.add("active");
  });
})();
