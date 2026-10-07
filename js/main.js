/* ==========================================================
   main.js – small vanilla JS, no dependencies
   CONFIG: change the WhatsApp number / email here (digits only, with country code)
   ========================================================== */
const CONFIG = { whatsapp: "919999999999", email: "info@yourhotel.com", hotel: "Hotel Exclusive" };

/* 1. Mobile menu + sticky-header shadow */
const menuBtn = document.getElementById("menu-btn");
const menu = document.getElementById("mobile-menu");
if (menuBtn && menu) {
  menuBtn.addEventListener("click", () => {
    const open = menu.classList.toggle("hidden") === false;
    menuBtn.setAttribute("aria-expanded", open);
  });
}
const header = document.getElementById("site-header");
const onScroll = () => header && header.classList.toggle("shadow-md", window.scrollY > 10);
window.addEventListener("scroll", onScroll, { passive: true });
onScroll();

/* 2. Hero: sliding background images (auto-plays, loops) + progress bars + particles */
const slides = [...document.querySelectorAll(".slide")];
const bars = [...document.querySelectorAll(".hs-dots i")];
if (slides.length > 1 && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  let i = 0, prev = null;
  setInterval(() => {
    const cur = slides[i], next = slides[(i + 1) % slides.length];
    if (prev) { prev.style.transition = "none"; prev.classList.remove("is-prev"); void prev.offsetWidth; prev.style.transition = ""; } // reset old slide off-screen right
    cur.classList.remove("is-active"); cur.classList.add("is-prev");
    next.classList.add("is-active");
    prev = cur; i = (i + 1) % slides.length;
    bars.forEach((b, k) => b.classList.toggle("on", k === i));
  }, 6000);
}
const pBox = document.getElementById("particles");
if (pBox) for (let n = 0; n < 28; n++) {
  const s = document.createElement("span");
  s.style.cssText = `left:${Math.random() * 100}%;top:${Math.random() * 100}%;--d:${3 + Math.random() * 5}s;animation-delay:-${Math.random() * 6}s`;
  pBox.appendChild(s);
}

/* 2b. Search form: block past dates; Rooms page shows the search summary */
const sf = document.querySelector("form[data-search]");
if (sf) {
  const ci = sf.elements.checkin, co = sf.elements.checkout, today = new Date().toISOString().split("T")[0];
  ci.min = co.min = today;
  ci.addEventListener("change", () => { co.min = ci.value || today; if (co.value < co.min) co.value = ""; });
}
const sum = document.getElementById("search-summary");
if (sum) {
  const q = new URLSearchParams(location.search), parts = [];
  if (q.get("checkin")) parts.push(`${q.get("checkin")} to ${q.get("checkout") || "?"}`);
  if (q.get("adults")) parts.push(`${q.get("adults")} adult${q.get("adults") > 1 ? "s" : ""}`);
  if (parts.length) { sum.textContent = "Showing rooms for: " + parts.join(", ") + ". Pick a room and book on WhatsApp or email."; sum.hidden = false; }
}

/* 3. Booking / enquiry forms -> WhatsApp or email (no backend needed) */
document.querySelectorAll("form[data-enquiry]").forEach((form) => {
  const build = () => {
    const d = Object.fromEntries(new FormData(form));
    const lines = [`Hello ${CONFIG.hotel}, I'd like to enquire about a stay.`];
    if (d.room) lines.push(`Room: ${d.room}`);
    if (d.checkin) lines.push(`Check-in: ${d.checkin}`);
    if (d.checkout) lines.push(`Check-out: ${d.checkout}`);
    if (d.guests) lines.push(`Guests: ${d.guests}`);
    if (d.name) lines.push(`Name: ${d.name}`);
    if (d.phone) lines.push(`Phone: ${d.phone}`);
    if (d.subject) lines.push(`Subject: ${d.subject}`);
    if (d.message) lines.push(`Message: ${d.message}`);
    return lines.join("\n");
  };
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const via = e.submitter && e.submitter.value;
    const text = encodeURIComponent(build());
    if (via === "email") location.href = `mailto:${CONFIG.email}?subject=${encodeURIComponent("Booking enquiry")}&body=${text}`;
    else window.open(`https://wa.me/${CONFIG.whatsapp}?text=${text}`, "_blank", "noopener");
  });
  // Prevent past dates; check-out must follow check-in
  const ci = form.querySelector('[name="checkin"]'), co = form.querySelector('[name="checkout"]');
  if (ci && co) {
    const today = new Date().toISOString().split("T")[0];
    ci.min = co.min = today;
    ci.addEventListener("change", () => { co.min = ci.value || today; if (co.value < co.min) co.value = ""; });
  }
});

document.addEventListener("DOMContentLoaded", () => {

  const items = document.querySelectorAll("[data-gallery-item]");
  const filters = document.querySelectorAll("[data-filter]");
  const lightbox = document.getElementById("lightbox");

  /* =========================
     GALLERY FILTER
     ========================= */

  filters.forEach((button) => {

    button.addEventListener("click", function () {

      const selectedCategory = this.getAttribute("data-filter");

      /* Active button */
      filters.forEach((btn) => {
        btn.setAttribute("aria-pressed", "false");
      });

      this.setAttribute("aria-pressed", "true");

      /* Show / hide photos */
      items.forEach((item) => {

        const itemCategory = item.getAttribute("data-cat");

        if (
          selectedCategory === "all" ||
          itemCategory === selectedCategory
        ) {
          item.hidden = false;
          item.style.display = "";
        } else {
          item.hidden = true;
          item.style.display = "none";
        }

      });

    });

  });


  /* =========================
     LIGHTBOX
     ========================= */

  if (!lightbox || !items.length) return;

  const lightboxImage = lightbox.querySelector("img");
  const caption = lightbox.querySelector("p");
  const previousButton = lightbox.querySelector("[data-prev]");
  const nextButton = lightbox.querySelector("[data-next]");
  const closeButton = lightbox.querySelector("[data-close]");

  let visibleItems = [];
  let currentIndex = 0;


  function updateVisibleItems() {
    visibleItems = [...items].filter((item) => {
      return !item.hidden;
    });
  }


  function showImage(index) {

    updateVisibleItems();

    if (!visibleItems.length) return;

    currentIndex =
      (index + visibleItems.length) % visibleItems.length;

    const item = visibleItems[currentIndex];

    lightboxImage.src = item.getAttribute("data-full");
    lightboxImage.alt = item.getAttribute("data-caption") || "";

    caption.textContent =
      `${item.getAttribute("data-caption") || ""} (${currentIndex + 1}/${visibleItems.length})`;
  }


  /* Open lightbox */
  items.forEach((item) => {

    item.addEventListener("click", () => {

      updateVisibleItems();

      currentIndex = visibleItems.indexOf(item);

      showImage(currentIndex);

      lightbox.showModal();

    });

  });


  /* Previous */
  previousButton.addEventListener("click", () => {
    showImage(currentIndex - 1);
  });


  /* Next */
  nextButton.addEventListener("click", () => {
    showImage(currentIndex + 1);
  });


  /* Close */
  closeButton.addEventListener("click", () => {
    lightbox.close();
  });


  /* Close by clicking outside */
  lightbox.addEventListener("click", (event) => {

    if (event.target === lightbox) {
      lightbox.close();
    }

  });


  /* Keyboard */
  lightbox.addEventListener("keydown", (event) => {

    if (event.key === "ArrowLeft") {
      showImage(currentIndex - 1);
    }

    if (event.key === "ArrowRight") {
      showImage(currentIndex + 1);
    }

    if (event.key === "Escape") {
      lightbox.close();
    }

  });

});