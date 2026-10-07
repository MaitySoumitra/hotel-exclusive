"""
build.py – OPTIONAL helper that writes the static HTML pages + placeholder images.
You do NOT need Python to maintain the site: the generated .html files are plain HTML
and can be edited directly. Run `python3 build.py` only if you want to regenerate everything.
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

# ---------- EDIT ME: brand details ----------
BRAND = "Hotel Exclusive"
TAGLINE = "Quiet rooms, warm service, a short walk from everything."
WA = "919999999999"                 # WhatsApp number, digits only, with country code
EMAIL = "info@yourhotel.com"
PHONE = "+91 99999 99999"
ADDR = "Your Street Address, City, Country"
SITE = "https://www.yourhotel.com"  # used for canonical + social tags
CUR = "₹"
MAPQ = "Kolkata, West Bengal, India"  # Google Maps search text for the embedded map

# ---------- Content ----------
ROOMS = [
 dict(slug="standard-twin-loft", name="Standard Twin Loft", cat="Standard", price=1500, size=13, guests=2, bed="Twin loft beds",
      short="Two-level loft beds with a private bathroom. Smart and affordable for friends or siblings.",
      long="Two separate sleeping levels give each guest privacy: a 4 ft lower bed and a 3 ft loft bed reached by a ladder. A private bathroom, fast Wi-Fi and air conditioning keep short stays easy.",
      am=["wifi","ac","tv","coffee","key","shower"]),
 dict(slug="standard-double", name="Standard Double", cat="Standard", price=1900, size=15, guests=2, bed="Double bed",
      short="A calm, compact room with a 5 ft double bed and a small work corner.",
      long="Designed for couples and solo travellers who want a quiet base. Expect a comfortable 5 ft bed, blackout curtains, a work desk, and a private bathroom with hot shower.",
      am=["wifi","ac","tv","desk","key","shower"]),
 dict(slug="deluxe-queen", name="Deluxe Queen", cat="Deluxe", price=2400, size=20, guests=2, bed="Queen bed",
      short="Extra floor space, a queen bed and a proper desk for working remotely.",
      long="At 20 sqm this room has space to unpack. A queen bed, a dedicated work desk, mini fridge and tea/coffee station make it a favourite for week-long stays.",
      am=["wifi","ac","tv","desk","fridge","coffee"]),
 dict(slug="deluxe-courtyard", name="Deluxe Courtyard", cat="Deluxe", price=2800, size=20, guests=2, bed="Queen bed",
      short="Quiet courtyard-facing room with softer lighting and extra storage.",
      long="Facing the inner courtyard, this room is the quietest in the hotel. Warm lighting, a queen bed, wardrobe space and a rainfall shower round out the stay.",
      am=["wifi","ac","tv","fridge","laundry","shower"]),
 dict(slug="family-bunk-room", name="Family Bunk Room", cat="Family", price=3200, size=27, guests=4, bed="Two bunk beds",
      short="Sleeps four with sturdy bunk beds and a shared lounge corner.",
      long="Ideal for families or small groups. Two sturdy bunk beds, a seating corner, ample luggage space and a large bathroom with shower.",
      am=["wifi","ac","tv","laundry","key","shower"]),
 dict(slug="executive-suite", name="Executive Suite", cat="Suite", price=4500, size=37, guests=3, bed="King bed + sofa bed",
      short="Our largest room: king bed, sofa bed, lounge area and city views.",
      long="Spacious and light, with a king bed, a sofa bed for a third guest, a seating area, mini fridge and a full-size desk. Priority housekeeping and late check-out on request.",
      am=["wifi","ac","tv","desk","fridge","coffee"]),
]
AMEN = {
 "wifi":("Free Wi-Fi","Fast fibre internet in every room",'<path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19" r="1"/>'),
 "ac":("Air conditioning","Individual climate control",'<path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9"/>'),
 "tv":("Smart TV","Streaming-ready screens",'<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8"/>'),
 "desk24":("24-hour front desk","Help any time, day or night",'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 "coffee":("Tea & coffee","Complimentary in-room station",'<path d="M5 9h11v5a4 4 0 0 1-4 4H9a4 4 0 0 1-4-4zM16 10h2a2 2 0 0 1 0 4h-2M8 3v3M12 3v3"/>'),
 "key":("Keycard security","CCTV and keycard access",'<circle cx="8" cy="12" r="4"/><path d="M12 12h9M18 12v3"/>'),
 "shower":("Hot shower","Private bathroom with hot water",'<path d="M6 20v-9a5 5 0 0 1 10 0M4 11h14M8 15v1M12 15v1M16 15v1"/>'),
 "laundry":("Laundry","Wash and dry on request",'<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="13" r="4"/>'),
 "fridge":("Mini fridge","Cold drinks in your room",'<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M6 10h12M9 6v1M9 13v2"/>'),
 "desk":("Work desk","A proper desk and good light",'<path d="M3 9h18M5 9v10M19 9v10M9 9v5h6V9"/>'),
 "parking":("Parking","Secure on-site parking",'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M10 16V8h3a2.5 2.5 0 0 1 0 5h-3"/>'),
 "shield":("Housekeeping","Daily cleaning included",'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>'),
}
HOME_AM = ["wifi","ac","tv","desk24","coffee","key","laundry","parking"]
GAL = [("hotel","Lobby and reception"),("room","Deluxe Queen bedroom"),("hotel","Staircase and corridor"),("amenities","Breakfast and coffee corner"),
       ("room","Bathroom"),("surroundings","Street outside the hotel"),("hotel","Lounge seating"),("room","Executive Suite"),
       ("amenities","Laundry corner"),("hotel","Entrance"),("room","Standard Double"),("surroundings","Nearby market")]
REVIEWS = [("The quietest room I've booked in the city, and the team replied on WhatsApp within minutes.","Sample guest, London"),
           ("Clean, simple and exactly as pictured. Easy to walk to dinner and the station.","Sample guest, New York"),
           ("Late check-in was no problem at all. We would happily stay again.","Sample guest, Tokyo")]

# ---------- Placeholder images (replace with real photos, keep same file names) ----------
PALS = [("#cfd8d2","#7f9a93"),("#e4dccb","#b79f74"),("#d5dde3","#7d93a3"),("#e0d3cf","#a98279"),("#d3dcc9","#8aa070"),("#d9d3e0","#8f82a6")]
def ph(name, w, h, i, label):
    a, b = PALS[i % len(PALS)]
    img = Image.new("RGB", (w, h), a); d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h; c = tuple(int(int(a[k:k+2],16)*(1-t) + int(b[k:k+2],16)*t) for k in (1,3,5)); d.line([(0,y),(w,y)], fill=c)
    d.ellipse([w*.55, h*.1, w*1.1, h*.8], fill=tuple(min(255,x+18) for x in c))
    d.rectangle([w*.08, h*.62, w*.55, h*.9], fill=tuple(max(0,x-28) for x in c))
    try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", max(14, w//40))
    except Exception: f = ImageFont.load_default()
    d.text((w*.05, h*.05), f"Placeholder – replace {name}.jpg  |  {label}", fill="#ffffff", font=f)
    img.save(f"images/{name}.jpg", quality=72, optimize=True, progressive=True)

os.makedirs("images", exist_ok=True)
_hero_png = True
for n in range(1,4): ph(f"hero-{n}", 1920, 1080, n, "hero 1920x1080")
for i, r in enumerate(ROOMS): ph(f"room-{i+1}", 1200, 800, i, r["name"])
for i, (c, cap) in enumerate(GAL):
    h = 1000 if i % 3 == 0 else 700
    ph(f"gallery-{i+1}", 1200, int(1200*h/800), i, cap); ph(f"gallery-{i+1}-t", 640, h, i, cap)
[Image.open(f"images/hero-{n}.jpg").save(f"images/hero-{n}.png", optimize=True) for n in (1,2,3)]
ph("about", 1000, 1200, 2, "about image"); ph("og-image", 1200, 630, 0, "social share image")

# ---------- Helpers ----------
def icon(k, cls="h-6 w-6"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{AMEN[k][2]}</svg>'
def img(src, alt, w, h, cls="", eager=False):
    return f'<img src="images/{src}" alt="{alt}" width="{w}" height="{h}" class="{cls}" {"fetchpriority=\"high\"" if eager else "loading=\"lazy\""} decoding="async">'
def money(n): return f"{CUR}{n:,}"
WA_LINK = f"https://wa.me/{WA}?text=Hello%20{BRAND.replace(' ','%20')}%2C%20I%27d%20like%20to%20book%20a%20room."
WA_ICON = '<svg class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15l-1.4 5 5.1-1.3A10 10 0 1 0 12 2zm5.2 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.4.6c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.1 1 2 1.3 2.3 1.4.3.1.4.1.6-.1l.8-1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.4.1.2.1.8-.1 1.3z"/></svg>'
NAV = [("index.html","Home"),("rooms.html","Rooms"),("amenities.html","Amenities"),("gallery.html","Gallery"),("contact.html","Contact")]

def page(fname, title, desc, body, active="", ld=None, og="og-image.jpg"):
    links = "".join(f'<a href="{h}" class="rounded-full px-3 py-2 text-sm font-medium hover:text-brass {"text-brass" if h==active else "text-ink"}" {"aria-current=\"page\"" if h==active else ""}>{t}</a>' for h,t in NAV)
    mlinks = "".join(f'<a href="{h}" class="block rounded-lg px-3 py-3 text-ink hover:bg-mist">{t}</a>' for h,t in NAV)
    fl = "".join(f'<li><a class="hover:text-white" href="{h}">{t}</a></li>' for h,t in NAV)
    ldj = f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{fname}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/images/{og}"><meta name="theme-color" content="#12302f">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:opsz,wght@9..144,400;9..144,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
{ldj}
</head>
<body>
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:bg-white focus:p-3">Skip to content</a>
<!-- Sticky navigation -->
<header id="site-header" class="sticky top-0 z-40 bg-white/95 backdrop-blur transition-shadow">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-5 py-3">
    <a href="index.html" class="font-display text-xl font-semibold text-ink">{BRAND}</a>
    <nav class="hidden items-center gap-1 md:flex" aria-label="Main">{links}</nav>
    <div class="flex items-center gap-2">
      <a href="rooms.html" class="btn btn-primary hidden !py-2 sm:inline-flex">Book Now</a>
      <button id="menu-btn" class="rounded-lg p-2 text-ink md:hidden" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu">
        <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
  <nav id="mobile-menu" class="hidden border-t border-slate-100 px-5 pb-4 md:hidden" aria-label="Mobile">{mlinks}<a href="rooms.html" class="btn btn-primary mt-2 w-full">Book Now</a></nav>
</header>
<main id="main">
{body}
</main>
<!-- Floating WhatsApp button -->
<a href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp" class="btn-wa fixed bottom-5 right-5 z-40 flex h-14 w-14 items-center justify-center rounded-full shadow-lg transition hover:scale-105">{WA_ICON}</a>
<footer class="bg-ink text-white/80">
  <div class="mx-auto grid max-w-6xl gap-10 px-5 py-14 md:grid-cols-4">
    <div class="md:col-span-2"><p class="font-display text-2xl text-white">{BRAND}</p><p class="mt-3 max-w-sm text-sm">{TAGLINE}</p></div>
    <div><p class="font-display text-lg text-white">Explore</p><ul class="mt-3 space-y-2 text-sm">{fl}</ul></div>
    <div><p class="font-display text-lg text-white">Reach us</p>
      <address class="mt-3 space-y-2 text-sm not-italic"><p>{ADDR}</p><p><a class="hover:text-white" href="tel:{PHONE.replace(' ','')}">{PHONE}</a></p>
      <p><a class="hover:text-white" href="mailto:{EMAIL}">{EMAIL}</a></p><p><a class="hover:text-white" href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp us</a></p></address></div>
  </div>
  <p class="border-t border-white/10 py-5 text-center text-xs">© <span data-year>2026</span> {BRAND}. All rights reserved.</p>
</footer>
<script src="js/main.js" defer></script>
</body>
</html>'''
    open(fname, "w", encoding="utf-8").write(html)

def room_card(i, r, h="h3"):
    return f'''<article class="group overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm">
  <a href="{r["slug"]}.html" class="block overflow-hidden">{img(f"room-{i+1}.jpg", f'{r["name"]} bedroom', 600, 400, "aspect-[3/2] w-full object-cover transition duration-500 group-hover:scale-105")}</a>
  <div class="p-5"><{h} class="text-xl"><a href="{r["slug"]}.html">{r["name"]}</a></{h}>
  <p class="mt-1 text-sm text-slate-500">{r["size"]} sqm · up to {r["guests"]} guests · {r["bed"]}</p>
  <p class="mt-3 text-sm">{r["short"]}</p>
  <div class="mt-4 flex items-center justify-between"><p><span class="text-lg font-semibold text-brass">{money(r["price"])}</span> <span class="text-sm text-slate-500">per night</span></p>
  <a href="{r["slug"]}.html" class="text-sm font-semibold text-ink underline underline-offset-4">View room</a></div></div></article>'''

def amen_tile(k):
    return f'<li class="flex items-start gap-4 rounded-2xl bg-mist p-5"><span class="rounded-full bg-white p-3 text-ink">{icon(k)}</span><div><p class="font-semibold text-ink">{AMEN[k][0]}</p><p class="text-sm">{AMEN[k][1]}</p></div></li>'

def enquiry_form(room=None, compact=False):
    r = f'<input type="hidden" name="room" value="{room}">' if room else ""
    return f'''<form data-enquiry class="grid gap-3 {"" if compact else "sm:grid-cols-2 lg:grid-cols-4 lg:items-end"}">{r}
  <label class="text-sm font-medium text-ink">Check-in<input class="field mt-1" type="date" name="checkin" required></label>
  <label class="text-sm font-medium text-ink">Check-out<input class="field mt-1" type="date" name="checkout" required></label>
  <label class="text-sm font-medium text-ink">Guests<select class="field mt-1" name="guests"><option>1 guest</option><option selected>2 guests</option><option>3 guests</option><option>4+ guests</option></select></label>
  <div class="flex flex-wrap gap-2 {"pt-1" if compact else ""}"><button class="btn btn-wa flex-1" name="via" value="wa">{WA_ICON} Book on WhatsApp</button><button class="btn btn-primary" name="via" value="email">Email</button></div></form>'''

# ---------- HOME ----------
slides = "".join(f'<img src="images/hero-{n}.png" alt="" width="1920" height="1080" class="slide absolute inset-0 h-full w-full object-cover {"is-active" if n==1 else ""}" {"fetchpriority=\"high\"" if n==1 else "loading=\"lazy\""} decoding="async">' for n in (1,2,3))
home = f'''
<section class="relative isolate flex min-h-[92vh] items-center overflow-hidden bg-[#050b14]" aria-label="Welcome">
  <div class="absolute inset-0 -z-10 overflow-hidden" aria-hidden="true">{slides}
    <div class="absolute inset-0 bg-gradient-to-r from-[#050b14]/90 via-[#050b14]/55 to-[#050b14]/10"></div>
    <div class="absolute inset-0 bg-gradient-to-t from-[#050b14]/85 via-transparent to-transparent"></div>
    <div class="beam"></div><div class="horizon"></div><div id="particles"></div>
    <span class="drone" style="top:16%;animation-duration:30s"></span><span class="drone" style="top:30%;animation-duration:44s;animation-delay:-14s;scale:.7"></span><span class="drone" style="top:9%;animation-duration:38s;animation-delay:-26s;scale:.5"></span>
  </div>
  <div class="mx-auto grid w-full max-w-6xl gap-10 px-5 pb-12 pt-16 lg:grid-cols-5 lg:items-center">
    <div class="text-white lg:col-span-3">
      <h1 class="font-display text-5xl font-semibold leading-none !text-white sm:text-7xl">Hotel <span class="text-[#22b8ff]">Booking</span></h1>
      <p class="mt-4 text-xl text-white/90 sm:text-2xl">Future stays, extraordinary experiences</p>
      <form action="rooms.html" method="get" data-search role="search" aria-label="Search rooms" class="mt-8 flex flex-col gap-1 rounded-3xl bg-white p-2 shadow-2xl sm:flex-row sm:items-center sm:rounded-full">
        <label class="flex flex-1 items-center gap-3 rounded-full px-4 py-2 focus-within:ring-2 focus-within:ring-[#1d8fff] "><svg class="h-5 w-5 shrink-0 text-ink" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg><span class="block w-full"><span class="block text-sm font-semibold text-ink">Where to?</span><input type="text" name="where" class="w-full bg-transparent text-xs text-slate-600 placeholder:text-slate-400 focus:outline-none" placeholder="City, hotel or destination"></span></label>
        <label class="flex flex-1 items-center gap-3 rounded-full px-4 py-2 focus-within:ring-2 focus-within:ring-[#1d8fff] sm:border-l sm:border-slate-200"><svg class="h-5 w-5 shrink-0 text-ink" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg><span class="block w-full"><span class="block text-sm font-semibold text-ink">Check In</span><input type="date" name="checkin" class="w-full bg-transparent text-xs text-slate-600 placeholder:text-slate-400 focus:outline-none" placeholder="Select date"></span></label>
        <label class="flex flex-1 items-center gap-3 rounded-full px-4 py-2 focus-within:ring-2 focus-within:ring-[#1d8fff] sm:border-l sm:border-slate-200"><svg class="h-5 w-5 shrink-0 text-ink" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/></svg><span class="block w-full"><span class="block text-sm font-semibold text-ink">Check Out</span><input type="date" name="checkout" class="w-full bg-transparent text-xs text-slate-600 placeholder:text-slate-400 focus:outline-none" placeholder="Select date"></span></label>
        <button type="submit" class="btn bg-[#1d8fff] px-8 text-white hover:bg-[#0f74d6]"><svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>Search</button>
      </form>
      <ul class="mt-10 grid grid-cols-2 gap-5 sm:grid-cols-4"><li class="flex items-center gap-3"><svg class="h-8 w-8 shrink-0 text-[#7fd0ff]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h12l3 6-9 12L3 9z"/></svg><span><span class="block text-sm font-semibold">Smart rooms</span><span class="block text-xs text-white/70">Easy in-room controls</span></span></li><li class="flex items-center gap-3"><svg class="h-8 w-8 shrink-0 text-[#7fd0ff]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 21V4h9v17M14 9h5v12M8 8h3M8 12h3M8 16h3"/></svg><span><span class="block text-sm font-semibold">Prime location</span><span class="block text-xs text-white/70">Close to everything</span></span></li><li class="flex items-center gap-3"><svg class="h-8 w-8 shrink-0 text-[#7fd0ff]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19" r="1"/></svg><span><span class="block text-sm font-semibold">Fast check-in</span><span class="block text-xs text-white/70">Contactless on arrival</span></span></li><li class="flex items-center gap-3"><svg class="h-8 w-8 shrink-0 text-[#7fd0ff]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-9 5-14 15-14 0 10-5 15-14 15M5 19c3-5 6-8 10-10"/></svg><span><span class="block text-sm font-semibold">Sustainable stays</span><span class="block text-xs text-white/70">Greener choices</span></span></li></ul>
    </div>
    <aside class="holo hidden p-5 text-sm text-white lg:col-span-2 lg:block lg:justify-self-end" aria-hidden="true"><p class="mb-2 font-semibold text-[#7fd0ff]">AI Room Control</p><ul><li class="flex items-center justify-between gap-6 border-t border-white/10 py-3 first:border-0"><span class="flex items-center gap-3"><span class="h-2.5 w-2.5 rounded-full bg-[#22b8ff]"></span>Lighting</span><span class="tg" style="animation-delay:0s"></span></li><li class="flex items-center justify-between gap-6 border-t border-white/10 py-3 first:border-0"><span class="flex items-center gap-3"><span class="h-2.5 w-2.5 rounded-full bg-[#22b8ff]"></span>Temperature</span><span class="tg" style="animation-delay:1.2s"></span></li><li class="flex items-center justify-between gap-6 border-t border-white/10 py-3 first:border-0"><span class="flex items-center gap-3"><span class="h-2.5 w-2.5 rounded-full bg-[#22b8ff]"></span>Curtains</span><span class="tg" style="animation-delay:2.4s"></span></li><li class="flex items-center justify-between gap-6 border-t border-white/10 py-3 first:border-0"><span class="flex items-center gap-3"><span class="h-2.5 w-2.5 rounded-full bg-[#22b8ff]"></span>Entertainment</span><span class="tg" style="animation-delay:3.6s"></span></li></ul></aside>
  </div>
</section>

<section class="section grid items-center gap-12 md:grid-cols-2" aria-labelledby="about-h">
  <div><h2 id="about-h" class="text-3xl md:text-4xl">Simple, thoughtful stays</h2>
  <p class="mt-5">We keep things easy: clean rooms, fair prices and people who answer quickly. Whether you are here for a weekend or a month, you get a comfortable bed, fast Wi-Fi and a front desk that is always open.</p>
  <dl class="mt-8 grid grid-cols-3 gap-4 border-t border-slate-100 pt-6 text-center">
    <div><dt class="text-sm text-slate-500">Rooms</dt><dd class="font-display text-3xl text-ink">30+</dd></div>
    <div><dt class="text-sm text-slate-500">Guest rating</dt><dd class="font-display text-3xl text-ink">4.8</dd></div>
    <div><dt class="text-sm text-slate-500">Front desk</dt><dd class="font-display text-3xl text-ink">24/7</dd></div></dl></div>
  {img("about.jpg","Hotel lounge and reception",800,960,"mx-auto aspect-[5/6] w-full max-w-md rounded-[2rem] object-cover md:ml-auto")}
</section>

<section class="bg-mist" aria-labelledby="rooms-h"><div class="section">
  <div class="flex flex-wrap items-end justify-between gap-4"><h2 id="rooms-h" class="text-3xl md:text-4xl">Rooms for every kind of stay</h2><a href="rooms.html" class="btn btn-primary">All rooms</a></div>
  <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">{"".join(room_card(i,r) for i,r in list(enumerate(ROOMS))[:3])}</div></div></section>

<section class="section" aria-labelledby="am-h"><h2 id="am-h" class="text-3xl md:text-4xl">Everything you need, included</h2>
  <ul class="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{"".join(amen_tile(k) for k in HOME_AM)}</ul></section>

<section class="bg-mist" aria-labelledby="gal-h"><div class="section">
  <div class="flex flex-wrap items-end justify-between gap-4"><h2 id="gal-h" class="text-3xl md:text-4xl">A look around</h2><a href="gallery.html" class="btn btn-primary">Open gallery</a></div>
  <div class="mt-10 grid grid-cols-2 gap-3 md:grid-cols-4">{"".join(f'<a href="gallery.html">{img(f"gallery-{n}-t.jpg", GAL[n-1][1], 640, 700, "aspect-square w-full rounded-2xl object-cover")}</a>' for n in (1,2,3,4))}</div></div></section>

<section class="section" aria-labelledby="rev-h"><h2 id="rev-h" class="text-3xl md:text-4xl">What guests say</h2>
  <div class="mt-10 grid gap-6 md:grid-cols-3">{"".join(f'<figure class="rounded-2xl border border-slate-100 p-6"><blockquote class="text-slate-700">“{q}”</blockquote><figcaption class="mt-4 text-sm font-semibold text-ink">{a}</figcaption></figure>' for q,a in REVIEWS)}</div></section>

<section class="mx-auto max-w-6xl px-5 pb-20"><div class="rounded-3xl bg-ink px-6 py-12 text-center text-white md:px-12">
  <h2 class="font-display text-3xl !text-white md:text-4xl">Ready to book?</h2><p class="mx-auto mt-3 max-w-lg text-white/80">Send us your dates and we will reply with availability and the best direct rate.</p>
  <div class="mt-6 flex flex-wrap justify-center gap-3"><a href="{WA_LINK}" target="_blank" rel="noopener" class="btn btn-wa">{WA_ICON} WhatsApp us</a><a href="mailto:{EMAIL}" class="btn btn-ghost">Email us</a></div></div></section>'''
ld = {"@context":"https://schema.org","@type":"Hotel","name":BRAND,"description":TAGLINE,"url":SITE,"telephone":PHONE,"email":EMAIL,"address":ADDR,"image":f"{SITE}/images/og-image.jpg","priceRange":f"{CUR}{ROOMS[0]['price']}+"}
page("index.html", f"{BRAND} – Rooms, amenities and direct booking", f"Book a comfortable room at {BRAND}. Free Wi-Fi, 24-hour front desk and direct booking by WhatsApp or email.", home, "index.html", ld)

# ---------- ROOMS ----------
rows = "".join(f'<tr class="border-t border-slate-100"><th scope="row" class="py-3 pr-4 text-left font-medium text-ink"><a href="{r["slug"]}.html">{r["name"]}</a></th><td class="py-3 pr-4">{r["cat"]}</td><td class="py-3 pr-4">{r["guests"]}</td><td class="py-3 text-right font-semibold text-brass">{money(r["price"])}</td></tr>' for r in ROOMS)
rlist = "".join(f'''<article class="grid overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-sm md:grid-cols-5">
  <a href="{r["slug"]}.html" class="md:col-span-2">{img(f"room-{i+1}.jpg", r["name"]+" bedroom", 600, 400, "h-full min-h-56 w-full object-cover")}</a>
  <div class="p-6 md:col-span-3"><div class="flex flex-wrap items-start justify-between gap-2"><h2 class="text-2xl"><a href="{r["slug"]}.html">{r["name"]}</a></h2>
  <p class="text-right"><span class="text-xl font-semibold text-brass">{money(r["price"])}</span><br><span class="text-xs text-slate-500">per night</span></p></div>
  <p class="mt-2 text-sm text-slate-500">{r["cat"]} · {r["size"]} sqm · up to {r["guests"]} guests · {r["bed"]}</p><p class="mt-3">{r["short"]}</p>
  <ul class="mt-4 flex flex-wrap gap-2" aria-label="Amenities">{"".join(f'<li class="flex items-center gap-1 rounded-full bg-mist px-3 py-1 text-xs text-ink">{icon(k,"h-4 w-4")}{AMEN[k][0]}</li>' for k in r["am"][:4])}</ul>
  <a href="{r["slug"]}.html" class="btn btn-primary mt-5">View details</a></div></article>''' for i,r in enumerate(ROOMS))
rooms = f'''<section class="bg-mist"><div class="mx-auto max-w-6xl px-5 py-14"><h1 class="text-4xl md:text-5xl">Rooms and suites</h1><p class="mt-3 max-w-xl">Choose a room, then book directly on WhatsApp or by email. Prices shown per night.</p></div></section>
<div class="section space-y-6"><p id="search-summary" hidden class="rounded-2xl bg-mist p-4 text-sm text-ink"></p>{rlist}
<section aria-labelledby="price-h" class="pt-10"><h2 id="price-h" class="text-3xl">Rate card</h2>
<p class="mt-2 text-sm text-slate-500">Placeholder table: edit the rows in rooms.html when final seasonal prices are ready.</p>
<div class="mt-5 overflow-x-auto"><table class="w-full min-w-[32rem] text-sm"><thead><tr class="text-left text-slate-500"><th class="pb-3">Room</th><th class="pb-3">Type</th><th class="pb-3">Guests</th><th class="pb-3 text-right">From, per night</th></tr></thead><tbody>{rows}</tbody></table></div></section></div>'''
page("rooms.html", f"Rooms and suites | {BRAND}", f"Browse every room at {BRAND}: sizes, beds, amenities and nightly rates.", rooms, "rooms.html")

# ---------- ROOM DETAIL (one file per room) ----------
for i, r in enumerate(ROOMS):
    others = [(j,x) for j,x in enumerate(ROOMS) if j != i][:3]
    body = f'''<section class="mx-auto max-w-6xl px-5 pt-8"><nav aria-label="Breadcrumb" class="text-sm text-slate-500"><a href="rooms.html" class="hover:text-ink">Rooms</a> / {r["name"]}</nav>
  <h1 class="mt-3 text-4xl md:text-5xl">{r["name"]}</h1></section>
<div class="mx-auto grid max-w-6xl gap-10 px-5 py-8 lg:grid-cols-3">
  <div class="lg:col-span-2">{img(f"room-{i+1}.jpg", r["name"]+" bedroom", 1200, 800, "aspect-[3/2] w-full rounded-3xl object-cover", True)}
    <h2 class="mt-10 text-2xl">About this room</h2><p class="mt-3">{r["long"]}</p>
    <dl class="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">{"".join(f'<div class="rounded-2xl bg-mist p-4"><dt class="text-xs text-slate-500">{a}</dt><dd class="font-semibold text-ink">{b}</dd></div>' for a,b in [("Type",r["cat"]),("Bed",r["bed"]),("Size",f'{r["size"]} sqm'),("Guests",f'Up to {r["guests"]}')])}</dl>
    <h2 class="mt-10 text-2xl">Included in your stay</h2><ul class="mt-4 grid gap-3 sm:grid-cols-2">{"".join(f'<li class="flex items-center gap-3 rounded-xl border border-slate-100 p-3 text-sm"><span class="text-brass">{icon(k,"h-5 w-5")}</span>{AMEN[k][0]}</li>' for k in r["am"])}</ul></div>
  <aside class="lg:sticky lg:top-24 lg:self-start"><div class="rounded-3xl border border-slate-100 bg-white p-6 shadow-lg" aria-label="Book this room">
    <p><span class="font-display text-3xl text-ink">{money(r["price"])}</span> <span class="text-sm text-slate-500">per night</span></p>
    <div class="mt-5">{enquiry_form(r["name"], True)}</div></div></aside></div>
<section class="bg-mist"><div class="section"><h2 class="text-3xl">You may also like</h2><div class="mt-8 grid gap-6 md:grid-cols-3">{"".join(room_card(j,x) for j,x in others)}</div></div></section>'''
    page(f'{r["slug"]}.html', f'{r["name"]} | {BRAND}', f'{r["name"]}: {r["short"]} From {money(r["price"])} per night.', body, "rooms.html")

# ---------- AMENITIES ----------
am = f'''<section class="bg-mist"><div class="mx-auto max-w-6xl px-5 py-14"><h1 class="text-4xl md:text-5xl">Amenities</h1><p class="mt-3 max-w-xl">The small things that make a stay easy. Most are included in every room.</p></div></section>
<div class="section"><ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{"".join(amen_tile(k) for k in AMEN)}</ul>
<div class="mt-12 rounded-3xl bg-ink p-8 text-white md:p-12"><h2 class="font-display text-2xl !text-white">Need something not listed?</h2><p class="mt-2 text-white/80">Extra bed, airport pick-up or early check-in: just ask.</p><a href="{WA_LINK}" target="_blank" rel="noopener" class="btn btn-wa mt-5">{WA_ICON} Ask on WhatsApp</a></div></div>'''
page("amenities.html", f"Amenities | {BRAND}", f"Free Wi-Fi, air conditioning, 24-hour front desk and more at {BRAND}.", am, "amenities.html")

# ---------- GALLERY ----------
cats = ["all","hotel","room","amenities","surroundings"]
btns = "".join(f'<button data-filter="{c}" aria-pressed="{"true" if c=="all" else "false"}" class="rounded-full border border-slate-200 px-4 py-2 text-sm capitalize text-ink aria-pressed:border-ink aria-pressed:bg-ink aria-pressed:text-white">{c}</button>' for c in cats)
gi = "".join(f'<button data-gallery-item data-cat="{c}" data-full="images/gallery-{n}.jpg" data-caption="{cap}" class="mb-3 block w-full break-inside-avoid overflow-hidden rounded-2xl" aria-label="Open photo: {cap}">{img(f"gallery-{n}-t.jpg", cap, 640, 1000 if (n-1)%3==0 else 700, "w-full transition duration-500 hover:scale-105")}</button>' for n,(c,cap) in enumerate(GAL,1))
gal = f'''<section class="bg-mist"><div class="mx-auto max-w-6xl px-5 py-14"><h1 class="text-4xl md:text-5xl">Gallery</h1><p class="mt-3">Tap any photo to view it full size.</p></div></section>
<div class="section"><div class="mb-8 flex flex-wrap gap-2" role="group" aria-label="Filter photos">{btns}</div><div class="columns-2 gap-3 md:columns-3 lg:columns-4">{gi}</div></div>
<dialog id="lightbox" class="m-auto w-[min(95vw,1100px)] rounded-2xl bg-black/95 p-3 text-white backdrop:bg-black/80" aria-label="Photo viewer">
  <img src="" alt="" class="max-h-[78vh] w-full rounded-xl object-contain"><p class="mt-3 text-center text-sm"></p>
  <div class="mt-3 flex justify-between"><button data-prev class="btn btn-ghost !py-2" aria-label="Previous photo">Prev</button><button data-close class="btn btn-ghost !py-2">Close</button><button data-next class="btn btn-ghost !py-2" aria-label="Next photo">Next</button></div></dialog>'''
page("gallery.html", f"Photo gallery | {BRAND}", f"Browse photos of rooms, lobby, amenities and the neighbourhood around {BRAND}.", gal, "gallery.html")

# ---------- CONTACT ----------
cards = "".join(f'<div class="rounded-2xl border border-slate-100 p-6"><p class="font-display text-lg text-ink">{t}</p><p class="mt-2 text-sm">{v}</p></div>' for t,v in [
  ("Phone",f'<a class="underline" href="tel:{PHONE.replace(" ","")}">{PHONE}</a>'),("Email",f'<a class="underline" href="mailto:{EMAIL}">{EMAIL}</a>'),("Address",ADDR),("Reception","Open 24 hours, every day")])
contact = f'''<section class="bg-mist"><div class="mx-auto max-w-6xl px-5 py-14"><h1 class="text-4xl md:text-5xl">Contact us</h1><p class="mt-3 max-w-xl">Questions about a room or your stay? Message us and we usually reply within the hour.</p></div></section>
<div class="section"><div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{cards}</div>
<div class="mt-12 grid gap-8 lg:grid-cols-2">
  <form data-enquiry class="space-y-4 rounded-3xl border border-slate-100 p-6 shadow-sm" aria-labelledby="form-h"><h2 id="form-h" class="text-2xl">Send a message</h2>
    <label class="block text-sm font-medium text-ink">Full name<input class="field mt-1" name="name" required autocomplete="name"></label>
    <label class="block text-sm font-medium text-ink">Phone<input class="field mt-1" type="tel" name="phone" autocomplete="tel"></label>
    <label class="block text-sm font-medium text-ink">Subject<input class="field mt-1" name="subject"></label>
    <label class="block text-sm font-medium text-ink">Message<textarea class="field mt-1" name="message" rows="4" required></textarea></label>
    <div class="flex flex-wrap gap-2"><button class="btn btn-wa" name="via" value="wa">{WA_ICON} Send on WhatsApp</button><button class="btn btn-primary" name="via" value="email">Send by email</button></div></form>
  <div class="overflow-hidden rounded-3xl border border-slate-100"><iframe title="Hotel location on Google Maps" class="h-full min-h-[22rem] w-full" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={MAPQ.replace(" ","+")}&output=embed"></iframe></div></div></div>'''
page("contact.html", f"Contact and location | {BRAND}", f"Call, email or WhatsApp {BRAND}. Find our address and map.", contact, "contact.html")

# sitemap + robots
pages = ["index","rooms","amenities","gallery","contact"] + [r["slug"] for r in ROOMS]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE}/{p}.html</loc></url>" for p in pages) + "</urlset>")
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built", len(pages), "pages")
