"""Generate the Siddha365 static multi-page website from the content below."""

from html import escape
import hashlib
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import unquote, urlsplit

# Optional image optimization using Pillow (PIL).
# Handled via dynamic import so missing PIL never triggers linter or module errors.
try:
    import importlib
    Image = importlib.import_module("PIL.Image")
    ImageOps = importlib.import_module("PIL.ImageOps")
except (ImportError, ModuleNotFoundError):
    Image = ImageOps = None


SITE = Path(__file__).resolve().parent
from site_content import (
    PHONE,
    PHONE_TEL,
    WHATSAPP,
    INSTAGRAM,
    MOGAPPAIR_MAP,
    FACEBOOK,
    GOOGLE_SEARCH,
    GOOGLE_EMBED,
    REVIEWS_API,
    ASSET_VERSION,
    LOGO,
    FAVICON,
    DOCTOR,
    FOUNDER_DOCTOR,
    HERO_ALT,
    CONDITIONS,
    NAV,
    HOME_SLIDES,
    SPECIALTY_CARE,
    VIDEOS,
    POPULAR_VIDEOS,
    YOUTUBE_SHORTS,
    INSTAGRAM_REELS,
    YOUTUBE_CHANNEL,
    PARTNER_LOGOS,
)

def partner_logo_html(route, path, name):
    # CSS fits the original artwork without modifying or recompressing its pixels.
    return f'<div class="partner-logo"><span class="partner-art" data-partner="{esc(name)}"><img src="{asset(route, path)}" alt="{esc(name)}" loading="lazy" decoding="async"></span></div>'


def esc(value):
    return escape(str(value), quote=True)


def rel(current, target):
    """Relative URL from a route directory to another route or site asset."""
    current_dir = current or "."
    value = posixpath.relpath(target or ".", current_dir)
    return "./" if value == "." else value.rstrip("/") + "/"


def asset(current, path):
    return posixpath.relpath(path, current or ".")


def page_shell(route, title, description, body, *, homepage=False, section=""):
    body = body.replace("at Siddha 365 Health Care Clinic.", "at <span class=\"founder-clinic-name\">Siddha 365 Health Care Clinic</span>.")
    route_dir = route
    site_css_version = "20261020-partner-scroll-v1"
    css = f"{asset(route_dir, 'assets/site.css')}?v={site_css_version}"
    refinement_version = "20261022-treatment-image-edges-v3"
    refinements = f"{asset(route_dir, 'assets/refinement.css')}?v={refinement_version}"
    experience_version = "20261021-home-slider-fit-v1" if homepage else ASSET_VERSION
    experience_css = f"{asset(route_dir, 'assets/experience.css')}?v={experience_version}"
    experience_js = f"{asset(route_dir, 'assets/experience.js')}?v={ASSET_VERSION}"
    js_version = "20261020-new-logo-v3"
    js = f"{asset(route_dir, 'assets/site.js')}?v={js_version}"
    boot = f"{asset(route_dir, 'assets/boot.js')}?v={ASSET_VERSION}"
    review_script = f'<script defer src="{asset(route_dir, "assets/reviews.js")}?v={ASSET_VERSION}"></script>' if 'data-live-reviews-url' in body else ''
    active_section = section or (route.split("/", 1)[0] if route else "")
    about_href = rel(route_dir, "about")
    about_active = (active_section == "about")
    about_active_attr = ' aria-current="page"' if about_active else ""
    nav_items = []
    for label, target in NAV:
        is_active = (target == active_section) or (target == "" and not active_section)
        href = rel(route_dir, target)
        item_class = ' class="nav-item-about"' if target == "about" else ""
        nav_items.append(f'<li{item_class}><a href="{href}"' + (' aria-current="page"' if is_active else "") + f'>{label}</a></li>')
    nav_html = "\n".join(nav_items)
    logo = asset(route_dir, LOGO)
    favicon = asset(route_dir, FAVICON)
    tel = f"tel:{PHONE_TEL}"
    if not homepage:
        page_social = f'''<aside class="social-rail" aria-label="Siddha365 social links"><span class="social-rail-label">Follow Siddha365</span><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer" aria-label="Message Siddha365 on WhatsApp"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.7 15l-1 4 4-1A10 10 0 1 0 12 2Z"/></svg></a><a href="{YOUTUBE_CHANNEL}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on YouTube"><svg viewBox="0 0 24 24"><path d="M23 12s0-4-1-5-2-1-4-1H6C4 6 3 6 2 7s-1 5-1 5 0 4 1 5 2 1 4 1h12c2 0 3 0 4-1s1-5 1-5Zm-14 3V9l5 3-5 3Z"/></svg></a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on Instagram"><svg viewBox="0 0 24 24"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7Z"/></svg></a><a href="{FACEBOOK}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on Facebook"><svg viewBox="0 0 24 24"><path d="M14 22v-9h3l1-4h-4V7c0-1 1-2 2-2h2V1h-3c-3 0-5 2-5 5v3H7v4h3v9h4Z"/></svg></a></aside>'''
        page_social = page_social.replace('M12 2a10 10 0 0 0-8.7 15l-1 4 4-1A10 10 0 1 0 12 2Z', 'M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.6 4.2 1.7 6L.2 24l6.3-1.7a11.8 11.8 0 0 1 5.6 1.4h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.3-6.2-3.5-8.4Z')
    page_social = "" if homepage else f'<a class="site-whatsapp-float" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer" aria-label="Message Siddha365 on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.6 4.2 1.7 6L.2 24l6.3-1.7a11.8 11.8 0 0 0 5.6 1.4h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.3-6.2-3.5-8.4Zm-8.4 18.1h-.1a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4a9.8 9.8 0 1 1 8.4 4.6Zm5.4-7.3c-.3-.2-1.8-.9-2.1-1s-.5-.2-.7.2c-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-1.8-.9-3-1.6-4.2-3.6-.3-.5.3-.5.9-1.6.1-.2.1-.4 0-.6s-.7-1.7-.9-2.3c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.1 1.1-1.1 2.7s1.1 3.1 1.3 3.3c.2.2 2.2 3.4 5.3 4.7 2 .9 2.8 1 3.8.8.6-.1 1.8-.7 2.1-1.4.3-.7.3-1.3.2-1.4-.1-.2-.3-.3-.7-.5Z"/></svg></a>'
    if not homepage:
        page_social = f'''<aside class="social-rail" aria-label="Siddha365 social links"><span class="social-rail-label">Follow Siddha365</span><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer" aria-label="Message Siddha365 on WhatsApp"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.7 15l-1 4 4-1A10 10 0 1 0 12 2Z"/></svg></a><a href="{YOUTUBE_CHANNEL}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on YouTube"><svg viewBox="0 0 24 24"><path d="M23 12s0-4-1-5-2-1-4-1H6C4 6 3 6 2 7s-1 5-1 5 0 4 1 5 2 1 4 1h12c2 0 3 0 4-1s1-5 1-5Zm-14 3V9l5 3-5 3Z"/></svg></a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on Instagram"><svg viewBox="0 0 24 24"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Z"/></svg></a><a href="{FACEBOOK}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on Facebook"><svg viewBox="0 0 24 24"><path d="M14 22v-9h3l1-4h-4V7c0-1 1-2 2-2h2V1h-3c-3 0-5 2-5 5v3H7v4h3v9h4Z"/></svg></a></aside>'''
    if not homepage:
        page_social = page_social.replace('M12 2a10 10 0 0 0-8.7 15l-1 4 4-1A10 10 0 1 0 12 2Z', 'M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.6 4.2 1.7 6L.2 24l6.3-1.7a11.8 11.8 0 0 1 5.6 1.4h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.3-6.2-3.5-8.4Z')
    dialog = ""
    if homepage:
        dialog = f'''<dialog class="visit-dialog" id="visit-dialog" aria-labelledby="dialog-title">
  <div class="dialog-content"><div class="dialog-top"><div><p class="eyebrow">Siddha365 · Chennai</p><h2 id="dialog-title">Plan a clinic visit</h2></div><button class="dialog-close" type="button" data-dialog-close aria-label="Close appointment message">×</button></div>
    <p>Speak with the clinic about an appointment, opening hours, or the right next step for your concern.</p>
    <div class="dialog-actions"><a class="button" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Message on WhatsApp ↗</a><a class="button button-secondary" href="{tel}">Call {PHONE}</a></div>
  </div>
</dialog>'''
    html = f'''<!doctype html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#0c110e">
  <meta name="description" content="{esc(description)}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; base-uri 'self'; object-src 'none'; form-action 'self'; script-src 'self'; style-src 'self'; img-src 'self' https://i.ytimg.com; font-src 'self'; connect-src 'self' https://siddha365.com; frame-src https://www.youtube-nocookie.com https://maps.google.com https://www.google.com; upgrade-insecure-requests">
  <title>{esc(title)} | Siddha365 Health Care Clinic</title>
  <link rel="canonical" href="https://siddha365.com/{route + '/' if route else ''}">
  <link rel="icon" type="image/png" href="{favicon}">
  <link rel="preload" as="image" href="{logo}">
  <script src="{boot}"></script>
  <link rel="stylesheet" href="{css}">
  <link rel="stylesheet" href="{refinements}">
  <link rel="stylesheet" href="{experience_css}">
  <script defer src="{experience_js}"></script>
  <script defer src="{js}"></script>
  {review_script}
</head>
<body class="page-{section or ('home' if homepage else route.split('/')[0])}">
  <div class="page-loader" aria-hidden="true"><div class="loader-mark"><img src="{logo}" alt="" width="150" height="92"><span class="loader-scan"></span></div><span class="loader-label">Siddha365 · Care, with you in mind</span><span class="loader-line"></span></div>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <div class="utility-bar"><div class="container utility-inner"><p><span class="utility-tamil">உணவே மருந்து — மருந்தே உணவு;</span></p><div class="utility-actions"><p><a href="{tel}">Call {PHONE}</a><span class="utility-hours"><span aria-hidden="true"> &nbsp;·&nbsp; </span>Mon–Sat, 10:30 am–1:30 pm &amp; 7–9:30 pm</span></p><button class="motion-toggle" type="button" data-motion-toggle aria-pressed="false">Pause motion</button></div></div></div>
  <header class="site-header">
    <a class="desktop-external-brand" href="{rel(route_dir, '')}" aria-label="Siddha365 home"><img src="{asset(route_dir, 'assets/optimized/siddha365-transparent-logo.png')}" alt="Siddha 365 Health Care Clinic" width="150" height="92"></a>
    <div class="nav-capsule">
      <a class="brand" href="{rel(route_dir, '')}" aria-label="Siddha365 home"><img src="{logo}" alt="Siddha 365 Health Care Clinic" width="138" height="84"></a>
      <nav class="nav-menu" aria-label="Main navigation"><ul class="nav-links" id="primary-navigation">{nav_html}<li class="nav-drawer-cta"><a class="button button-small nav-cta-drawer" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Book appointment ↗</a></li></ul></nav>
      <div class="nav-actions">
        <a class="nav-pill-about" href="{about_href}"{about_active_attr}>About us</a>
        <a class="button button-small nav-cta" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer"><span class="nav-cta-text-full">Book Appointment</span><span class="nav-cta-text-short">Book</span><span class="nav-cta-arrow" aria-hidden="true"> ↗</span></a>
        <button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="primary-navigation"><span class="menu-icon" aria-hidden="true"></span></button>
      </div>
    </div>
  </header>
  {page_social}{body}
  {footer(route_dir)}
  {dialog}
  <dialog class="media-dialog" id="video-dialog" aria-labelledby="video-dialog-title"><div class="media-dialog-head"><div><p class="eyebrow">Siddha365 · Watch &amp; learn</p><h2 id="video-dialog-title">Clinic video</h2></div><button class="dialog-close" type="button" data-dialog-close aria-label="Close video">×</button></div><div class="video-dialog-player" data-video-player></div></dialog>
  <dialog class="review-dialog" id="review-dialog" aria-labelledby="review-dialog-title"><div class="media-dialog-head"><h2 id="review-dialog-title">Patient review</h2><button class="dialog-close" type="button" data-dialog-close aria-label="Close review">×</button></div><div data-review-detail></div></dialog>
</body>
</html>'''
    return html


def footer(route):
    home = rel(route, "")
    treatment = rel(route, "treatments")
    about = rel(route, "about")
    reviews = rel(route, "reviews")
    contact = rel(route, "contact-us")
    gallery = rel(route, "gallery")
    tel = f"tel:{PHONE_TEL}"
    logo = asset(route, LOGO)
    partner_items = "".join(partner_logo_html(route, path, name) for path, name in PARTNER_LOGOS)
    return f'''<footer class="footer">
  <section class="container partner-section" aria-labelledby="partner-title">
    <div class="partner-heading"><h2 id="partner-title">Our herbal partners</h2></div>
    <div class="partner-marquee" aria-label="Siddha365 herbal partners"><div class="partner-track"><div class="partner-set">{partner_items}</div><div class="partner-set" aria-hidden="true">{partner_items}</div></div></div>
  </section>
  <div class="container footer-grid">
    <div class="footer-brand"><a class="brand" href="{home}" aria-label="Siddha365 home"><img src="{logo}" alt="Siddha 365 Health Care Clinic"></a><p>Thoughtful Siddha care with personal attention in Chennai. Every concern starts with a conversation and an individual assessment.</p></div>
    <div><h2 class="footer-title">Explore</h2><div class="footer-links"><a href="{treatment}">Treatments</a><a href="{about}">About the clinic</a><a href="{gallery}">Gallery</a><a href="{reviews}">Google reviews</a></div></div>
    <div><h2 class="footer-title">Visit</h2><div class="footer-links"><a href="{contact}">Clinic locations</a><a href="{MOGAPPAIR_MAP}" target="_blank" rel="noopener noreferrer">Mogappair East location ↗</a><a href="{contact}#hours">Opening hours</a><a href="{tel}">{PHONE}</a><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp appointments</a></div></div>
    <div><h2 class="footer-title">Clinic hours</h2><div class="footer-links"><span>Monday – Saturday</span><span>10:30 am – 1:30 pm</span><span>7:00 pm – 9:30 pm</span><span>Sunday · by appointment</span></div></div>
  </div>
  <div class="footer-bottom container"><p>© 2026 Siddha365 Health Care Clinic</p><p>Health information on this site is general and does not replace an individual medical consultation.</p></div>
</footer>'''


def breadcrumb(route, title):
    crumbs = [f'<a href="{rel(route, "")}">Home</a>']
    if route.startswith("treatments"):
        crumbs.extend([f'<span class="separator" aria-hidden="true">/</span>', f'<a href="{rel(route, "treatments")}">Treatments</a>'])
    crumbs.extend([f'<span class="separator" aria-hidden="true">/</span>', f'<span aria-current="page">{esc(title)}</span>'])
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + "".join(crumbs) + "</nav>"


def image_for(route, path, alt, cls="", *, loading=None, priority=False):
    cls_attr = f' class="{cls}"' if cls else ""
    loading = loading or ("eager" if "page-hero-art" in cls else "lazy")
    priority_attr = ' fetchpriority="high"' if priority or loading == "eager" else ""
    return f'<img{cls_attr} src="{asset(route, path)}" alt="{esc(alt)}" loading="{loading}" decoding="async"{priority_attr}>'


def condition_card(route, condition):
    href = rel(route, "treatments/" + condition["slug"])
    # Keep the card grid responsive: images load as cards approach the viewport.
    # The source assets are committed, so lazy loading no longer risks missing files.
    image = image_for(route, condition["image"], condition.get("image_alt", condition["title"]), "condition-image", loading="lazy")
    return f'''<a class="condition-card reveal" href="{href}">
      {image}<div class="condition-body"><span class="tag">{esc(condition['category'])}</span><h3>{esc(condition['title'])}</h3><p>{esc(condition['intro'])}</p><span class="text-link">Read the care guide</span></div>
    </a>'''


def review_rows_html(route):
    # Only the live feed may populate review cards; no testimonials are stored here.
    rows = "".join(f'<div class="review-marquee" role="group" aria-label="Google reviews, row {i + 1}"><div class="review-marquee-track"><div class="review-group" data-review-group></div><div class="review-group" data-review-duplicate aria-hidden="true"></div></div></div>' for i in range(2))
    logo = asset(route, LOGO)
    return f'''<div class="review-feed-placeholder" data-review-placeholder><img src="{logo}" width="112" height="68" alt="Siddha365"><div><strong data-review-placeholder-title>Patient experiences, in their own words</strong><p data-review-placeholder-copy>Reviews will appear here when the clinic’s Google review feed connects.</p></div></div><div class="review-marquees" data-review-rows hidden>{rows}</div><noscript><p class="medical-note">Enable JavaScript to load current reviews from the clinic’s Google review feed.</p></noscript>'''


def nasagra_home_section():
    route = ""
    diagram = image_for(
        route,
        "wp-content/uploads/2026/02/thepranabody.png",
        "Traditional illustration used by the clinic to describe pranayama concepts; it is not an anatomical diagram",
        "nasagra-art-image",
    )
    return f'''<section class="section home-nasagra-section" id="nasagra-mudra"><div class="container"><div class="section-head"><div><p class="eyebrow">Traditional breathing practice · Learning guide</p><h2>Nasagra <span class="accent">Mudra</span></h2><p class="lead">A traditional hand position used in alternate-nostril breathing. This learning guide presents the practice as a cultural and wellness tradition, not as a treatment or cure for disease.</p></div></div><blockquote class="traditional-quote" lang="ta">“வளி, அழல், ஐயம் சமநிலையில் இருந்தால் ஆரோக்கியம்; அவை சீர்கெட்டால் நோய்.”</blockquote><div class="nasagra-page-grid"><div class="condition-content">
  <section class="prose-panel reveal"><h3>About the practice</h3><p>In descriptions of Nasagra Mudra, the thumb rests near one nostril while the ring and little fingers rest near the other. Some traditions use Vishnu Mudra, folding the index and middle fingers into the palm. The left hand may rest comfortably on the knee. Hand positions vary across teachers and traditions.</p></section>
  <section class="prose-panel reveal"><h3>How it is traditionally described</h3><ol class="nasagra-steps"><li>Sit in a comfortable position and keep the breath natural.</li><li>If a qualified instructor has shown you the technique, gently close one nostril and breathe through the other without straining.</li><li>Do not force, hold, or deliberately deepen the breath. Stop and rest if you feel dizzy, uncomfortable, or short of breath.</li></ol></section>
  <section class="prose-panel reveal"><h3>Benefits and evidence</h3><p>People may explore breathing practices for general wellbeing or as part of yoga. Research on yoga and breathing techniques varies, and this practice should not be presented as a cure for a medical condition or used in place of medical care.</p></section>
  <section class="prose-panel reveal"><h3>Safety and guidance</h3><p>Learn from a qualified instructor. If you have a health condition, are pregnant, are older, or have concerns about whether breath practice is suitable for you, discuss it with your healthcare provider first. Avoid forceful breathing and stop if you feel unwell.</p><div class="source-list"><a href="https://www.nccih.nih.gov/health/yoga-effectiveness-and-safety" target="_blank" rel="noopener noreferrer">NCCIH: Yoga effectiveness and safety ↗</a><a href="https://www.cuh.nhs.uk/patient-information/breathing-exercises/" target="_blank" rel="noopener noreferrer">Cambridge University Hospitals: Breathing exercises ↗</a></div></section>
  <p class="medical-note"><strong>Please note:</strong> This is general educational information, not a diagnosis or personal treatment plan. Do not delay medical assessment or stop a prescribed treatment to try a breathing practice.</p>
</div><figure class="nasagra-art reveal">{diagram}<figcaption>Traditional illustration provided in the clinic’s original website material. Its labels represent traditional concepts, not medical anatomy.</figcaption></figure></div></div></section>'''


def care_explorer():
    categories = [
        ("women", "Women’s Health Care", "Care through different stages of life", "Explore guides to fertility and menstrual health, and prepare for a conversation about your needs.", ["infertility", "pcod"]),
        ("skin", "Skin & Hair", "Start with understanding your concern", "Find information about skin, hair and foot concerns, with guidance on assessment and next steps.", ["skin-problems", "hair-fall", "corn-foot"]),
        ("movement", "Joints & Cupping Therapy", "Explore comfort, movement and care", "Read about joint concerns and traditional therapies, including what to discuss with your clinician.", ["joint-pain", "kati-vasthi", "fire-cupping", "hijama-cupping"]),
        ("family", "Family & Child Care", "Information for everyday health questions", "Browse care guides for ongoing concerns and learn when individual assessment or specialist care is needed.", ["diabetes", "weight-management", "sinusitis", "wheezing", "piles", "autism"]),
    ]
    by_slug = {item['slug']: item for item in CONDITIONS}
    tabs = []
    panels = []
    for index, (key, label, title, copy, slugs) in enumerate(categories):
        tabs.append(f'<button type="button" role="tab" id="care-tab-{key}" aria-controls="care-panel-{key}" aria-selected="{str(index == 0).lower()}" data-care-tab="{key}">{label}<span aria-hidden="true">↗</span></button>')
        featured = by_slug[slugs[0]]
        image = image_for('', featured['image'], featured['title'], 'care-explorer-image', loading='eager')
        links = ''.join(f'<a class="care-guide-link" href="treatments/{slug}/"><span class="guide-index" aria-hidden="true">0{i + 1}</span><span><strong>{esc(by_slug[slug]["title"])}</strong><small>Read the care guide</small></span><span class="guide-arrow" aria-hidden="true">↗</span></a>' for i, slug in enumerate(slugs))
        panels.append(f'<section class="care-panel" id="care-panel-{key}" role="tabpanel" aria-labelledby="care-tab-{key}" tabindex="0" data-care-panel="{key}"><div class="care-panel-overview"><div class="care-panel-photo">{image}<span class="care-photo-caption">Individual care. Clear next steps.</span></div><div class="care-panel-intro"><p class="eyebrow">{label}</p><h3>{title}</h3><p>{copy}</p><a class="text-link" href="contact-us/">Talk to the clinic</a></div></div><div class="care-guide-list">{links}</div></section>')
    return f'<div class="care-explorer" data-care-explorer><div class="care-tabs" role="tablist" aria-label="Explore care by category">{"".join(tabs)}</div><div class="care-panels">{"".join(panels)}</div><p class="care-explorer-note"><span aria-hidden="true">✦</span> Every person is different. An individual consultation helps determine the right next step.</p></div>'


def homepage():
    route = ""
    slide_markup = []
    for index, (path, label) in enumerate(HOME_SLIDES):
        image = image_for(route, path, label, "home-slide-image", loading="eager" if index == 0 else "lazy", priority=index == 0)
        if index >= 2:
            desktop_path = f"assets/home-slider-desktop/slider-{index - 1}.png"
            desktop_image = image_for(route, desktop_path, label, "home-slide-image", loading="eager" if index == 0 else "lazy", priority=index == 0)
            image = f'<picture><source media="(min-width: 721px)" srcset="{desktop_path}">{image}</picture>'
        slide_markup.append(f'<figure class="home-slide">{image}</figure>')
    slides = "".join(slide_markup)
    explorer = care_explorer()

    stats = "".join([
        '<article class="home-stat"><span class="stat-icon" aria-hidden="true"><svg viewBox="0 0 48 48"><path d="M8 37V10M8 37h33M13 29l9-9 7 7 12-14M33 13h8v8"/></svg></span><strong data-count-to="5">5</strong><span class="stat-label">Year of experience</span></article>',
        '<article class="home-stat"><span class="stat-icon" aria-hidden="true"><svg viewBox="0 0 48 48"><g transform="rotate(-42 18 24)"><rect x="10" y="8" width="15" height="32" rx="7.5"/><path d="M10 24h15"/></g><g transform="rotate(42 32 24)"><rect x="25" y="12" width="13" height="27" rx="6.5"/><path d="M25 25.5h13"/></g></svg></span><strong data-count-to="516">516</strong><span class="stat-label">Health concerns supported</span></article>',
        '<article class="home-stat"><span class="stat-icon" aria-hidden="true"><svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="17"/><path d="M24 12v24M18 18h9a5 5 0 0 1 0 10h-7a5 5 0 0 0 0 10h10M7 10h10M31 38h10"/></svg></span><strong data-count-to="723">723</strong><span class="stat-label">Treatments</span></article>',
        '<article class="home-stat"><span class="stat-icon" aria-hidden="true"><svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="18"/><path d="M17 20h.1M31 20h.1M16 28c2.2 4.2 4.8 6 8 6s5.8-1.8 8-6"/></svg></span><strong data-count-to="5102">5,102</strong><span class="stat-label">Clients served</span></article>',
    ])
    video_cards = "".join(f'''<article class="video-card"><button class="video-poster" type="button" data-youtube-id="{esc(vid)}" data-youtube-title="{esc(label)}" aria-label="Play {esc(label)}"><img src="https://i.ytimg.com/vi/{esc(vid)}/hqdefault.jpg" alt="" loading="lazy" decoding="async"><span class="video-play-icon" aria-hidden="true">▶</span></button><p>{esc(label)}</p></article>''' for vid, label in VIDEOS)
    home_video_cards = "".join(f'''<article class="home-video-card"><button class="home-video-poster" type="button" data-youtube-id="{esc(vid)}" data-youtube-title="{esc(label)}" aria-label="Play {esc(label)}"><img src="https://i.ytimg.com/vi/{esc(vid)}/mqdefault.jpg" alt="" loading="lazy" decoding="async"><span class="video-play-icon" aria-hidden="true">▶</span></button><p>{esc(label)}</p></article>''' for vid, label in POPULAR_VIDEOS)
    shorts_cards = "".join(f'''<article class="video-card short-video-card"><button class="video-poster" type="button" data-youtube-id="{esc(vid)}" data-youtube-title="{esc(label)}" aria-label="Play {esc(label)}"><img src="https://i.ytimg.com/vi/{esc(vid)}/hqdefault.jpg" alt="" loading="lazy" decoding="async"><span class="video-play-icon" aria-hidden="true">▶</span></button><p>{esc(label)}</p></article>''' for vid, label in YOUTUBE_SHORTS)
    instagram_cards = "".join(f'''<article class="video-card short-video-card instagram-reel-card"><div class="video-poster instagram-reel-poster"><img src="{esc(preview)}" alt="{esc(label)}" loading="eager" decoding="async"><a class="instagram-reel-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer" aria-label="Open {esc(label)} on Instagram"><span class="video-play-icon" aria-hidden="true">▶</span></a></div><p>{esc(label)}</p></article>''' for url, label, preview in INSTAGRAM_REELS)
    social_rail = f'''<aside class="social-rail" aria-label="Siddha365 social links"><span class="social-rail-label">Follow Siddha365</span><a href="{WHATSAPP}" target="_blank" rel="noopener noreferrer" aria-label="Message Siddha365 on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.6 4.2 1.7 6L.2 24l6.3-1.7a11.8 11.8 0 0 0 5.6 1.4h.1c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.3-6.2-3.5-8.4Zm-8.4 18.1h-.1a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4a9.8 9.8 0 1 1 8.4 4.6Zm5.4-7.3c-.3-.2-1.8-.9-2.1-1s-.5-.2-.7.2c-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-1.8-.9-3-1.6-4.2-3.6-.3-.5.3-.5.9-1.6.1-.2.1-.4 0-.6s-.7-1.7-.9-2.3c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.1 1.1-1.1 2.7s1.1 3.1 1.3 3.3c.2.2 2.2 3.4 5.3 4.7 2 .9 2.8 1 3.8.8.6-.1 1.8-.7 2.1-1.4.3-.7.3-1.3.2-1.4-.1-.2-.3-.3-.7-.5Z"/></svg><span>WhatsApp</span></a><a href="{YOUTUBE_CHANNEL}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on YouTube"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8ZM9.6 15.7V8.3l6.3 3.7-6.3 3.7Z"/></svg><span>YouTube</span></a><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on Instagram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7Zm5 3.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 0 1 12 7.5Zm0 2A2.5 2.5 0 1 0 14.5 12 2.5 2.5 0 0 0 12 9.5ZM17.5 6A1.2 1.2 0 1 1 16.3 7.2 1.2 1.2 0 0 1 17.5 6Z"/></svg><span>Instagram</span></a><a href="{FACEBOOK}" target="_blank" rel="noopener noreferrer" aria-label="Visit Siddha365 on Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-9h3l.5-3.5h-3.5V7.3c0-1 .3-1.8 1.9-1.8H17V2.3c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v3H7.5V13h2.8v9h3.2Z"/></svg><span>Facebook</span></a></aside>'''
    review_cards = review_rows_html(route)
    body = f'''<main id="main-content">{social_rail}
  <section class="home-gallery-section"><div class="hero-glow" data-hero-glow aria-hidden="true"></div><div class="hero-orbit" aria-hidden="true"></div><div class="container"><div class="home-hero-stage"><div class="home-gallery" data-carousel><div class="carousel-controls home-gallery-controls"><button class="icon-button" type="button" data-carousel-prev aria-label="Previous clinic image">←</button><button class="icon-button" type="button" data-carousel-next aria-label="Next clinic image">→</button></div><div class="home-gallery-track" data-carousel-track data-autoplay="true" data-autoplay-interval="3000" data-scroll-step="full" aria-label="Clinic treatments and care images">{slides}</div></div><div class="home-stage-shade" aria-hidden="true"></div><div class="home-hero-copy home-stage-copy"><p class="eyebrow">Traditional Siddha care · Chennai</p><h1>Thoughtful care, <span class="accent">rooted in tradition</span></h1><p>Meet Dr. Sindhu and explore personal care at Siddha365 Health Care Clinic.</p><div class="hero-actions home-hero-actions"><a class="button" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Book an appointment ↗</a><a class="button button-secondary" href="#specialized-care">Explore your care</a></div><div class="home-hero-details"><span>Dr. Sindhu V. · BSMS, MD (Siddha)</span><a href="contact-us/">Two locations in Chennai <span aria-hidden="true">↗</span></a></div></div><aside class="home-video-rail home-stage-videos" aria-label="Videos from the Siddha365 YouTube channel"><div class="home-video-rail-head"><div><p class="eyebrow">Watch &amp; learn</p><h2>From our <span class="accent">channel</span></h2></div><a class="text-link" href="{YOUTUBE_CHANNEL}" target="_blank" rel="noopener noreferrer">YouTube</a></div><div class="home-video-rail-window" data-video-rail><div class="home-video-rail-track" data-video-rail-track>{home_video_cards}</div></div></aside></div></div></section>

  <section class="section home-intro"><div class="container home-intro-grid"><div class="home-intro-copy reveal"><p class="eyebrow">Siddha 365 Health Care</p><h2>Traditional care rooted in <span class="accent">Tamil Siddha</span></h2><p class="home-tamil" lang="ta">பாரம்பரிய சித்த மருத்துவத்தின் மூலம் முழுமையான இயற்கை சிகிச்சை.</p><p>Siddha365 Health Care Clinic is guided by Dr. Sindhu V., B.S.M.S., M.D. (Siddha). Rooted in Tamil Siddha tradition, the clinic offers individual consultations with careful assessment, a respectful conversation about each person’s needs, and clear next steps.</p><div class="hero-actions"><a class="button" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Book an appointment ↗</a><a class="button button-secondary" href="about/">About the clinic</a></div></div><div class="home-intro-image reveal">{image_for(route, "wp-content/uploads/hero/tamil-siddha-herbal-prep.jpg", "Herbs and natural botanical remedies prepared using traditional Tamil Siddha methods")}</div></div></section>

  <section class="section home-care-section" id="specialized-care"><div class="container"><div class="section-head reveal"><div><p class="eyebrow">Specialized care by Dr. Sindhu V</p><h2>Find care that <span class="accent">speaks to you.</span></h2><p>Choose an area to explore helpful guides and your next step.</p></div><a class="text-link" href="treatments/">All 15 care guides</a></div>{explorer}</div></section>

  <section class="home-stats-band" aria-label="Siddha365 clinic statistics">{image_for(route, "wp-content/uploads/2023/05/IMG_20230517_195232-1-2048x1536.jpg", "", "home-stats-background", loading="lazy")}<div class="container home-stats-inner"><div class="home-stats-mobile-head"><img src="{asset(route, "assets/optimized/siddha365-brand-logo-new.png")}" alt="Siddha365" width="96" height="57"><span>SIDDHA 365 MILESTONES</span></div><div class="home-stats-grid">{stats}</div></div></section>

  <section class="section social-video-section desktop-social-video-section"><div class="container social-video-grid"><div class="video-section social-video-panel" data-carousel><div class="section-head reveal"><div><p class="eyebrow">Watch &amp; learn</p><h2>From the Siddha365 <span class="accent">YouTube Shorts</span></h2><p>Scroll through the clinic’s Shorts. Select a Short to play it here.</p></div><div class="video-section-desktop-social"><div class="carousel-controls"><button class="icon-button" type="button" data-carousel-prev aria-label="Scroll Shorts left">←</button><button class="icon-button" type="button" data-carousel-next aria-label="Scroll Shorts right">→</button><button class="icon-button" type="button" data-carousel-pause aria-pressed="false" aria-label="Pause automatic Shorts scrolling">Ⅱ</button></div></div></div><div class="video-track shorts-video-track" data-carousel-track data-scroll-step="full" data-autoplay="true" data-autoplay-interval="3500">{shorts_cards}</div></div><div class="video-section social-video-panel instagram-video-section" data-carousel><div class="section-head reveal"><div><p class="eyebrow">Follow the clinic</p><h2>See us on <span class="accent">Instagram</span></h2><p>Open the clinic’s latest reels and follow along on Instagram.</p></div><div class="video-section-desktop-social"><div class="carousel-controls"><button class="icon-button" type="button" data-carousel-prev aria-label="Scroll Instagram reels left">←</button><button class="icon-button" type="button" data-carousel-next aria-label="Scroll Instagram reels right">→</button><button class="icon-button" type="button" data-carousel-pause aria-pressed="false" aria-label="Pause automatic Instagram scrolling">Ⅱ</button></div></div></div><div class="video-track shorts-video-track" data-carousel-track data-scroll-step="full" data-autoplay="true" data-autoplay-interval="3500">{instagram_cards}</div></div></div></section>

  <section class="section video-section legacy-video-section"><div class="container carousel-shell" data-carousel><div class="section-head reveal"><div><p class="eyebrow">Watch &amp; learn</p><h2>From the Siddha365 <span class="accent">YouTube channel</span></h2><p>Scroll through clinic videos and health conversations. Select a video to play it here.</p></div><div class="carousel-controls"><button class="icon-button" type="button" data-carousel-prev aria-label="Scroll videos left">←</button><button class="icon-button" type="button" data-carousel-next aria-label="Scroll videos right">→</button><button class="icon-button" type="button" data-carousel-pause aria-pressed="false" aria-label="Pause automatic video scrolling">Ⅱ</button></div></div><div class="video-track" data-carousel-track data-autoplay="true">{video_cards}</div><p class="muted"><a class="text-link" href="{YOUTUBE_CHANNEL}" target="_blank" rel="noopener noreferrer">Visit the official YouTube channel</a></p></div></section>

  <section class="section home-reviews-section"><div class="container review-carousel" data-live-reviews-url="{REVIEWS_API}"><div class="section-head reveal home-review-heading"><img class="home-review-badge" src="{asset("", "assets/google-verified-reviews-transparent.png")}" width="1254" height="1254" alt="Google Verified Reviews badge" loading="lazy" decoding="async"><div><p class="eyebrow">Patient feedback</p><h2>Words from our <span class="accent">Patients</span></h2><p>Patient experiences from the clinic’s Google review feed. Select a card to read the full review.</p></div></div>{review_cards}<p class="muted review-feed-note" data-review-status aria-live="polite">Connecting to the clinic’s Google review feed…</p></div></section>

  <section class="section home-tradition-section"><div class="container home-tradition-grid"><div class="tradition-copy reveal"><p class="eyebrow">Siddha tradition</p><h2>Concept of Vatham, Pitham &amp; <span class="accent">Kabam</span></h2><p>Siddha tradition describes Vatham, Pitham, and Kabam as three principles used to discuss balance in health. This historical framework is part of Siddha practice; it does not replace medical testing or an individual clinical diagnosis.</p><div class="dosha-list"><article><strong>Vatham</strong><span>Traditionally associated with movement</span></article><article><strong>Pitham</strong><span>Traditionally associated with transformation</span></article><article><strong>Kabam</strong><span>Traditionally associated with structure</span></article></div></div><figure class="tradition-art reveal">{image_for(route, "wp-content/uploads/2026/02/vatham-pitham-kabam-premium.png", "Contemporary Siddha-inspired illustration representing Vatham, Pitham, and Kabam in balance")}</figure></div></section>

  <section class="section home-founder-section"><div class="container split-panel founder-panel"><div class="split-copy reveal"><p class="eyebrow">Founder &amp; Chief Siddha Consultant</p><h2><span class="accent">Dr. Sindhu V</span><small class="founder-registration">(Govt Reg. No. 6130)</small></h2><p>Dr. Sindhu V, B.S.M.S, M.D. (Siddha), H.A.H.M, DIP. CUPP, is the Founder and Chief Siddha Consultant at Siddha 365 Health Care Clinic. Her practice is guided by Siddha knowledge, clinical assessment, and patient-centred conversations.</p><ul class="check-list"><li>Women’s health, fertility, and family care</li><li>Skin, hair, joint, and lifestyle concerns</li><li>Traditional therapies discussed as part of an individual plan</li></ul><a class="button button-secondary" href="about/">Meet the clinic and doctor</a></div></div></section>
{treatment_wall_section(route)}
<section class="section home-visit-section"><div class="container visit-planner"><div><p class="eyebrow">Make your visit easier</p><h2>A little preparation.<br><span class="accent">A clearer conversation.</span></h2><p>Keep your questions ready and contact the clinic before you travel.</p><a class="button" href="contact-us/">Plan your visit <span aria-hidden="true">↗</span></a></div><div class="visit-planner-details"><article><span class="visit-step-number">01</span><div><h3>Choose your location</h3><p>Villivakkam or Mogappair East, Chennai.</p><a class="text-link" href="contact-us/">Locations &amp; directions</a></div></article><article><span class="visit-step-number">02</span><div><h3>Confirm your appointment</h3><p>Call the clinic for availability and opening hours.</p><a class="text-link" href="tel:{PHONE_TEL}">{PHONE}</a></div></article><article><span class="visit-step-number">03</span><div><h3>Bring what matters</h3><p>Your previous reports, current medicine list and questions for the clinician.</p></div></article></div></div></section>
</main>'''
    return page_shell(route, "Home", "Siddha365 Health Care Clinic in Chennai. Explore individual treatment guides, meet Dr. Sindhu V, and plan a clinic visit.", body, homepage=True)


def treatment_wall_section(route):
    treatment_rows = []
    for row in range(4):
        ordered = CONDITIONS[row * 3:] + CONDITIONS[:row * 3]
        pills = "".join(f'<span class="treatment-wall-pill">{esc(item["title"])}</span>' for item in ordered)
        treatment_rows.append(f'<div class="treatment-wall-row" data-treatment-row="{row}" aria-hidden="true">{pills}{pills}</div>')
    return '<section class="treatment-wall" aria-label="Explore our treatment guides" data-treatment-wall><div class="treatment-wall-rows">' + "".join(treatment_rows) + '</div><div class="treatment-wall-center"><a class="button treatment-wall-cta" href="' + rel(route, 'treatments') + '">Explore all<br>treatment guides <span aria-hidden="true">↗</span></a></div></section>'


def treatment_index():
    route = "treatments"
    cards = "".join(condition_card(route, item) for item in CONDITIONS)
    body = f'''<main id="main-content">
<section class="page-hero"><div class="container"><div class="page-hero-grid"><div class="reveal">{breadcrumb(route, "Treatments")}<p class="eyebrow">Browse by topic</p><h1>Choose a <span class="accent">care guide</span></h1><p class="lead">These pages are educational and do not diagnose or promise a cure. Please consult a qualified clinician for personal advice.</p></div><img class="page-hero-art treatment-heading-logo reveal" src="{asset(route, 'assets/optimized/siddha365-transparent-logo.png')}" alt="Siddha365 Health Care Clinic" loading="eager" decoding="async"></div></div></section>
<section class="section"><div class="container"><div class="card-grid">{cards}</div></div></section>
</main>'''
    return page_shell(route, "Treatments", "Browse separate Siddha365 care guide pages for health conditions and traditional therapies.", body, section="treatments")


def condition_page(condition):
    slug = "treatments/" + condition["slug"]
    title = condition["title"]
    source_links = "".join(f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} ↗</a>' for label, url in condition["sources"])
    bullets = "".join(f"<li>{esc(item)}</li>" for item in condition["care"])
    figure = image_for(slug, condition["image"], condition.get("image_alt", title), "page-hero-art reveal")
    body = f'''<main id="main-content"><section class="page-hero"><div class="container"><div class="page-hero-grid"><div class="reveal">{breadcrumb(slug, title)}<p class="eyebrow">{esc(condition['category'])} · Care guide</p><h1>{esc(title)}</h1><p class="lead">{esc(condition['intro'])}</p></div>{figure}</div></div></section>
<section class="section"><div class="container condition-layout"><div class="condition-content">
  <section class="prose-panel reveal"><h2>What it is</h2><p>{esc(condition['intro'])}</p></section>
  <section class="prose-panel reveal"><h2>{'Why people may consider it' if condition['category'] == 'Traditional therapy' else 'How it may develop'}</h2><p>{esc(condition['why'])}</p></section>
  <section class="prose-panel reveal"><h2>Care and treatment options</h2><ul>{bullets}</ul></section>
  <section class="prose-panel reveal"><h2>Learn more</h2><div class="source-list">{source_links}</div></section>
  <p class="medical-note"><strong>Important:</strong> This page is general health information, not a diagnosis or personal treatment plan. Do not stop or replace prescribed care. Before starting Siddha medicines, supplements, or a procedure, discuss it with your treating clinician and share your complete medicines list.</p>
</div><aside class="care-aside reveal"><p class="eyebrow">Talk to the clinic</p><h2 class="care-aside-title">Discuss your next step</h2><p>Share your concern with the clinic and ask whether an appointment is appropriate.</p><a class="button" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">Message on WhatsApp ↗</a><div class="safety-note"><strong>When to get help</strong><br>{esc(condition['safety'])}</div></aside></div></section>
<section class="section-tight"><div class="container carousel-shell" data-carousel><div class="section-head"><div><p class="eyebrow">Explore more</p><h2>More areas of <span class="accent">care</span></h2></div><div class="carousel-actions"><a class="text-link" href="{rel(slug, 'treatments')}">All treatments</a><div class="carousel-controls"><button class="icon-button" type="button" data-carousel-prev aria-label="Scroll care guides left">←</button><button class="icon-button" type="button" data-carousel-next aria-label="Scroll care guides right">→</button><button class="icon-button" type="button" data-carousel-pause aria-pressed="false" aria-label="Pause automatic care guide scrolling">Ⅱ</button></div></div></div><div class="condition-track" data-carousel-track data-autoplay="true" role="region" aria-label="More areas of care">{"".join(condition_card(slug, item) for item in CONDITIONS if item['slug'] != condition['slug'])}</div></div></section></main>'''
    return page_shell(slug, title, condition["intro"], body, section="treatments")


def generic_page(route, title, eyebrow, intro, content, image=None, section=None):
    if route == "reviews":
        body = f'<main id="main-content">{content}</main>'
        return page_shell(route, title, intro, body, section=section or route.split("/",1)[0])
    art = image_for(route, image, title, "page-hero-art reveal") if image else ""
    hero_class = "review-heading-grid" if route == "reviews" else ("page-hero-grid" if image else "")
    hero = f'''<section class="page-hero"><div class="container"><div class="{hero_class}"><div class="reveal">{breadcrumb(route, title)}<p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1><p class="lead">{esc(intro)}</p></div>{art}</div></div></section>'''
    body = f'<main id="main-content">{hero}{content}</main>'
    return page_shell(route, title, intro, body, section=section or route.split("/",1)[0])


def pages():
    output = {}
    output["index.html"] = homepage()
    output["treatments/index.html"] = treatment_index()
    for condition in CONDITIONS:
        route = "treatments/" + condition["slug"]
        output[route + "/index.html"] = condition_page(condition)

    about_content = f'''<section class="section"><div class="container split-panel"><div class="split-image reveal">{image_for("about", DOCTOR, HERO_ALT)}</div><div class="split-copy reveal"><p class="eyebrow">The clinic</p><h2>Traditional knowledge, delivered with <span class="accent">care and clarity</span></h2><p>Siddha365 Health Care Clinic is guided by Dr. Sindhu V., B.S.M.S., M.D. (Siddha), H.A.H.M., Dip. Cupp, Founder and Chief Siddha Consultant. The clinic offers Siddha consultations in Chennai with a focus on listening, individual assessment, and clear follow-up.</p><p>Care is discussed with attention to each person's history and current medicines. Patients are encouraged to ask questions, understand the limits of each option, and seek the right specialist care where needed.</p><ul class="check-list"><li>Women’s health, fertility, and family care</li><li>Skin, hair, joint, and lifestyle concerns</li><li>Traditional therapies discussed as part of an individual plan</li></ul><a class="button" href="{rel('about','contact-us')}">Clinic locations &amp; hours</a></div></div></section>
<section class="section-tight"><div class="container"><div class="feature-grid"><article class="feature-card"><span class="feature-icon" aria-hidden="true">◎</span><h3>Listen first</h3><p>Your concerns, goals, and medical history inform the conversation.</p></article><article class="feature-card"><span class="feature-icon" aria-hidden="true">✳</span><h3>Explain options</h3><p>Discuss what a treatment can and cannot do, along with alternatives.</p></article><article class="feature-card"><span class="feature-icon" aria-hidden="true">↗</span><h3>Work with your care team</h3><p>Share diagnoses and medicines so all clinicians can support safer decisions.</p></article></div></div></section>'''
    output["about/index.html"] = generic_page("about", "About Siddha365", "About us", "Meet the clinic and learn about the practitioner who leads Siddha365 Health Care Clinic.", about_content, LOGO, "about")

    treatment_images = [(c["image"], c["title"]) for c in CONDITIONS[:9]]
    treatment_images.extend([("wp-content/uploads/2024/07/oilslider-11-scaled.jpg", "Traditional oil therapy"), ("wp-content/uploads/2024/11/HERBAL-STEAM-BATH-scaled.jpg", "Herbal steam bath"), (DOCTOR, HERO_ALT)])
    gallery_items = "".join(f'<figure class="gallery-item reveal">{image_for("gallery", path, label)}<figcaption>{esc(label)}</figcaption></figure>' for path, label in treatment_images)
    gallery_content = f'<section class="section"><div class="container"><div class="gallery-grid">{gallery_items}</div><p class="medical-note">Clinic imagery is shared for general information. Individual treatment availability and suitability are decided after consultation.</p></div></section>'
    output["gallery/index.html"] = generic_page("gallery", "Clinic gallery", "At the clinic", "A look at Siddha365, traditional practice, and the clinic’s areas of care.", gallery_content, "assets/optimized/siddha365-transparent-logo.png", "gallery")


    review_cards = review_rows_html("reviews")
    reviews_content = f'''<section class="section"><div class="container review-carousel" data-live-reviews-url="{REVIEWS_API}"><div class="section-head review-section-heading"><div><p class="eyebrow">Patient feedback</p><h2>Latest Google <span class="accent">reviews</span></h2><p>Patient experiences from the clinic’s Google review feed. Select a card to read the full review.</p></div><img class="review-verified-badge" src="{asset('reviews', 'assets/google-verified-reviews-transparent.png')}" width="1254" height="1254" alt="Google Verified Reviews badge" loading="eager" decoding="async"></div>{review_cards}<p class="muted review-feed-note" data-review-status aria-live="polite">Connecting to the clinic’s Google review feed…</p><div class="review-source-panel"><div><h3>Reviews from Google</h3><p>Names, ratings and review text come from the clinic’s existing Google review feed. New feedback appears after that feed syncs with Google. Select a reviewer’s name to view their Google profile.</p><a class="text-link" href="{GOOGLE_SEARCH}" target="_blank" rel="noopener noreferrer">View the clinic on Google ↗</a></div></div></div></section>'''
    output["reviews/index.html"] = generic_page("reviews", "Google reviews", "Reviews", "Read patient feedback sourced from the clinic’s Google review feed.", reviews_content, None, "reviews")

    places = [
        ("Villivakkam", "No. 179, North Red Hills Road, near Subway, Villivakkam, Chennai, Tamil Nadu 600049."),
        ("Mogappair East", "No. 4/31, Pari Salai, Block 4, J.J. Nagar, Mogappair East, Chennai, Tamil Nadu 600037."),
    ]
    place_cards = "".join(f'''<article class="contact-card"><p class="eyebrow">Clinic {i}</p><h3>{esc(name)}</h3><p>{esc(address)}</p><a class="text-link" href="{MOGAPPAIR_MAP if name == 'Mogappair East' else 'https://www.google.com/maps/search/?api=1&amp;query=' + esc(address.replace(' ', '+'))}" target="_blank" rel="noopener noreferrer">Directions on Google Maps</a></article>''' for i, (name, address) in enumerate(places, start=1))
    contact_content = f'''<section class="section"><div class="container"><div class="contact-grid">{place_cards}<article class="contact-card"><p class="eyebrow">Call or message</p><h3>Plan an appointment</h3><p>Contact the clinic with questions about availability or directions.</p><div class="hero-actions"><a class="button" href="tel:{PHONE_TEL}">Call {PHONE}</a><a class="button button-secondary" href="{WHATSAPP}" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a></div></article><article class="contact-card" id="hours"><p class="eyebrow">Opening hours</p><h3>Clinic timings</h3><dl class="hours"><div><dt>Monday – Saturday</dt><dd>10:30 am – 1:30 pm</dd></div><div><dt>Evenings</dt><dd>7:00 pm – 9:30 pm</dd></div><div><dt>Sunday</dt><dd>By appointment</dd></div></dl></article></div><p class="medical-note">If you have a medical emergency, contact your local emergency service or go to the nearest emergency department.</p></div></section>'''
    output["contact-us/index.html"] = generic_page("contact-us", "Contact & Clinic Locations", "Visit Siddha365", "Find the Siddha365 Health Care Clinic locations in Villivakkam and Mogappair East, Chennai.", contact_content, "assets/optimized/siddha365-transparent-logo.png", "contact-us")

    return output


def optimize_embedded_images(generated):
    """Create small WebP copies for local page images and rewrite their src URLs."""
    if Image is None:
        return generated

    image_src = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")', re.IGNORECASE)
    optimized_dir = SITE / "assets" / "optimized"
    optimized_dir.mkdir(parents=True, exist_ok=True)
    outputs = {}

    for page_path, html in generated.items():
        page_dir = posixpath.dirname(page_path) or "."

        def replace_src(match):
            src = match.group(2)
            source_rel = posixpath.normpath(posixpath.join(page_dir, src))
            if not source_rel.startswith("wp-content/uploads/"):
                return match.group(0)
            source = SITE / Path(source_rel)
            if not source.is_file():
                return match.group(0)

            # Preserve original partner artwork without another lossy conversion.
            if source_rel in {path for path, _ in PARTNER_LOGOS}:
                return match.group(0)

            digest = hashlib.sha1(source_rel.encode("utf-8")).hexdigest()[:16]
            detailed_artwork = source_rel == "wp-content/uploads/2026/02/vatham-pitham-kabam-premium.png"
            webp_rel = f"assets/optimized/{digest}-hq.webp" if detailed_artwork else f"assets/optimized/{digest}-v2.webp"
            optimized = SITE / Path(webp_rel)
            if webp_rel not in outputs:
                outputs[webp_rel] = optimized
                if not optimized.exists() or source.stat().st_mtime > optimized.stat().st_mtime:
                    with Image.open(source) as original:
                        image = ImageOps.exif_transpose(original)
                        image.thumbnail((1080, 1080), Image.Resampling.LANCZOS)
                        if "A" in image.getbands():
                            image = image.convert("RGBA")
                        else:
                            image = image.convert("RGB")
                        quality = 90 if detailed_artwork else 75
                        image.save(optimized, "WEBP", quality=quality, method=5)

            target = posixpath.relpath(webp_rel, page_dir)
            return f'{match.group(1)}{target}{match.group(3)}'

        optimized_html = image_src.sub(replace_src, html)

        def dimensions(match):
            tag = match.group(0)
            if re.search(r"\bwidth=", tag):
                return tag
            image_path = re.search(r'src="([^"]+)"', tag).group(1)
            if urlsplit(image_path).scheme:
                return tag
            local = SITE / posixpath.normpath(posixpath.join(page_dir, image_path))
            if not local.is_file():
                return tag
            if local.suffix.lower() == ".svg":
                return tag
            with Image.open(local) as picture:
                width, height = picture.size
            return tag[:-1] + f' width="{width}" height="{height}">'

        generated[page_path] = re.sub(r'<img\b[^>]*>', dimensions, optimized_html)
    return generated


def build_distribution(generated):
    """Assemble a clean static deploy folder without the downloaded WordPress snapshot."""
    distribution = SITE / "dist"
    # Reject redirected output trees before writing or pruning anything.
    if distribution.resolve() != SITE / "dist" or distribution.is_symlink() or distribution.is_junction():
        raise ValueError("The deployment folder must be a real directory inside the project")
    for entry in distribution.rglob("*"):
        if entry.is_symlink() or entry.is_junction() or not entry.resolve().is_relative_to(distribution):
            raise ValueError("Linked paths are not allowed in the deployment folder")
    allowed_extensions = {".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico", ".woff", ".woff2"}
    assets = {}
    # The Founder leaf is referenced from refinement.css, so it is not
    # discovered by the HTML src/href scan above. Publish it explicitly.
    founder_leaf = SITE / "assets/doctor-founder-option5-leaf.png"
    if founder_leaf.is_file():
        assets["assets/doctor-founder-option5-leaf.png"] = founder_leaf
    desktop_slider_dir = SITE / "assets/home-slider-desktop"
    if desktop_slider_dir.is_dir():
        for desktop_slider in desktop_slider_dir.glob("*.png"):
            assets[f"assets/home-slider-desktop/{desktop_slider.name}"] = desktop_slider
    # Validate the entire input manifest before changing the deployment output.
    for page_path, content in generated.items():
        page = Path(page_path)
        if page.is_absolute() or ".." in page.parts or page.suffix != ".html":
            raise ValueError("Invalid generated page path")
        for match in re.finditer(r'\b(?:src|href)=["\']([^"\']+)["\']', content, re.IGNORECASE):
            parsed = urlsplit(match.group(1))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            raw = unquote(parsed.path)
            if "\\" in raw or "\x00" in raw:
                raise ValueError("Invalid local asset path")
            local = posixpath.normpath(raw.lstrip("/") if raw.startswith("/") else posixpath.join(posixpath.dirname(page_path), raw))
            source = (SITE / local).resolve()
            if not source.is_relative_to(SITE) or local.startswith("../"):
                raise ValueError("Local reference escapes the project")
            if local in generated or local.rstrip("/") + "/index.html" in generated or local == ".":
                continue
            if Path(local).suffix.lower() not in allowed_extensions or any(part.startswith(".") for part in Path(local).parts):
                raise ValueError("Non-public file referenced by a generated page")
            if not source.is_file():
                raise FileNotFoundError("Missing public asset: " + local)
            assets[local] = source
    distribution.mkdir(exist_ok=True)
    published_paths = set(generated)

    for relative_path, content in generated.items():
        destination = distribution / Path(relative_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    for local_path, source in assets.items():
        destination = distribution / local_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        published_paths.add(local_path)

    security_headers = """/*
  Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'; script-src 'self'; style-src 'self'; img-src 'self' https://i.ytimg.com; font-src 'self'; connect-src 'self' https://siddha365.com; frame-src https://www.youtube-nocookie.com https://maps.google.com https://www.google.com; upgrade-insecure-requests
  Referrer-Policy: strict-origin-when-cross-origin
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), autoplay=(self \"https://www.youtube-nocookie.com\")
"""
    (distribution / "_headers").write_text(security_headers, encoding="utf-8")
    apache_headers = '''Options -Indexes
<FilesMatch "(?i)^(?:\\..*|_headers|.*\\.(?:py|pyc|php|env|ini|log|sql|bak|key|pem|p12|pfx))$">
  Require all denied
</FilesMatch>
<IfModule mod_headers.c>
  Header always set Content-Security-Policy "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self'; script-src 'self'; style-src 'self'; img-src 'self' https://i.ytimg.com; font-src 'self'; connect-src 'self' https://siddha365.com; frame-src https://www.youtube-nocookie.com https://maps.google.com https://www.google.com; upgrade-insecure-requests"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "DENY"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(), usb=(), autoplay=(self \\"https://www.youtube-nocookie.com\\")"
  Header always set Strict-Transport-Security "max-age=31536000"
  Header always unset X-Powered-By
</IfModule>
'''
    (distribution / ".htaccess").write_text(apache_headers, encoding="utf-8")
    (distribution / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: https://siddha365.com/sitemap.xml\n",
        encoding="utf-8",
    )
    urls = []
    for page_path in sorted(published_paths):
        if not page_path.endswith("index.html"):
            continue
        route = page_path[:-len("index.html")]
        urls.append(f"  <url><loc>{escape('https://siddha365.com/' + route)}</loc></url>")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(urls) + "\n</urlset>\n"
    (distribution / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    published_paths.update({"_headers", ".htaccess", "robots.txt", "sitemap.xml"})
    # Only remove stale deployment copies, after all new files have been written.
    # Source originals and reference materials remain outside this folder.
    for entry in sorted(distribution.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        if not entry.resolve().is_relative_to(distribution):
            raise ValueError("Refusing to prune outside the deployment folder")
        if entry.is_file() and entry.relative_to(distribution).as_posix() not in published_paths:
            entry.unlink()
        elif entry.is_dir() and not any(entry.iterdir()):
            entry.rmdir()
    return len(published_paths)


def main():
    generated = optimize_embedded_images(pages())
    for relative_path, content in generated.items():
        destination = SITE / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
    distribution_files = build_distribution(generated)
    print(f"Generated {len(generated)} static pages and a clean distribution ({distribution_files} files) under {SITE / 'dist'}")


if __name__ == "__main__":
    main()
























