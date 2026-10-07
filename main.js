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

/* 4. Gallery: category filter + lightbox */
const items = [...document.querySelectorAll("[data-gallery-item]")];
const lb = document.getElementById("lightbox");
if (items.length && lb) {
  const img = lb.querySelector("img"), cap = lb.querySelector("p");
  let cur = 0, visible = items;
  const show = (n) => {
    cur = (n + visible.length) % visible.length;
    img.src = visible[cur].dataset.full;
    img.alt = visible[cur].dataset.caption;
    cap.textContent = `${visible[cur].dataset.caption} (${cur + 1}/${visible.length})`;
  };
  items.forEach((el) => el.addEventListener("click", () => { visible = items.filter((x) => !x.hidden); show(visible.indexOf(el)); lb.showModal(); }));
  lb.querySelector("[data-prev]").onclick = () => show(cur - 1);
  lb.querySelector("[data-next]").onclick = () => show(cur + 1);
  lb.querySelector("[data-close]").onclick = () => lb.close();
  lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); }); // click backdrop
  lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(cur - 1); if (e.key === "ArrowRight") show(cur + 1); });
  document.querySelectorAll("[data-filter]").forEach((b) => b.addEventListener("click", () => {
    document.querySelectorAll("[data-filter]").forEach((x) => x.setAttribute("aria-pressed", x === b));
    items.forEach((it) => (it.hidden = b.dataset.filter !== "all" && it.dataset.cat !== b.dataset.filter));
  }));
}

/* 5. Footer year */
document.querySelectorAll("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));

/* 6. Quick booking: live stay pass (room, dates, nights, total) */
const qb = document.querySelector(".qb");
if (qb) {
  const o = (k) => qb.querySelector(`[data-o="${k}"]`);
  const money = (n) => "₹" + n.toLocaleString("en-IN");   // change ₹ for another currency
  const fmt = (d) => new Date(d).toLocaleDateString("en-GB", { day: "numeric", month: "short" });
  let guests = 2;
  const update = () => {
    const r = qb.querySelector('input[name="room"]:checked');
    const a = qb.elements.checkin.value, b = qb.elements.checkout.value;
    const nights = a && b ? Math.max(0, Math.round((new Date(b) - new Date(a)) / 864e5)) : 0;
    const total = r && nights ? nights * Number(r.dataset.price) : 0;
    o("room").textContent = r ? r.value : "Not chosen yet";
    o("dates").textContent = nights ? `${fmt(a)} to ${fmt(b)}` : "Pick your dates";
    o("nights").textContent = nights;
    o("guests").textContent = qb.elements.guests.value = `${guests} guest${guests > 1 ? "s" : ""}`;
    const t = o("total"), prev = t.textContent;
    t.textContent = money(total);
    if (prev !== t.textContent) { t.classList.add("is-bump"); setTimeout(() => t.classList.remove("is-bump"), 250); }
    qb.elements.message.value = total ? `Estimated total: ${money(total)} for ${nights} night${nights > 1 ? "s" : ""}` : "";
  };
  qb.addEventListener("input", update);
  qb.addEventListener("change", update);
  qb.querySelectorAll("[data-step]").forEach((btn) => btn.addEventListener("click", () => {
    guests = Math.min(6, Math.max(1, guests + Number(btn.dataset.step)));
    update();
  }));
}
