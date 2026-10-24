/*
 * Configuración de marca.
 * Cambia aquí el nombre, el eslogan y los datos de contacto:
 * todo el sitio se actualiza automáticamente (textos con data-brand,
 * <title>, meta description y pie de página).
 */
window.BRAND = {
  name: "Fiestalia",            // ← nombre de tu marca
  tagline: "El álbum de tu evento, hecho por tus invitados",
  domain: "fiestalia.com",       // ← tu dominio
  email: "hola@fiestalia.com",   // ← correo de contacto
  whatsapp: "+34 634 11 85 79",   // teléfono / WhatsApp
  city: "Madrid, España",
  // Tema de color: "fiesta" (coral/violeta del logo), "oro" (marfil y oro), "negro" (negro y oro),
  // "esmeralda" (esmeralda y oro), "burdeos" (burdeos y champán), "medianoche" (azul noche y oro),
  // "noche" (fondo oscuro de gala) o "rosa" (rosa cuarzo nupcial).
  // Para previsualizar sin cambiar esto: index.html?theme=oro
  theme: "burdeos",   // Burdeos y Oro (tema elegido)
  freePhotos: 50,                // fotos gratis por álbum
  // Precios en euros, pago único (IVA incluido). Ajusta a tu estrategia.
  plans: [
    { id: "gratis",      name: "Gratis",      price: 0,  photos: 50,   gb: 0.5, guests: 2,   liveWall: false, selfie: true,  months: 1  },
    { id: "basico",      name: "Básico",      price: 19, photos: 500,  gb: 5,   guests: 20,  liveWall: false, selfie: true,  months: 6  },
    { id: "celebracion", name: "Celebración", price: 39, photos: 1500, gb: 20,  guests: 60,  liveWall: true,  selfie: true,  months: 12, featured: true },
    { id: "gran-evento", name: "Gran evento", price: 69, photos: 5000, gb: 60,  guests: 200, liveWall: true,  selfie: true,  months: 24 }
  ],
  // Fotos estimadas por invitado (para el calculador de planes)
  photosPerGuest: 25
};
