#!/usr/bin/env python3
"""Generates the static pages of the LLJ Marketing site into <out>/ (usage: build.py <public_dir> <domain>)."""
import html
import json
import sys
from urllib.parse import quote

OUT = sys.argv[1]
DOMAIN = sys.argv[2].rstrip("/")

NAV = [("index.html", "Home", "/"), ("about.html", "About", "/about"),
       ("pricelist.html", "Pricelist", "/pricelist"), ("contact.html", "Contact", "/contact")]

BUSINESS = {
    "@context": "https://schema.org",
    "@type": "Store",
    "name": "LLJ Marketing Sdn. Bhd.",
    "url": DOMAIN + "/",
    "telephone": "+60 16-780 8678",
    "description": "iPhone wholesale and retail supplier offering new and pre-owned iPhones.",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "11, Batu, 5, Jalan Perdana 1, Taman Segar Perdana",
        "addressLocality": "Cheras",
        "addressRegion": "Selangor",
        "postalCode": "43200",
        "addressCountry": "MY",
    },
}

# ---------------- pricelist data (typos fixed: iPhone 16 Plus, RM, 128 Gb, Gb) ----------------
LL_A = [
    ("iPhone 11", [(64, 590), (128, 690), (256, 710)]),
    ("iPhone 11 Pro", [(64, 690), (256, 790)]),
    ("iPhone 11 Pro Max", [(64, 750), (256, 830)]),
    ("iPhone 12 Mini", [(64, 500), (128, 500), (256, 500)]),
    ("iPhone 12", [(64, 660), (128, 750), (256, 800)]),
    ("iPhone 12 Pro", [(128, 930), (256, 1030)]),
    ("iPhone 12 Pro Max", [(128, 1070), (256, 1170), (512, 1180)]),
    ("iPhone 13 Mini", [(128, 840), (256, 940)]),
    ("iPhone 13", [(128, 1000), (256, 1060), (512, 1080)]),
    ("iPhone 13 Pro", [(128, 1330), (256, 1450), (512, 1490)]),
    ("iPhone 13 Pro Max", [(128, 1480), (256, 1680), (512, 1700)]),
    ("iPhone 14 Plus", [(128, 1160)]),
]
LL_B = [
    ("iPhone 15", [(128, 1550), (256, 1780), (512, 1880)]),
    ("iPhone 15 Plus", [(128, 1750), (256, 1880)]),
    ("iPhone 15 Pro", [(128, 2000), (256, 2150)]),
    ("iPhone 15 Pro Max", [(256, 2500)]),
    ("iPhone 16", [(128, 2030), (256, 2180)]),
    ("iPhone 16 Plus", [(128, 2150), (256, 2480)]),
    ("iPhone 16 Pro", [(128, 2500), (256, 2700)]),
    ("iPhone 16 Pro Max", [(256, 3020)]),
]
ZP = [
    ("iPhone 14", [(128, 1150), (256, 1250)]),
    ("iPhone 14 Pro", [(128, 1730), (256, 1830)]),
    ("iPhone 14 Pro Max", [(128, 1930), (256, 2080)]),
]

e = html.escape


def head(title, desc, path, extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{DOMAIN}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LLJ Marketing">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta name="theme-color" content="#00999d">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{extra}</head>
"""


def header(active):
    items = []
    for href, label, _ in NAV:
        cur = ' aria-current="page"' if href == active else ""
        items.append(f'        <li><a href="{href}"{cur}>{label}</a></li>')
    links = "\n".join(items)
    return f"""<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="LLJ Marketing — home"><img src="images/logo.png" width="176" height="61" alt="LLJ Marketing Sdn. Bhd."></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span class="bars"><span></span><span></span><span></span></span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
{links}
      </ul>
    </nav>
  </div>
</header>
"""


FOOT = """<script src="js/main.js" defer></script>
</body>
</html>
"""


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, indent=2, ensure_ascii=False) + "\n</script>\n"


# ---------------- pages ----------------
def page_home():
    t = head("LLJ Marketing | iPhone Wholesale & Retail Supplier in Cheras, Selangor",
             "Quality new and pre-owned iPhones at competitive prices. LLJ Marketing is an iPhone wholesale and retail supplier based in Cheras, Selangor, Malaysia, with worldwide distribution.",
             "/", ld(BUSINESS))
    t += header("index.html")
    t += """<main id="main">
  <section class="hero">
    <div class="wrap">
      <div class="hero-text">
        <h1>LLJ MARKETING</h1>
        <p class="subtitle">Your Trusted iPhone Wholesale &amp; Retail Supplier</p>
        <p class="lead"><strong>Competitive Prices. Quality Assured. Worldwide Distribution</strong></p>
        <p class="lead">Based in Cheras, Selangor, LLJ Marketing is an iPhone wholesale and retail supplier with 6 years of experience, <strong>offering quality new and pre-owned iPhones at competitive prices.</strong></p>
        <div class="btn-row">
          <a class="btn" href="pricelist.html">Pricelist</a>
          <a class="btn" href="contact.html">Contact</a>
        </div>
      </div>
      <div class="phone"><img src="images/hero-phone.png" width="2048" height="1536" alt="iPhone showing the LLJ Marketing logo" fetchpriority="high"></div>
    </div>
  </section>
</main>
"""
    return t + FOOT


def page_about():
    t = head("About LLJ Marketing | Wholesale & Retail iPhone Supply",
             "LLJ Marketing is a Malaysia-based iPhone wholesale and retail supplier specialising in pre-owned iPhones, with new devices for individual customers and business partners worldwide.",
             "/about")
    t += header("about.html")
    t += """<main id="main">
  <section class="about">
    <div class="wrap about-grid">
      <div class="about-intro">
        <div class="block">
          <h1>LLJ MARKETING</h1>
          <p class="subtitle">Your Reliable Partner for iPhone Supply</p>
          <p class="lead">LLJ Marketing is a Malaysia-based iPhone wholesale and retail supplier committed to providing quality products at competitive prices. We specialize in pre-owned iPhones, while also offering new devices to meet different customer needs.</p>
          <p class="lead">With a focus on product quality, competitive pricing, and customer satisfaction, we aim to build lasting relationships with individual customers and business partners worldwide.</p>
        </div>
      </div>
      <div class="phone"><img src="images/about-phone.png" width="2482" height="1862" alt="iPhone showing the LLJ Marketing logo" loading="lazy"></div>
      <div class="about-rest">
        <div class="block">
          <h2 class="section-title">WHOLESALE &amp; RETAIL</h2>
          <p class="subtitle">Flexible Solutions for Every Customer</p>
        </div>
        <div class="block">
          <h3>Wholesale Supply</h3>
          <p class="lead">Looking for a reliable iPhone supplier for your business?</p>
          <p class="lead">LLJ Marketing offers competitive wholesale pricing, special rates for bulk purchases, and dedicated services for business customers and resellers.</p>
        </div>
        <div class="block">
          <h3>Retail Purchase</h3>
          <p class="lead">Looking for an iPhone for personal use?</p>
          <p class="lead">Explore our selection of new and pre-owned iPhones with competitive prices and quality-assured devices.</p>
        </div>
      </div>
    </div>
  </section>
</main>
"""
    return t + FOOT


def table(tid, region, label, models, first_label):
    total = sum(len(o) for _, o in models)
    rows = []
    for mi, (model, opts) in enumerate(models):
        last_model = mi == len(models) - 1
        for oi, (gb, price) in enumerate(opts):
            cells = []
            if oi == 0:
                cls = "device last" if last_model else "device"
                cells.append(f'<th class="{cls}" scope="rowgroup" role="rowheader" rowspan="{len(opts)}">{e(model)}</th>')
            cells.append(f'<td class="num storage" role="cell">{gb} Gb</td>')
            cells.append(f'<td class="num price" role="cell">{price} RM</td>')
            if mi == 0 and oi == 0:
                cells.append(f'<td class="region" role="cell" rowspan="{total}">{region}</td>')
            rows.append('        <tr role="row">' + "".join(cells) + "</tr>")
    body = "\n".join(rows)
    return f"""      <div class="table-block">
        <h3 id="{tid}">{e(label)}</h3>
        <div class="table-card">
          <table class="price-table" role="table" aria-labelledby="{tid}">
            <thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Device</th><th role="columnheader" scope="col">Storage</th><th role="columnheader" scope="col">Price</th><th role="columnheader" scope="col">Region</th></tr></thead>
            <tbody role="rowgroup">
{body}
            </tbody>
          </table>
        </div>
      </div>
"""


def page_pricelist():
    t = head("iPhone Pricelist (RM) | LLJ Marketing",
             "Wholesale and retail pricelist for new and pre-owned iPhone 11 to iPhone 16 Pro Max by storage and region (LL, ZP). Prices in Malaysian Ringgit (RM).",
             "/pricelist")
    t += header("pricelist.html")
    t += """<main id="main">
  <section class="pricelist">
    <div class="wrap">
      <h1>OUR PRICELIST</h1>
      <div class="tables">
"""
    t += '    <div class="tables-col">\n' + table("tbl-ll-a", "LL", "Region LL: iPhone 11 to iPhone 14 Plus", LL_A, "") + "    </div>\n"
    t += '    <div class="tables-col">\n' + table("tbl-ll-b", "LL", "Region LL: iPhone 15 to iPhone 16 Pro Max", LL_B, "") \
        + table("tbl-zp", "ZP", "Region ZP: iPhone 14 series", ZP, "") + "    </div>\n"
    t += """      </div>
    </div>
  </section>
  <section class="why">
    <div class="wrap">
      <h2 class="section-title">WHY CHOOSE LLJ MARKETING?</h2>
      <ul>
        <li><strong>Competitive Pricing</strong> — Attractive prices for both wholesale and retail customers.</li>
        <li><strong>Strict Quality Control</strong> — Pre-owned devices undergo careful inspection before distribution.</li>
        <li><strong>Wide Product Selection</strong> — Various iPhone models, storage capacities, and regional variants.</li>
        <li><strong>Warranty &amp; Aftersales</strong> — Customer support and aftersales services for greater peace of mind.</li>
        <li><strong>Trade-In Services</strong> — Flexible options for customers looking to upgrade their devices.</li>
        <li><strong>Worldwide Distribution</strong> — Serving customers and business partners across international markets.</li>
      </ul>
    </div>
  </section>
  <section class="ship">
    <div class="wrap stack">
      <h2 class="section-title">WORLDWIDE SHIPPING</h2>
      <p class="subtitle">Connecting iPhone Supply to Global Markets</p>
      <p class="lead">Based in Cheras, Selangor, Malaysia, LLJ Marketing serves customers and business partners beyond local markets. We welcome international inquiries and provide shipping solutions to support wholesale and retail purchases worldwide.</p>
    </div>
  </section>
</main>
"""
    return t + FOOT


def page_contact():
    addr = "11, Batu, 5, Jalan Perdana 1, Taman Segar Perdana, 43200 Cheras, Selangor, Malaysia"
    maps = "https://www.google.com/maps/search/?api=1&query=" + quote("LLJ Marketing Sdn. Bhd. " + addr)
    t = head("Contact LLJ Marketing | Cheras, Selangor, Malaysia",
             "Contact LLJ Marketing for iPhone availability, wholesale pricing and business inquiries. Call +60 16-780 8678 or visit us in Taman Segar Perdana, Cheras, Selangor.",
             "/contact", ld(BUSINESS))
    t += header("contact.html")
    t += f"""<main id="main">
  <section class="contact wrap">
    <div class="stack">
      <h1>LET'S BUILD A BUSINESS CONNECTION</h1>
      <p class="lead">Whether you're an individual buyer, reseller, or business owner, LLJ Marketing is ready to assist you. Get in touch with our team for product availability, wholesale pricing, and business inquiries.</p>
      <p><a class="phone-link" href="tel:+60167808678"><span class="icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.61 21 3 13.39 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2z"/></svg></span><span>+60 16-780 8678</span></a></p>
    </div>
    <div class="stack">
      <h2 class="section-title">OUR LOCATION</h2>
      <div class="location">
        <a class="map-link" href="{e(maps)}" target="_blank" rel="noopener"><img src="images/map.png" width="253" height="253" alt="Map showing the LLJ Marketing location in Cheras, Selangor" loading="lazy"></a>
        <div>
          <p class="company">LLJ MARKETING SDN. BHD.</p>
          <address>{e(addr)}</address>
        </div>
      </div>
    </div>
  </section>
</main>
"""
    return t + FOOT


def write(name, content):
    with open(f"{OUT}/{name}", "w", encoding="utf-8") as f:
        f.write(content)


write("index.html", page_home())
write("about.html", page_about())
write("pricelist.html", page_pricelist())
write("contact.html", page_contact())
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
urls = "".join(f"  <url><loc>{DOMAIN}{p}</loc></url>\n" for _, _, p in NAV)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
print("built", OUT, DOMAIN)
