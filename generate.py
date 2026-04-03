#!/usr/bin/env python3
"""
COMUNIKOO — Static Site Generator
Generates ~200 HTML pages from page data definitions.
Pure Python, no dependencies.
"""
import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR
sys.path.insert(0, str(BASE_DIR))

# Import content modules
def load_content_pages():
    """Load full-content page data from content/ directory"""
    pages = {}
    verticals = {}
    content_dir = BASE_DIR / 'content'
    if content_dir.exists():
        for f in content_dir.glob('*.py'):
            if f.name.startswith('__'):
                continue
            mod_name = f.stem
            spec = __import__(f'content.{mod_name}', fromlist=['PAGE_DATA', 'VERTICAL_CONTENT'])
            if hasattr(spec, 'PAGE_DATA'):
                pd = spec.PAGE_DATA
                pages[pd['url']] = pd
                print(f"  [content] Loaded service content: {pd['url']}")
            if hasattr(spec, 'VERTICAL_CONTENT'):
                verticals.update(spec.VERTICAL_CONTENT)
                print(f"  [content] Loaded {len(spec.VERTICAL_CONTENT)} vertical pages")
    return pages, verticals

# ============================================================
# TEMPLATES
# ============================================================

def base_html(title, meta_desc, canonical, body, breadcrumbs="", schema=""):
    """Base HTML template wrapping all pages"""
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://comunikoo.es{canonical}">
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/style.css?v=6">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://comunikoo.es{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
{schema}
</head>
<body>
<a href="#main" class="skip">Ir al contenido</a>

{header_html()}

<div class="mobile-nav-overlay" aria-hidden="true"></div>
{mobile_nav_html()}

<main id="main">
{breadcrumbs}
{body}
</main>

{footer_html()}

<script defer src="/js/main.js"></script>
</body>
</html>'''


def header_html():
    return '''<header class="hdr">
<div class="hdr-in">
<a href="/" class="logo"><span class="logo-dot"></span>COMUNIKOO</a>
<nav>
<ul class="nav">
<li class="nav-item"><a href="/servicios/">Servicios</a>
<div class="nav-dropdown">
<div class="nav-dropdown-col">
<h4>SEO</h4>
<a href="/agencia-seo/">Agencia SEO</a>
<a href="/servicios/agencia-seo-local/">SEO Local</a>
<a href="/servicios/consultoria-seo/">Consultoría SEO</a>
<a href="/servicios/auditoria-seo/">Auditoría SEO</a>
<a href="/servicios/posicionamiento-web/">Posicionamiento Web</a>
<a href="/servicios/linkbuilding/">Linkbuilding</a>
</div>
<div class="nav-dropdown-col">
<h4>Diseño Web</h4>
<a href="/diseno-web/">Diseño Web</a>
<a href="/servicios/diseno-web-wordpress/">Diseño WordPress</a>
<a href="/tienda-online/">Tiendas Online</a>
<a href="/servicios/desarrollo-web/">Desarrollo Web</a>
<a href="/servicios/landing-pages/">Landing Pages</a>
<a href="/servicios/mantenimiento-web/">Mantenimiento Web</a>
<a href="/servicios/optimizacion-cro/">CRO</a>
</div>
<div class="nav-dropdown-col">
<h4>Publicidad</h4>
<a href="/agencia-google-ads/">Google Ads</a>
<a href="/servicios/agencia-facebook-ads/">Facebook Ads</a>
<a href="/servicios/instagram-ads/">Instagram Ads</a>
<a href="/servicios/agencia-meta-ads/">Meta Ads</a>
<a href="/servicios/youtube-ads/">YouTube Ads</a>
<a href="/servicios/publicidad-en-google/">Publicidad Google</a>
<a href="/servicios/google-shopping/">Google Shopping</a>
</div>
<div class="nav-dropdown-col">
<h4>Redes Sociales</h4>
<a href="/community-manager/">Community Manager</a>
<a href="/servicios/gestion-redes-sociales/">Gestión Redes</a>
<a href="/servicios/marketing-de-contenidos/">Marketing Contenidos</a>
<a href="/email-marketing/">Email Marketing</a>
</div>
</div>
</li>
<li class="nav-item"><a href="#">Sectores</a>
<div class="nav-dropdown" style="min-width:520px;grid-template-columns:repeat(3,1fr)">
<div class="nav-dropdown-col">
<h4>Hostelería y Salud</h4>
<a href="/marketing-para-restaurantes/">Restaurantes</a>
<a href="/marketing-para-hoteles/">Hoteles</a>
<a href="/marketing-para-clinicas-dentales/">Clínicas Dentales</a>
<a href="/marketing-para-clinicas-esteticas/">Clínicas Estéticas</a>
<a href="/marketing-para-psicologos/">Psicólogos</a>
<a href="/marketing-para-veterinarias/">Veterinarias</a>
</div>
<div class="nav-dropdown-col">
<h4>Servicios y Local</h4>
<a href="/marketing-para-abogados/">Abogados</a>
<a href="/marketing-para-asesorias/">Asesorías</a>
<a href="/marketing-para-inmobiliarias/">Inmobiliarias</a>
<a href="/marketing-para-empresas-de-reformas/">Reformas</a>
<a href="/marketing-para-autoescuelas/">Autoescuelas</a>
<a href="/marketing-para-talleres-de-coches/">Talleres</a>
</div>
<div class="nav-dropdown-col">
<h4>Empresas</h4>
<a href="/marketing-para-ecommerce/">Ecommerce</a>
<a href="/marketing-para-empresas-b2b/">Empresas B2B</a>
<a href="/marketing-para-gimnasios/">Gimnasios</a>
<a href="/marketing-para-academias/">Academias</a>
</div>
</div>
</li>
<li><a href="/blog/">Blog</a></li>
<li><a href="/nosotros/">Nosotros</a></li>
</ul>
</nav>
<a href="/contacto/" class="btn btn-p hdr-cta">Auditoría gratis</a>
<button class="hamburger" aria-label="Abrir menú">
<span></span><span></span><span></span>
</button>
</div>
</header>'''




def mobile_nav_html():
    return '''<nav class="mobile-nav" aria-label="Menú móvil">
<button class="mobile-nav-close" aria-label="Cerrar menú">&times;</button>
<ul>
<li><a href="/servicios/">Servicios</a></li>
<li><a href="/agencia-seo/">Agencia SEO</a></li>
<li><a href="/diseno-web/">Diseño Web</a></li>
<li><a href="/agencia-google-ads/">Google Ads</a></li>
<li><a href="/community-manager/">Community Manager</a></li>
<li><a href="/tienda-online/">Tiendas Online</a></li>
<li><a href="#">Sectores</a></li>
<li><a href="/blog/">Blog</a></li>
<li><a href="/nosotros/">Nosotros</a></li>
<li><a href="/agencia-marketing-digital-barcelona/">Barcelona</a></li>
<li><a href="/agencia-marketing-digital-madrid/">Madrid</a></li>
<li><a href="/contacto/" class="btn btn-primary" style="margin-top:1rem">Contacto</a></li>
</ul>
</nav>'''


def footer_html():
    return '''<footer class="ft">
<div class="ft-grid">
<div class="ft-info">
<a href="/" class="logo"><span class="logo-dot"></span>COMUNIKOO</a>
<p>Agencia de Marketing Digital en Barcelona. Expertos en SEO, SEM y Resultados.</p>
<p>📍 Aragó 4, Barcelona 08015</p>
<p>📞 <a href="tel:+34608721015">+34 608 721 015</a></p>
<p>📧 <a href="mailto:hola@comunikoo.es">hola@comunikoo.es</a></p>
</div>
<div>
<h4>Servicios</h4>
<ul>
<li><a href="/agencia-seo/">Agencia SEO</a></li>
<li><a href="/servicios/agencia-seo-local/">SEO Local</a></li>
<li><a href="/diseno-web/">Diseño Web</a></li>
<li><a href="/servicios/diseno-web-wordpress/">Diseño WordPress</a></li>
<li><a href="/tienda-online/">Tiendas Online</a></li>
<li><a href="/agencia-google-ads/">Google Ads</a></li>
<li><a href="/servicios/agencia-facebook-ads/">Facebook Ads</a></li>
<li><a href="/community-manager/">Community Manager</a></li>
<li><a href="/email-marketing/">Email Marketing</a></li>
<li><a href="/servicios/branding/">Branding</a></li>
</ul>
</div>
<div>
<h4>Ciudades</h4>
<ul>
<li><a href="/agencia-marketing-digital-barcelona/">Barcelona</a></li>
<li><a href="/agencia-marketing-digital-madrid/">Madrid</a></li>
</ul>
<h4 style="margin-top:1.5rem">Recursos</h4>
<ul>
<li><a href="/blog/">Blog</a></li>
<li><a href="/casos-de-exito/">Casos de Éxito</a></li>
</ul>
</div>
<div>
<h4>Sectores</h4>
<ul>
<li><a href="/marketing-para-restaurantes/">Restaurantes</a></li>
<li><a href="/marketing-para-hoteles/">Hoteles</a></li>
<li><a href="/marketing-para-clinicas-dentales/">Clínicas Dentales</a></li>
<li><a href="/marketing-para-abogados/">Abogados</a></li>
<li><a href="/marketing-para-inmobiliarias/">Inmobiliarias</a></li>
<li><a href="/marketing-para-gimnasios/">Gimnasios</a></li>
<li><a href="/marketing-para-ecommerce/">Ecommerce</a></li>
<li><a href="/marketing-para-empresas-b2b/">B2B</a></li>
</ul>
</div>
</div>
<div class="ft-btm">
<span>&copy; 2026 Comunikoo. Todos los derechos reservados.</span>
<div>
<a href="/politica-de-privacidad/">Privacidad</a> ·
<a href="/aviso-legal/">Aviso Legal</a> ·
<a href="/politica-de-cookies/">Cookies</a> ·
<a href="/sitemap.xml">Sitemap</a>
</div>
</div>
</footer>'''


def breadcrumb_html(items):
    """items: list of (label, url) tuples. Last one is current page (no link)"""
    schema_items = []
    parts = ['<nav class="breadcrumbs wrap" aria-label="Breadcrumb">']
    for i, (label, url) in enumerate(items):
        if i > 0:
            parts.append('<span>›</span>')
        if i < len(items) - 1:
            parts.append(f'<a href="{url}">{label}</a>')
        else:
            parts.append(f'<span aria-current="page">{label}</span>')
        schema_items.append(f'{{"@type":"ListItem","position":{i+1},"name":"{label}","item":"https://comunikoo.es{url}"}}')
    parts.append('</nav>')
    return '\n'.join(parts)


def faq_html(faqs):
    """faqs: list of (question, answer) tuples"""
    h = '<div class="faq">\n'
    for q, a in faqs:
        h += f'<details>\n<summary>{q}</summary>\n<p>{a}</p>\n</details>\n'
    h += '</div>'
    return h


def faq_schema(faqs):
    items = []
    for q, a in faqs:
        items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(items)}]}}
</script>'''


def service_schema(name, desc):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{name}","description":"{desc}","provider":{{"@type":"Organization","name":"Comunikoo","url":"https://comunikoo.es","address":{{"@type":"PostalAddress","streetAddress":"Aragó 4","addressLocality":"Barcelona","postalCode":"08015","addressCountry":"ES"}},"telephone":"+34608721015"}},"areaServed":{{"@type":"Country","name":"España"}}}}
</script>'''


def local_business_schema(city, service_name):
    address = "Aragó 4" if city == "Barcelona" else ""
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LocalBusiness","name":"Comunikoo - {service_name} {city}","address":{{"@type":"PostalAddress","addressLocality":"{city}","addressCountry":"ES"}},"telephone":"+34608721015","url":"https://comunikoo.es","openingHours":"Mo-Fr 09:00-20:00"}}
</script>'''


# ============================================================
# PAGE BUILDERS
# ============================================================

def build_home():
    body = '''
<!-- HERO: Centered, gradient text, badge, orbs -->
<section class="section-glow" style="padding:var(--s32) 0 var(--s20);text-align:center">
<div class="wrap" style="position:relative;z-index:1">
<div class="badge" style="margin-bottom:var(--s6)">Agencia de Marketing Digital en Barcelona</div>
<h1 style="font-size:var(--text-hero);max-width:18ch;margin:0 auto;line-height:1.05">
Posicionamos negocios<br><span class="text-gradient">donde sus clientes los buscan</span>
</h1>
<p style="font-size:var(--text-lg);color:var(--text-secondary);max-width:50ch;margin:var(--s6) auto 0">
SEO, Diseño Web, Google Ads y Redes Sociales. Resultados medibles. Sin permanencia. Dashboard en tiempo real.
</p>
<div style="display:flex;gap:var(--s4);justify-content:center;margin-top:var(--s8);flex-wrap:wrap">
<a href="/contacto/" class="btn btn-primary btn-lg">Auditoría gratuita</a>
<a href="/servicios/" class="btn btn-outline btn-lg">Ver servicios</a>
</div>
</div>
</section>

<!-- STATS: Bento grid -->
<section class="section" style="padding-top:0">
<div class="wrap">
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s4)" class="bento-stats">
<div class="card" style="text-align:center;padding:var(--s8)">
<div class="stat-number gradient" style="font-size:var(--text-4xl)">+320%</div>
<div class="stat-label">tráfico orgánico medio</div>
</div>
<div class="card" style="text-align:center;padding:var(--s8)">
<div class="stat-number gradient" style="font-size:var(--text-4xl)">5.8M€</div>
<div class="stat-label">gestionados en campañas</div>
</div>
<div class="card" style="text-align:center;padding:var(--s8)">
<div class="stat-number gradient" style="font-size:var(--text-4xl)">98%</div>
<div class="stat-label">clientes satisfechos</div>
</div>
<div class="card" style="text-align:center;padding:var(--s8)">
<div class="stat-number gradient" style="font-size:var(--text-4xl)">487</div>
<div class="stat-label">proyectos entregados</div>
</div>
</div>
<style>.bento-stats{grid-template-columns:repeat(4,1fr)}@media(max-width:768px){.bento-stats{grid-template-columns:repeat(2,1fr)}}</style>
</div>
</section>

<!-- LOGOS -->
<section style="padding:var(--s8) 0 var(--s16)">
<div class="wrap">
<p style="font-size:var(--text-xs);color:var(--text-tertiary);text-align:center;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:var(--s6)">Confían en nosotros</p>
<div class="logos">
<span>Empresa 1</span><span>Empresa 2</span><span>Empresa 3</span>
<span>Empresa 4</span><span>Empresa 5</span><span>Empresa 6</span>
</div>
</div>
</section>

<!-- SERVICES: Bento cards grid -->
<section class="section section-dots">
<div class="wrap">
<div style="text-align:center;margin-bottom:var(--s10)">
<div class="badge" style="margin-bottom:var(--s4)">Servicios</div>
<h2 class="mt-0">Todo lo que tu negocio necesita para<br><span class="text-gradient">dominar el mundo digital</span></h2>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4)" class="bento-services">
<a href="/agencia-seo/" class="card" style="grid-row:span 2;text-decoration:none;display:flex;flex-direction:column;justify-content:space-between">
<div>
<div class="feature-icon">S</div>
<h3>SEO y Posicionamiento Web</h3>
<p>Posicionamos tu negocio en las primeras posiciones de Google. Estrategia probada con resultados medibles y tráfico orgánico que crece cada mes.</p>
</div>
<span class="link-arrow" style="margin-top:var(--s4)">Explorar servicio</span>
</a>
<a href="/diseno-web/" class="card" style="text-decoration:none">
<div class="feature-icon">W</div>
<h3>Diseño Web & WordPress</h3>
<p>Webs rápidas y que venden. Sin plantillas genéricas.</p>
<span class="link-arrow" style="margin-top:var(--s3)">Ver más</span>
</a>
<a href="/servicios/agencia-ecommerce/" class="card" style="text-decoration:none">
<div class="feature-icon">E</div>
<h3>Tiendas Online</h3>
<p>Shopify, WooCommerce, PrestaShop. Ecommerce que vende.</p>
<span class="link-arrow" style="margin-top:var(--s3)">Ver más</span>
</a>
<a href="/agencia-google-ads/" class="card" style="text-decoration:none">
<div class="feature-icon">A</div>
<h3>Google Ads & SEM</h3>
<p>Campañas rentables. Cada euro invertido, medido.</p>
<span class="link-arrow" style="margin-top:var(--s3)">Ver más</span>
</a>
<a href="/community-manager/" class="card" style="text-decoration:none">
<div class="feature-icon">R</div>
<h3>Redes Sociales</h3>
<p>Community manager, social ads y contenido que convierte.</p>
<span class="link-arrow" style="margin-top:var(--s3)">Ver más</span>
</a>
</div>
<style>.bento-services{grid-template-columns:repeat(3,1fr)}@media(max-width:768px){.bento-services{grid-template-columns:1fr}.bento-services .card{grid-row:auto!important}}</style>
</div>
</section>

<!-- TESTIMONIAL: Glass card with glow -->
<section class="section-glow">
<div class="wrap" style="max-width:800px;margin:0 auto;position:relative;z-index:1">
<div style="text-align:center;margin-bottom:var(--s8)">
<div class="badge badge" style="margin-bottom:var(--s4)">Casos de éxito</div>
<h2 class="mt-0">Resultados que hablan por sí solos</h2>
</div>
<div class="testimonial-block">
<p class="testimonial-text">"Pasamos de 200 a 3.400 visitas orgánicas al mes en 6 meses. Comunikoo entiende de negocio, no solo de SEO."</p>
<div class="testimonial-author">
<div class="testimonial-avatar">ML</div>
<div><div class="testimonial-name">María López</div><div class="testimonial-role">CEO, Empresa X — Barcelona</div></div>
</div>
</div>
<div class="stats" style="margin-top:var(--s8)">
<div style="text-align:center"><div class="stat-number success">+1.600%</div><div class="stat-label">tráfico orgánico</div></div>
<div style="text-align:center"><div class="stat-number success">12 → 1</div><div class="stat-label">posición en Google</div></div>
<div style="text-align:center"><div class="stat-number success">34</div><div class="stat-label">leads/mes</div></div>
</div>
<div style="text-align:center;margin-top:var(--s8)">
<a href="/casos-de-exito/" class="link-arrow">Ver todos los casos de éxito</a>
</div>
</div>
</section>

<!-- SECTORS: Cards scroll -->
<section class="section">
<div class="wrap">
<div style="text-align:center;margin-bottom:var(--s8)">
<div class="badge" style="margin-bottom:var(--s4)">Especialización</div>
<h2 class="mt-0">Expertos en tu sector</h2>
<p style="color:var(--text-secondary);max-width:45ch;margin:var(--s3) auto 0">Conocemos los retos de tu industria. Estrategias específicas para cada negocio.</p>
</div>
<div class="cards-scroll">
''' + ''.join([build_sector_card(s,d,u) for s,d,u in [
    ("Restaurantes", "Llenamos tu local con clientes que buscan en Google.", "/marketing-para-restaurantes/"),
    ("Clínicas Dentales", "+300% en captación de pacientes.", "/marketing-para-clinicas-dentales/"),
    ("Abogados", "El 96% busca abogado en Google.", "/marketing-para-abogados/"),
    ("Ecommerce", "Solo el 3% de tiendas online son rentables.", "/marketing-para-ecommerce/"),
    ("Hoteles", "Más reservas directas, menos comisiones.", "/marketing-para-hoteles/"),
    ("Gimnasios", "Más socios todo el año, no solo en enero.", "/marketing-para-gimnasios/"),
    ("Inmobiliarias", "Leads de compradores y vendedores.", "/marketing-para-inmobiliarias/"),
    ("Clínicas Estéticas", "Captación de pacientes premium.", "/marketing-para-clinicas-esteticas/"),
]]) + '''
</div>
</div>
</section>

<!-- WHY US: Feature bento -->
<section class="section section-dots">
<div class="wrap">
<div style="text-align:center;margin-bottom:var(--s10)">
<div class="badge" style="margin-bottom:var(--s4)">¿Por qué Comunikoo?</div>
<h2 class="mt-0">Lo que nos hace <span class="text-gradient">diferentes</span></h2>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--s4)" class="bento-why">
<div class="card" style="grid-column:span 2;display:flex;align-items:center;gap:var(--s8);padding:var(--s8)">
<div style="flex-shrink:0">
<div style="font-size:var(--text-hero);font-weight:900;line-height:1" class="text-gradient">0€</div>
</div>
<div>
<h3 style="margin-top:0">Sin permanencia</h3>
<p style="margin:0">Nos ganamos tu confianza mes a mes con resultados. Si no estás contento, te vas. El 98% se queda más de 12 meses — porque funciona, no porque estén obligados.</p>
</div>
</div>
<div class="card" style="padding:var(--s8)">
<div class="feature-icon">⚡</div>
<h3>Dashboard en tiempo real</h3>
<p>Nada de PDFs mensuales. Tus datos 24/7: posiciones, tráfico, conversiones.</p>
</div>
<div class="card" style="padding:var(--s8)">
<div class="feature-icon">📈</div>
<h3>Enfocados en tu ROI</h3>
<p>Medimos éxito en leads, ventas y facturación. No vanity metrics.</p>
</div>
<div class="card" style="padding:var(--s8)">
<div class="feature-icon">👤</div>
<h3>Equipo senior</h3>
<p>Consultor senior asignado a tu proyecto. +5 años de experiencia.</p>
</div>
<div class="card" style="padding:var(--s8)">
<div class="feature-icon">🏆</div>
<h3>+487 proyectos</h3>
<p>+30 sectores: salud, legal, hostelería, ecommerce, SaaS, B2B.</p>
</div>
</div>
<style>.bento-why{grid-template-columns:repeat(3,1fr)}@media(max-width:768px){.bento-why{grid-template-columns:1fr}.bento-why .card{grid-column:auto!important}}</style>
</div>
</section>

<!-- LOCATIONS -->
<section class="section">
<div class="wrap">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--s4)" class="bento-loc">
<a href="/agencia-marketing-digital-barcelona/" class="card" style="padding:var(--s10);text-decoration:none">
<div style="font-size:var(--text-3xl);font-weight:800;color:var(--text);margin-bottom:var(--s2)">Barcelona</div>
<p style="color:var(--text-secondary);margin-bottom:var(--s4)">Oficina central — Aragó 4, 08015</p>
<span class="link-arrow">Servicios en Barcelona</span>
</a>
<a href="/agencia-marketing-digital-madrid/" class="card" style="padding:var(--s10);text-decoration:none">
<div style="font-size:var(--text-3xl);font-weight:800;color:var(--text);margin-bottom:var(--s2)">Madrid</div>
<p style="color:var(--text-secondary);margin-bottom:var(--s4)">Presencia activa en la capital</p>
<span class="link-arrow">Servicios en Madrid</span>
</a>
</div>
<style>@media(max-width:640px){.bento-loc{grid-template-columns:1fr}}</style>
</div>
</section>

<!-- CTA: Gradient glow -->
<section class="section">
<div class="wrap">
<div class="cta-block">
<h2 style="font-size:var(--text-3xl)">¿Listo para que tu negocio<br><span style="color:var(--accent)">domine Google?</span></h2>
<p>Solicita tu auditoría gratuita. Analizamos tu web y tu competencia sin compromiso.</p>
<div style="display:flex;gap:var(--s4);justify-content:center;flex-wrap:wrap">
<a href="/contacto/" class="btn btn-primary btn-lg">Solicita tu auditoría gratuita</a>
<a href="tel:+34608721015" class="btn btn-outline btn-lg">+34 608 721 015</a>
</div>
</div>
</div>
</section>
'''
    schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Comunikoo","url":"https://comunikoo.es","logo":"https://comunikoo.es/img/logo.svg","address":{"@type":"PostalAddress","streetAddress":"Aragó 4","addressLocality":"Barcelona","postalCode":"08015","addressCountry":"ES"},"telephone":"+34608721015","email":"hola@comunikoo.es","sameAs":[]}
</script>'''
    return base_html(
        "Agencia de Marketing Digital Barcelona | SEO, Diseño Web y Google Ads — Comunikoo",
        "Agencia de marketing digital en Barcelona. Expertos en SEO, diseño web, Google Ads y redes sociales. Resultados reales. Sin permanencia. Auditoría gratuita.",
        "/", body, schema=schema
    )


def build_service_list(services):
    h = ''
    for num, title, desc, url in services:
        h += f'''<a href="{url}" class="svc-item anim">
<div class="svc-num">{num}</div>
<div class="svc-info"><h3>{title}</h3><p>{desc}</p></div>
<div class="svc-arr">→</div>
</a>\n'''
    return h


def build_sector_card(title, desc, url):
    return f'''<a href="{url}" class="gc anim" style="text-decoration:none">
<h3>{title}</h3>
<p>{desc}</p>
<span class="arr">Ver más</span>
</a>\n'''


def build_service_page(page):
    """Build a service page — LANDING PAGE style, transactional"""
    p = page
    sections_data = p.get('sections', [])
    faqs = p.get('faqs', [])
    faq_schema_tag = faq_schema(faqs) if faqs else ''

    # Sidebar nav
    sidebar_nav = ''
    for s in sections_data:
        sidebar_nav += f'<li><a href="#{s["id"]}">{s["nav_label"]}</a></li>\n'

    # Sidebar stats
    sidebar_stats = ''
    for stat in p.get('sidebar_stats', []):
        sidebar_stats += f'<div class="ss"><div class="st-n tg">{stat["number"]}</div><div class="st-l">{stat["label"]}</div></div>\n'

    # Main content sections
    content = ''
    for i, s in enumerate(sections_data):
        cls = ' class="mt0"' if i == 0 else ''
        content += f'<h2 id="{s["id"]}"{cls}>{s["title"]}</h2>\n'
        content += s.get('html', '<p>[Contenido pendiente de redacción]</p>') + '\n'

    # FAQ
    if faqs:
        content += '<h2 id="faq">Preguntas frecuentes</h2>\n'
        content += faq_html(faqs)

    # CTA
    content += f'''
<div class="cta-b" style="margin-top:var(--s16)">
<h2>{p.get("cta_title", "¿Empezamos?")}</h2>
<p>{p.get("cta_desc", "Solicita tu auditoría gratuita y descubre cómo podemos ayudarte.")}</p>
<a href="/contacto/" class="btn btn-w btn-lg">{p.get("cta_button", "Solicita auditoría gratuita")}</a>
</div>
'''

    breadcrumbs_items = [("Inicio", "/"), ("Servicios", "/servicios/")]
    if p.get('breadcrumb_parent'):
        breadcrumbs_items.append(p['breadcrumb_parent'])
    breadcrumbs_items.append((p['h1_short'], p['url']))

    body = f'''
<!-- HERO: Landing style -->
<section class="sec-hero" style="padding-bottom:var(--s12)">
<div class="wrap tc" style="position:relative;z-index:1">
{breadcrumb_html(breadcrumbs_items)}
<div class="pill anim" style="margin-bottom:var(--s5)">{p["h1_short"]}</div>
<h1 class="anim" style="max-width:20ch;margin:0 auto">{p["h1"]}</h1>
<p class="anim" style="font-size:var(--ts-lg);color:var(--text-sub);margin:var(--s5) auto 0;max-width:55ch">{p.get("intro", "")}</p>
<div class="anim" style="display:flex;gap:var(--s4);justify-content:center;margin-top:var(--s8);flex-wrap:wrap">
<a href="/contacto/" class="btn btn-p btn-lg">{p.get("cta_button_short", "Auditoría gratis")}</a>
<a href="#servicios" class="btn btn-o btn-lg">Ver servicios</a>
</div>
</div>
</section>

<!-- STATS BAR -->
<section class="sec-alt" style="padding:var(--s10) 0">
<div class="wrap">
<div class="bento bento-4 anim">
''' + ''.join([f'<div class="gc tc" style="padding:var(--s6)"><div class="st-n tg">{s["number"]}</div><div class="st-l">{s["label"]}</div></div>' for s in p.get('sidebar_stats', [])]) + '''
</div>
</div>
</section>

<!-- MAIN CONTENT: Sidebar + Content -->
<section class="sec" style="padding-top:var(--s12)">
<div class="pg">
<aside class="pg-side">
<nav>
<ul class="side-nav">
''' + sidebar_nav + '''
''' + (f'<li><a href="#faq">FAQ</a></li>' if faqs else '') + '''
</ul>
</nav>
<div class="side-stats">
''' + sidebar_stats + '''
</div>
<a href="/contacto/" class="btn btn-p" style="width:100%;justify-content:center;margin-top:var(--s6)">''' + p.get("cta_button_short", "Auditoría gratis") + '''</a>
</aside>
<div class="pg-main">
''' + content + '''
</div>
</div>
</section>
'''
    schema = service_schema(p['h1_short'], p.get('meta_desc', ''))
    schema += '\n' + faq_schema_tag if faq_schema_tag else ''

    return base_html(p['title'], p.get('meta_desc', ''), p['url'], body, schema=schema)


def build_vertical_page(page):
    """Build a vertical/sector page — LANDING TRANSACTIONAL"""
    p = page
    services_cards = ''
    for svc in p.get('services', []):
        services_cards += f'<div class="gc anim"><div class="fi">{svc["title"][0]}</div><h3>{svc["title"]}</h3><p>{svc["desc"]}</p></div>\n'

    faqs = p.get('faqs', [])
    faq_section = ''
    faq_schema_tag = ''
    if faqs:
        faq_section = f'<h2 class="tc">Preguntas frecuentes</h2>\n' + faq_html(faqs)
        faq_schema_tag = faq_schema(faqs)

    breadcrumbs = breadcrumb_html([("Inicio", "/"), ("Sectores", "/servicios/"), (p['h1_short'], p['url'])])

    body = f'''
<!-- HERO -->
<section class="sec-hero" style="padding-bottom:var(--s12)">
<div class="wrap tc" style="position:relative;z-index:1">
{breadcrumbs}
<div class="pill anim" style="margin-bottom:var(--s5)">{p.get("sector_name", "Sector").title()}</div>
<h1 class="anim" style="max-width:20ch;margin:0 auto">{p["h1"]}</h1>
<p class="anim" style="font-size:var(--ts-lg);color:var(--text-sub);margin:var(--s5) auto 0;max-width:55ch">{p.get("intro", "")}</p>
<p class="anim" style="font-size:var(--ts-2xl);font-weight:800;margin-top:var(--s6)"><span class="tg">{p.get("hook_stat", "")}</span></p>
<a href="/contacto/" class="btn btn-p btn-lg anim" style="margin-top:var(--s6)">{p.get("cta_button", "Auditoría gratuita")}</a>
</div>
</section>

<!-- SERVICES GRID -->
<section class="sec-colored">
<div class="wrap">
<h2 class="mt0 tc anim">Lo que hacemos para <span class="tg">{p.get("sector_name", "tu sector")}</span></h2>
<div class="bento bento-3 anim" style="margin-top:var(--s8)">
{services_cards}
</div>
</div>
</section>

<!-- TESTIMONIAL -->
<section class="sec">
<div class="wrap" style="max-width:800px;margin:0 auto">
<div class="testi anim">
<p class="testi-q">"{p.get("testimonial_quote", "[Testimonio del sector pendiente]")}"</p>
<div class="testi-a">
<div class="testi-av">{p.get("testimonial_author", "XX")[0]}</div>
<div><div class="testi-name">{p.get("testimonial_author", "[Nombre]").split(",")[0]}</div>
<div class="testi-role">{",".join(p.get("testimonial_author", "[Empresa]").split(",")[1:]).strip()}</div></div>
</div>
</div>
</div>
</section>

<!-- FAQ -->
<section class="sec-alt">
<div class="wrap-n">
{faq_section}
</div>
</section>

<!-- CTA -->
<section class="sec">
<div class="wrap">
<div class="cta-b anim">
<h2>{p.get("cta_title", "¿Empezamos?")}</h2>
<p>Solicita tu auditoría gratuita y descubre cómo podemos ayudarte.</p>
<a href="/contacto/" class="btn btn-w btn-lg">{p.get("cta_button", "Auditoría gratuita")}</a>
</div>
</div>
</section>
'''
    schema = service_schema(p['h1_short'], p.get('meta_desc', ''))
    schema += '\n' + faq_schema_tag if faq_schema_tag else ''
    return base_html(p['title'], p.get('meta_desc', ''), p['url'], body, schema=schema)


def build_geo_page(page):
    """Build a geolocalised city page"""
    p = page
    city = p['city']
    faqs = p.get('faqs', [])
    faq_section = ''
    faq_schema_tag = ''
    if faqs:
        faq_section = f'<h2>Preguntas frecuentes sobre {p["service_name"]} en {city}</h2>\n' + faq_html(faqs)
        faq_schema_tag = faq_schema(faqs)

    services_links = ''
    for svc in p.get('related_services', []):
        services_links += f'<li><a href="{svc["url"]}">{svc["label"]}</a></li>\n'

    zones = ' · '.join(p.get('zones', []))
    breadcrumbs = breadcrumb_html([("Inicio", "/"), (city, f"/agencia-marketing-digital-{city.lower()}/"), (p['h1_short'], p['url'])])

    body = f'''
<section class="section" style="padding-top:var(--space-8)">
<div class="wrap-narrow">
{breadcrumbs}
<h1>{p["h1"]}</h1>
<p style="font-size:var(--text-lg);color:var(--text-muted);margin-top:var(--space-4)">{p.get("intro", "")}</p>
<p style="margin-top:var(--space-4)">📍 {p.get("address", "Aragó 4, Barcelona 08015")} · 📞 <a href="tel:+34608721015">+34 608 721 015</a></p>

<div class="stats" style="margin-top:var(--space-8)">
<div><div class="stat-number text-accent">{p.get("stat1_num", "487")}</div><div class="stat-label">{p.get("stat1_label", "clientes en " + city)}</div></div>
<div><div class="stat-number text-accent">{p.get("stat2_num", "12+")}</div><div class="stat-label">{p.get("stat2_label", "años de experiencia")}</div></div>
</div>
</div>
</section>

<section class="section">
<div class="wrap-narrow">
<h2>Nuestros servicios de {p["service_name"]} en {city}</h2>
<ul>{services_links}</ul>

<h2>Zonas de {city} donde trabajamos</h2>
<p>{zones}</p>
</div>
</section>

<section class="section-dark">
<div class="wrap-narrow">
<h2 class="mt-0">Caso de éxito en {city}</h2>
<p class="testimonial">"{p.get("testimonial_quote", "[Testimonio local pendiente]")}"</p>
<p class="testimonial-author">— {p.get("testimonial_author", "[Nombre, Empresa, " + city + "]")}</p>
</div>
</section>

<section class="section">
<div class="wrap-narrow">
{faq_section}
</div>
</section>

<section class="section-accent">
<div class="wrap text-center">
<h2 class="mt-0" style="color:white">¿Buscas {p["service_name"]} en {city}?</h2>
<a href="/contacto/" class="btn btn-white" style="margin-top:var(--space-4)">Solicita presupuesto</a>
</div>
</section>
'''
    schema = local_business_schema(city, p['service_name'])
    schema += '\n' + faq_schema_tag if faq_schema_tag else ''
    return base_html(p['title'], p.get('meta_desc', ''), p['url'], body, schema=schema)


# ============================================================
# PAGE DATA — ALL URLS
# ============================================================

# Helper to make service page data with minimal boilerplate
def svc(url, title, meta_desc, h1, h1_short, intro, sections, faqs, sidebar_stats=None, cta_button="Auditoría gratuita", **kwargs):
    return {
        'type': 'service', 'url': url, 'title': title, 'meta_desc': meta_desc,
        'h1': h1, 'h1_short': h1_short, 'intro': intro,
        'sections': sections, 'faqs': faqs,
        'sidebar_stats': sidebar_stats or [
            {"number": "+320%", "label": "tráfico medio"},
            {"number": "98%", "label": "satisfacción"},
            {"number": "0€", "label": "permanencia"},
        ],
        'cta_button': cta_button, 'cta_button_short': cta_button,
        **kwargs
    }

def vert(url, title, meta_desc, h1, h1_short, intro, sector_name, hook_stat, services, faqs, cta_button="Auditoría gratuita", **kwargs):
    return {
        'type': 'vertical', 'url': url, 'title': title, 'meta_desc': meta_desc,
        'h1': h1, 'h1_short': h1_short, 'intro': intro,
        'sector_name': sector_name, 'hook_stat': hook_stat,
        'services': services, 'faqs': faqs, 'cta_button': cta_button, **kwargs
    }

def geo(url, title, meta_desc, h1, h1_short, intro, city, service_name, zones, related_services, faqs, **kwargs):
    return {
        'type': 'geo', 'url': url, 'title': title, 'meta_desc': meta_desc,
        'h1': h1, 'h1_short': h1_short, 'intro': intro,
        'city': city, 'service_name': service_name,
        'zones': zones, 'related_services': related_services,
        'faqs': faqs, **kwargs
    }

# --- SECTION HELPER ---
def sec(id, nav_label, title, html="<p>[Contenido pendiente de redacción profesional]</p>"):
    return {"id": id, "nav_label": nav_label, "title": title, "html": html}

# ============================================================
# ALL PAGES DATA
# ============================================================

ALL_PAGES = []

# --- HOME ---
# (built separately)

# --- SILO 1: SEO ---
ALL_PAGES.append(svc(
    "/agencia-seo/",
    "Agencia SEO | Expertos en Posicionamiento Web — Comunikoo",
    "Agencia SEO especializada en resultados. Aumentamos tu tráfico orgánico y ventas con estrategia SEO personalizada. Auditoría gratuita. Sin permanencia.",
    "Agencia SEO — Posicionamos Tu Negocio en el Top de Google",
    "Agencia SEO",
    "Somos una agencia SEO especializada en posicionar negocios en las primeras posiciones de Google. Sin permanencia, con resultados medibles y dashboard en tiempo real.",
    sections=[
        sec("por-que", "Por qué SEO", "¿Por qué necesitas una agencia SEO para tu negocio?"),
        sec("servicios", "Servicios", "Nuestros servicios SEO"),
        sec("proceso", "Proceso", "Cómo trabajamos tu posicionamiento SEO paso a paso"),
        sec("resultados", "Resultados", "Resultados reales — Casos de éxito SEO"),
        sec("diferencias", "Diferencias", "¿Qué nos diferencia de otras agencias SEO?"),
    ],
    faqs=[
        ("¿Cuánto cuesta contratar una agencia SEO?", "El precio depende de la competencia de tu sector, el estado actual de tu web y los objetivos. Nuestros planes empiezan desde 490€/mes."),
        ("¿Cuánto tiempo tarda el SEO en dar resultados?", "Los primeros resultados suelen verse entre 3 y 6 meses. El SEO es una inversión a medio-largo plazo con retorno creciente."),
        ("¿Qué diferencia hay entre SEO y SEM?", "El SEO posiciona tu web de forma orgánica (sin pagar por clic). El SEM (Google Ads) son anuncios de pago. Lo ideal es combinar ambos."),
        ("¿Necesito SEO si ya hago Google Ads?", "Sí. El SEO reduce tu dependencia de la publicidad de pago y genera tráfico constante sin coste por clic."),
        ("¿Qué incluye vuestro servicio de agencia SEO?", "Auditoría técnica, keyword research, optimización on-page, link building, contenidos SEO, reporting mensual y dashboard en tiempo real."),
        ("¿Hacéis SEO para tiendas online?", "Sí, tenemos un servicio especializado de SEO para ecommerce con optimización de fichas de producto, categorías y arquitectura web."),
    ],
))

ALL_PAGES.append(svc("/servicios/agencia-seo-local/", "Agencia SEO Local | Posiciona tu Negocio en Google Maps — Comunikoo", "Especialistas en SEO local. Posicionamos tu negocio en Google Maps y el pack local. Más clientes desde búsquedas cerca de mí. Auditoría gratis.", "Agencia de SEO Local — Domina las Búsquedas en Tu Ciudad", "SEO Local", "El 46% de las búsquedas en Google tienen intención local. Si no apareces en el pack local, estás perdiendo clientes cada día.", sections=[sec("que-es", "Qué es", "El 46% de las búsquedas en Google tienen intención local"), sec("servicios", "Servicios", "Servicios de SEO local que ofrecemos"), sec("sectores", "Sectores", "¿Para qué negocios funciona el SEO local?"), sec("proceso", "Proceso", "Nuestro proceso de trabajo en SEO local")], faqs=[("¿Cuánto tarda en posicionarse un negocio en Google Maps?", "Normalmente entre 2 y 4 meses, dependiendo de la competencia en tu zona."), ("¿Cuánto cuesta el servicio de SEO local?", "Desde 390€/mes para una ficha de Google Business Profile."), ("¿Puedo posicionarme en varias ciudades a la vez?", "Sí, trabajamos estrategias multi-ubicación con fichas independientes por ciudad.")]))

ALL_PAGES.append(svc("/servicios/auditoria-seo/", "Auditoría SEO Profesional | Diagnóstico Completo — Comunikoo", "Auditoría SEO completa: técnica, on-page y off-page. Detectamos errores que frenan tu posicionamiento. Informe detallado + plan de acción.", "Auditoría SEO — Descubre Qué Frena el Posicionamiento de Tu Web", "Auditoría SEO", "Una auditoría SEO profesional identifica todos los problemas técnicos, de contenido y de autoridad que impiden que tu web posicione en Google.", sections=[sec("que-es", "Qué es", "¿Qué es una auditoría SEO y por qué la necesitas?"), sec("incluye", "Qué incluye", "Qué incluye nuestra auditoría SEO"), sec("herramientas", "Herramientas", "Herramientas que utilizamos"), sec("proceso", "Proceso", "¿Cómo es el proceso de auditoría?")], faqs=[("¿Cuánto cuesta una auditoría SEO?", "Ofrecemos una auditoría inicial gratuita. Las auditorías completas con informe detallado tienen un coste a partir de 350€."), ("¿Cada cuánto tiempo debo hacer una auditoría SEO?", "Recomendamos una auditoría completa al menos una vez al año, y mini-auditorías trimestrales."), ("¿La auditoría incluye la implementación de mejoras?", "La auditoría incluye el diagnóstico y plan de acción. La implementación puede contratarse por separado.")]))

ALL_PAGES.append(svc("/servicios/consultoria-seo/", "Consultoría SEO | Asesoramiento Experto en Posicionamiento — Comunikoo", "Consultoría SEO personalizada. Te asesoramos, formamos a tu equipo y diseñamos la estrategia SEO perfecta. Primera consulta gratuita.", "Consultoría SEO — Estrategia Experta para Tu Posicionamiento Web", "Consultoría SEO", "Si tienes equipo interno o quieres una second opinion, nuestra consultoría SEO te da la estrategia y el acompañamiento que necesitas.", sections=[sec("que-es", "Qué es", "¿Qué es una consultoría SEO y en qué se diferencia de una agencia?"), sec("servicios", "Servicios", "Servicios de consultoría SEO"), sec("para-quien", "Para quién", "¿Para quién es nuestra consultoría SEO?"), sec("proceso", "Proceso", "Nuestro proceso de consultoría")], faqs=[("¿Cuál es la diferencia entre consultoría SEO y agencia SEO?", "La consultoría te asesora y forma; la agencia ejecuta el trabajo completo por ti."), ("¿Cuánto cuesta una consultoría SEO?", "Las sesiones de consultoría empiezan desde 150€/hora. Los planes mensuales desde 590€/mes."), ("¿Ofrecéis formación SEO in-company?", "Sí, formamos a equipos internos de marketing con talleres prácticos adaptados a su nivel.")]))

ALL_PAGES.append(svc("/servicios/posicionamiento-web/", "Posicionamiento Web | Primeras Posiciones en Google — Comunikoo", "Servicio de posicionamiento web profesional. Te posicionamos en las primeras posiciones de Google con estrategia SEO probada. +300% tráfico orgánico.", "Posicionamiento Web — Lleva Tu Página a las Primeras Posiciones de Google", "Posicionamiento Web", "El posicionamiento web es la estrategia para que tu página aparezca en los primeros resultados de Google cuando tus clientes buscan tus servicios.", sections=[sec("que-es", "Qué es", "¿Qué es el posicionamiento web y cómo funciona?"), sec("beneficios", "Beneficios", "Beneficios del posicionamiento web para tu negocio"), sec("servicios", "Servicios", "Nuestro servicio de posicionamiento web"), sec("precios", "Precios", "¿Cuánto cuesta el posicionamiento web?"), sec("resultados", "Resultados", "Resultados de posicionamiento web — Casos reales")], faqs=[("¿Cuánto tarda en funcionar el posicionamiento web?", "Entre 3 y 6 meses para ver resultados significativos, aunque mejoras técnicas se notan antes."), ("¿El posicionamiento web es lo mismo que el SEO?", "Sí, posicionamiento web es el término en español para referirse al SEO (Search Engine Optimization)."), ("¿Garantizáis la primera posición en Google?", "No. Nadie puede garantizar posiciones específicas. Lo que sí garantizamos es una metodología probada y resultados medibles.")]))

ALL_PAGES.append(svc("/servicios/linkbuilding/", "Linkbuilding Profesional | Backlinks de Calidad — Comunikoo", "Servicio de link building con backlinks de calidad que aumentan tu autoridad en Google. Estrategia white hat. Sin enlaces tóxicos.", "Link Building — Aumentamos la Autoridad de Tu Web con Backlinks de Calidad", "Linkbuilding", "El link building es la estrategia de conseguir enlaces de calidad hacia tu web para aumentar su autoridad a ojos de Google.", sections=[sec("que-es", "Qué es", "¿Qué es el link building y por qué es esencial para el SEO?"), sec("estrategias", "Estrategias", "Nuestras estrategias de link building"), sec("proceso", "Proceso", "Cómo trabajamos tu perfil de enlaces"), sec("metricas", "Métricas", "Métricas que monitorizamos")], faqs=[("¿Cuántos backlinks necesita mi web al mes?", "Depende de tu sector y competencia. Normalmente trabajamos con 10-20 enlaces de calidad al mes."), ("¿Comprar enlaces es seguro?", "Los enlaces de baja calidad son peligrosos. Nosotros trabajamos solo con estrategias white hat: guest posting, digital PR y contenido enlazable."), ("¿Cuánto cuesta un servicio de link building?", "Los planes de link building empiezan desde 490€/mes, dependiendo del volumen y calidad de enlaces necesarios.")]))

# --- SILO 2: DISEÑO WEB (shortened for brevity — all follow same pattern) ---
for pg in [
    ("/diseno-web/", "Diseño Web Profesional | Webs que Convierten — Comunikoo", "Diseño web profesional enfocado en ventas. Webs rápidas, responsive y optimizadas para SEO. Presupuesto sin compromiso.", "Diseño Web Profesional — Creamos Webs que Generan Negocio", "Diseño Web"),
    ("/servicios/diseno-web-wordpress/", "Diseño Web WordPress | Webs Profesionales — Comunikoo", "Diseño web en WordPress a medida. Webs rápidas, editables y optimizadas para SEO. Sin plantillas genéricas.", "Diseño Web WordPress — Webs Profesionales, Rápidas y Autogestionables", "Diseño WordPress"),
    ("/servicios/agencia-wordpress/", "Agencia WordPress | Desarrollo Especializado — Comunikoo", "Agencia WordPress con +200 proyectos completados. Diseño, desarrollo, plugins a medida, WPO y soporte técnico. Sin permanencia. Pide tu auditoría gratis.", "Agencia WordPress — Tu Partner Especializado en WordPress", "Agencia WordPress"),
    ("/servicios/programador-wordpress/", "Programador WordPress | Desarrollo a Medida — Comunikoo", "Programadores WordPress senior. Desarrollo a medida, plugins custom, integraciones API y WPO avanzado. +200 proyectos. Presupuesto sin compromiso.", "Programador WordPress — Desarrollo a Medida Sin Límites Técnicos", "Programador WordPress"),
    ("/servicios/mantenimiento-wordpress/", "Mantenimiento WordPress | Soporte y Seguridad — Comunikoo", "Planes de mantenimiento WordPress: actualizaciones, seguridad, backups y soporte. Desde 99€/mes.", "Mantenimiento WordPress — Tu Web Siempre Segura y Actualizada", "Mantenimiento WordPress"),
    ("/servicios/diseno-web-a-medida/", "Diseño Web a Medida | Sin Plantillas — Comunikoo", "Diseño web a medida 100% personalizado. Sin plantillas, sin límites. Tu web única.", "Diseño Web a Medida — Tu Web Única, Diseñada Desde Cero", "Diseño Web a Medida"),
    ("/servicios/diseno-web-para-empresas/", "Diseño Web para Empresas | Webs Corporativas — Comunikoo", "Diseño web para empresas que genera confianza y clientes. Webs corporativas profesionales.", "Diseño Web para Empresas — La Web Corporativa que Tu Negocio Necesita", "Diseño Web Empresas"),
    ("/servicios/desarrollo-web/", "Desarrollo Web Profesional | Programación a Medida — Comunikoo", "Desarrollo web profesional: frontend, backend, APIs y aplicaciones web. Código limpio y escalable.", "Desarrollo Web — Programación Profesional para Proyectos Ambiciosos", "Desarrollo Web"),
    ("/servicios/landing-pages/", "Landing Pages | Páginas de Alta Conversión — Comunikoo", "Landing pages diseñadas para convertir. Optimizadas para Google Ads y Meta Ads. Test A/B incluido.", "Landing Pages — Páginas que Convierten Visitantes en Clientes", "Landing Pages"),
    ("/servicios/mantenimiento-web/", "Mantenimiento Web | Soporte Técnico Mensual — Comunikoo", "Mantenimiento web profesional: actualizaciones, seguridad, backups y soporte. Desde 79€/mes.", "Mantenimiento Web — Tu Página Siempre Segura y Actualizada", "Mantenimiento Web"),
    ("/servicios/optimizacion-cro/", "Optimización CRO | Más Conversiones — Comunikoo", "CRO: optimización de conversión. Aumentamos tus ventas sin más tráfico. Test A/B y heatmaps.", "Optimización CRO — Más Clientes Con el Mismo Tráfico", "CRO"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Servicio profesional con resultados medibles. Sin permanencia. Dashboard en tiempo real.", sections=[sec("que-es", "Qué es", f"¿Qué es {pg[4].lower()} y por qué lo necesitas?"), sec("servicios", "Servicios", f"Nuestros servicios de {pg[4].lower()}"), sec("proceso", "Proceso", "Nuestro proceso de trabajo"), sec("resultados", "Resultados", "Casos de éxito")], faqs=[("¿Cuánto cuesta este servicio?", "El precio depende de tu proyecto. Solicita presupuesto sin compromiso."), ("¿Cuánto tiempo tardáis?", "Depende de la complejidad. Te damos plazos claros desde el primer día."), ("¿Ofrecéis soporte después?", "Sí, todos nuestros proyectos incluyen soporte post-entrega.")]))

# --- SILO 2B: ECOMMERCE ---
for pg in [
    ("/servicios/agencia-ecommerce/", "Agencia Ecommerce | Tiendas Online — Comunikoo", "Agencia ecommerce: diseño, SEO, campañas y CRO para tiendas online. Shopify, WooCommerce y PrestaShop.", "Agencia Ecommerce — Creamos, Optimizamos y Escalamos Tu Tienda Online", "Agencia Ecommerce"),
    ("/tienda-online/", "Crear Tienda Online | Ecommerce Profesional — Comunikoo", "Creamos tu tienda online profesional lista para vender. Diseño, pasarela de pago y SEO incluidos.", "Tienda Online — Tu Ecommerce Listo para Vender desde el Día 1", "Tienda Online"),
    ("/servicios/diseno-tienda-online/", "Diseño Tienda Online | Ecommerce que Vende — Comunikoo", "Diseño de tienda online orientado a conversión. UX/UI que enamora y convierte.", "Diseño de Tienda Online — Un Ecommerce que Enamora y Convierte", "Diseño Tienda Online"),
    ("/servicios/seo-para-ecommerce/", "SEO para Ecommerce | Posiciona Tu Tienda — Comunikoo", "SEO especializado para tiendas online. Posicionamos tus productos y categorías en Google.", "SEO para Ecommerce — Posiciona Tu Tienda y Multiplica Ventas", "SEO Ecommerce"),
    ("/servicios/agencia-shopify/", "Agencia Shopify | Partner Shopify España — Comunikoo", "Agencia Shopify Partner. Diseño, desarrollo, migración y optimización de tiendas Shopify.", "Agencia Shopify — Tu Partner para Crear y Escalar en Shopify", "Agencia Shopify"),
    ("/servicios/agencia-woocommerce/", "Agencia WooCommerce | Tiendas WordPress — Comunikoo", "Agencia WooCommerce. Diseño, desarrollo y optimización de tiendas online en WordPress.", "Agencia WooCommerce — WordPress para Tu Tienda Online", "Agencia WooCommerce"),
    ("/servicios/agencia-prestashop/", "Agencia PrestaShop | Desarrollo PrestaShop — Comunikoo", "Agencia PrestaShop. Diseño, desarrollo, módulos a medida y migración.", "Agencia PrestaShop — Desarrollo y Soporte para Tu Tienda", "Agencia PrestaShop"),
    ("/servicios/google-shopping/", "Google Shopping | Campañas Shopping — Comunikoo", "Gestión profesional de Google Shopping. Optimizamos tu feed para maximizar ventas y ROAS.", "Google Shopping — Tus Productos en los Primeros Resultados", "Google Shopping"),
    ("/servicios/publicidad-tiendas-online/", "Publicidad Tiendas Online | Campañas Ecommerce — Comunikoo", "Campañas de publicidad para tiendas online: Google Ads, Shopping, Meta Ads y remarketing.", "Publicidad para Tiendas Online — Campañas que Multiplican Ventas", "Publicidad Ecommerce"),
    ("/servicios/email-marketing-ecommerce/", "Email Marketing Ecommerce | Automatizaciones — Comunikoo", "Email marketing para ecommerce: carritos abandonados, flows de bienvenida y fidelización.", "Email Marketing Ecommerce — Automatizaciones que Recuperan Ventas", "Email Ecommerce"),
    ("/servicios/cro-ecommerce/", "CRO Ecommerce | Optimización Conversión Tienda — Comunikoo", "CRO para ecommerce: optimizamos checkout, fichas de producto y funnel de compra.", "CRO para Ecommerce — Vende Más con el Mismo Tráfico", "CRO Ecommerce"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Servicio especializado en ecommerce con resultados medibles.", sections=[sec("que-es", "Qué es", f"¿Qué es {pg[4].lower()} y por qué lo necesitas?"), sec("servicios", "Servicios", f"Nuestros servicios de {pg[4].lower()}"), sec("proceso", "Proceso", "Nuestro proceso de trabajo"), sec("resultados", "Resultados", "Casos de éxito")], faqs=[("¿Cuánto cuesta este servicio?", "Solicita presupuesto personalizado sin compromiso."), ("¿Con qué plataformas trabajáis?", "Trabajamos con Shopify, WooCommerce y PrestaShop."), ("¿En cuánto tiempo veo resultados?", "Depende del servicio. Te damos plazos claros desde el inicio.")]))

# --- SILO 3: PUBLICIDAD DIGITAL ---
for pg in [
    ("/agencia-google-ads/", "Agencia Google Ads | Campañas Rentables — Comunikoo", "Agencia Google Ads certificada. Campañas rentables que generan clientes reales. Google Partner. Sin permanencia.", "Agencia Google Ads — Campañas Rentables que Generan Clientes Reales", "Agencia Google Ads"),
    ("/servicios/experto-google-ads/", "Experto Google Ads | Especialista Certificado — Comunikoo", "Expertos Google Ads con certificaciones oficiales y +10 años de experiencia.", "Experto Google Ads — Especialistas que Hacen Rendir Tu Inversión", "Experto Google Ads"),
    ("/servicios/consultor-google-ads/", "Consultor Google Ads | Asesoría SEM — Comunikoo", "Consultoría Google Ads: auditoría, estrategia y formación para tu equipo.", "Consultor Google Ads — Asesoría Estratégica para Tus Campañas", "Consultor Google Ads"),
    ("/servicios/freelance-google-ads/", "Freelance Google Ads | Trato Directo — Comunikoo", "Freelance Google Ads: gestión con trato directo, sin intermediarios.", "Freelance Google Ads — Trato Directo, Flexibilidad y Resultados", "Freelance Google Ads"),
    ("/servicios/especialista-google-ads/", "Especialista Google Ads | Campañas Avanzadas — Comunikoo", "Especialistas Google Ads para campañas avanzadas y presupuestos grandes.", "Especialista Google Ads — Campañas de Siguiente Nivel", "Especialista Google Ads"),
    ("/servicios/consultor-sem/", "Consultor SEM | Publicidad en Buscadores — Comunikoo", "Consultoría SEM: estrategia de publicidad en Google + Bing. Auditoría y optimización.", "Consultor SEM — Publicidad en Buscadores Multicanal", "Consultor SEM"),
    ("/servicios/publicidad-en-google/", "Publicidad en Google | Anúnciate en Google — Comunikoo", "¿Quieres aparecer en Google? Te ayudamos a anunciarte de forma rentable. Desde 300€/mes.", "Publicidad en Google — Aparece en los Primeros Resultados", "Publicidad Google"),
    ("/servicios/agencia-facebook-ads/", "Agencia Facebook Ads | Campañas Facebook — Comunikoo", "Agencia de Facebook Ads especializada. Campañas de captación, retargeting y conversión.", "Agencia Facebook Ads — Campañas que Generan Clientes Reales", "Agencia Facebook Ads"),
    ("/servicios/agencia-meta-ads/", "Agencia Meta Ads | Facebook + Instagram + WhatsApp — Comunikoo", "Agencia Meta Ads: campañas en todo el ecosistema Meta. Resultados multicanal.", "Agencia Meta Ads — Publicidad en Todo el Ecosistema Meta", "Agencia Meta Ads"),
    ("/servicios/instagram-ads/", "Instagram Ads | Publicidad en Instagram — Comunikoo", "Campañas de Instagram Ads: stories, reels, feed y shopping. Creatividades que convierten.", "Instagram Ads — Publicidad Visual que Impacta y Convierte", "Instagram Ads"),
    ("/servicios/youtube-ads/", "YouTube Ads | Publicidad en Video — Comunikoo", "Campañas de YouTube Ads: TrueView, Bumper y Discovery. Solo pagas por visualizaciones.", "YouTube Ads — Publicidad en Video que Genera Resultados", "YouTube Ads"),
    ("/servicios/publicidad-redes-sociales/", "Publicidad en Redes Sociales | Social Ads — Comunikoo", "Campañas de publicidad en redes sociales: Facebook, Instagram, TikTok, LinkedIn y YouTube.", "Publicidad en Redes Sociales — Campañas Multicanal que Convierten", "Social Ads"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Servicio profesional de publicidad digital con enfoque en ROI.", sections=[sec("que-es", "Qué es", f"¿Por qué necesitas {pg[4].lower()}?"), sec("servicios", "Servicios", f"Nuestros servicios de {pg[4].lower()}"), sec("proceso", "Proceso", "Nuestro proceso de trabajo"), sec("resultados", "Resultados", "Casos de éxito")], faqs=[("¿Cuánto cuesta este servicio?", "Depende de tu presupuesto publicitario y objetivos. Consulta sin compromiso."), ("¿Cuándo veré resultados?", "Con publicidad de pago los resultados son casi inmediatos. La optimización mejora con el tiempo."), ("¿Puedo cancelar cuando quiera?", "Sí, trabajamos sin permanencia.")]))

# --- SILO 4: REDES SOCIALES ---
for pg in [
    ("/community-manager/", "Community Manager Profesional | Gestión Redes — Comunikoo", "Community Manager profesional para tu empresa. Contenido, gestión de comunidad y crecimiento. Desde 350€/mes.", "Community Manager — Gestión Profesional de Tus Redes Sociales", "Community Manager"),
    ("/servicios/gestion-redes-sociales/", "Gestión de Redes Sociales | Estrategia + Ejecución — Comunikoo", "Servicio integral de gestión de redes sociales: estrategia, contenido y análisis.", "Gestión de Redes Sociales — Estrategia y Resultados para Tu Marca", "Gestión Redes"),
    ("/servicios/social-media-marketing/", "Social Media Marketing | Redes con ROI — Comunikoo", "Social media marketing orientado a resultados. Convierte tus redes en canal de ventas.", "Social Media Marketing — Convierte Tus Redes en Canal de Ventas", "Social Media"),
    ("/servicios/marketing-de-contenidos/", "Marketing de Contenidos | Contenido que Posiciona — Comunikoo", "Marketing de contenidos: blog, vídeo, infografías y lead magnets que atraen y convierten.", "Marketing de Contenidos — Atrae, Posiciona y Convierte", "Marketing Contenidos"),
    ("/email-marketing/", "Agencia Email Marketing | Campañas que Generan Ventas — Comunikoo", "Agencia de email marketing profesional: newsletter, automatizaciones, campañas y estrategia. El canal con mayor ROI del marketing digital. Sin permanencia.", "Agencia Email Marketing — El Canal con Mayor ROI del Marketing Digital", "Email Marketing"),
    ("/servicios/inbound-marketing/", "Inbound Marketing | Atrae Clientes con Valor — Comunikoo", "Inbound marketing: atraemos clientes con contenido, SEO, email y automatización.", "Inbound Marketing — Atrae Clientes con Valor", "Inbound Marketing"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Servicio profesional con resultados medibles y reporting mensual.", sections=[sec("que-es", "Qué es", f"¿Qué es {pg[4].lower()} y por qué lo necesitas?"), sec("servicios", "Servicios", f"Nuestros servicios de {pg[4].lower()}"), sec("proceso", "Proceso", "Nuestro proceso de trabajo"), sec("resultados", "Resultados", "Casos de éxito")], faqs=[("¿Cuánto cuesta este servicio?", "Solicita presupuesto personalizado sin compromiso."), ("¿En cuánto tiempo veo resultados?", "Depende del servicio y tu punto de partida. Te informamos con plazos realistas."), ("¿Puedo cancelar cuando quiera?", "Sí, sin permanencia.")]))

# --- SILO 5: BRANDING ---
for pg in [
    ("/servicios/branding/", "Branding para Empresas | Identidad de Marca — Comunikoo", "Servicios de branding: estrategia, identidad visual, naming y manual corporativo.", "Branding para Empresas — Marcas que Conectan y Venden", "Branding"),
    ("/servicios/estrategia-digital/", "Estrategia Digital | Plan de Marketing — Comunikoo", "Diseñamos tu estrategia de marketing digital: análisis, canales y hoja de ruta.", "Estrategia Digital — El Plan que Tu Negocio Necesita", "Estrategia Digital"),
    ("/servicios/analitica-web/", "Analítica Web | GA4 y Datos — Comunikoo", "Analítica web profesional: GA4, GTM, dashboards y reporting basado en datos.", "Analítica Web — Datos Reales para Decisiones Inteligentes", "Analítica Web"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Servicio profesional para impulsar tu negocio.", sections=[sec("que-es", "Qué es", f"¿Qué es {pg[4].lower()} y por qué lo necesitas?"), sec("servicios", "Servicios", f"Nuestros servicios de {pg[4].lower()}"), sec("proceso", "Proceso", "Nuestro proceso de trabajo")], faqs=[("¿Cuánto cuesta este servicio?", "Solicita presupuesto personalizado."), ("¿Cuánto tardáis?", "Depende del proyecto. Te informamos desde el inicio.")]))

# --- PERFILES PROFESIONALES ---
for pg in [
    ("/disenador-web-freelance/", "Diseñador Web Freelance | Trato Directo — Comunikoo", "Diseñador web freelance profesional: webs a medida, WordPress y tiendas online. Trato directo.", "Diseñador Web Freelance — Trato Directo y Diseño Profesional", "Diseñador Web Freelance"),
    ("/disenador-web-profesional/", "Diseñador Web Profesional | Portfolio y Resultados — Comunikoo", "Diseñador web profesional con +200 proyectos. Webs que posicionan y generan negocio.", "Diseñador Web Profesional — Experiencia y Resultados", "Diseñador Web Profesional"),
    ("/experto-wordpress/", "Experto WordPress | Consultor Especializado — Comunikoo", "Experto WordPress para proyectos complejos. Desarrollo avanzado y resolución de problemas.", "Experto WordPress — El Especialista que Necesitas", "Experto WordPress"),
    ("/freelance-wordpress/", "Freelance WordPress | Desarrollo WP — Comunikoo", "Freelance WordPress profesional: diseño, desarrollo, plugins y mantenimiento. Trato directo.", "Freelance WordPress — Tu Proyecto con Trato Directo", "Freelance WordPress"),
    ("/gestor-google-ads/", "Gestor Google Ads | Gestión Diaria — Comunikoo", "Gestor de Google Ads dedicado. Optimización diaria de campañas y reporting.", "Gestor Google Ads — Gestión Operativa de Tus Campañas", "Gestor Google Ads"),
    ("/experto-sem/", "Experto SEM | Publicidad en Buscadores — Comunikoo", "Experto SEM: publicidad en Google, Bing y buscadores. Estrategia multimotor.", "Experto SEM — Publicidad en Buscadores que Maximiza Tu Inversión", "Experto SEM"),
    ("/freelance-sem/", "Freelance SEM | Gestión PPC — Comunikoo", "Freelance SEM profesional: gestión de campañas en Google Ads y Bing Ads. Trato directo.", "Freelance SEM — Campañas con Trato Directo", "Freelance SEM"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Profesional especializado con experiencia verificable y resultados reales.", sections=[sec("que-es", "Qué es", f"¿Por qué contratar un {pg[4].lower()}?"), sec("servicios", "Servicios", f"Qué hago como {pg[4].lower()}"), sec("portfolio", "Portfolio", "Proyectos y resultados")], faqs=[("¿Cuánto cuesta?", "Solicita presupuesto personalizado sin compromiso."), ("¿Qué garantías tengo?", "Trabajamos con contrato, plazos claros y entregables definidos.")]))

# --- OPORTUNIDAD 7: SEO PARA [SECTOR] (2560 vol combinado, intent comercial) ---
for pg in [
    ("/servicios/seo-para-abogados/", "SEO para Abogados | Posiciona Tu Despacho — Comunikoo", "SEO para abogados y despachos: posicionamiento en Google que genera consultas. Resultados medibles desde el primer mes.", "SEO para Abogados — Que Te Encuentren Quienes Necesitan un Abogado", "SEO Abogados"),
    ("/servicios/seo-para-pymes/", "SEO para Pymes | Posicionamiento Asequible — Comunikoo", "SEO para pymes: posicionamiento en Google adaptado a presupuestos de pequeñas empresas. Sin permanencia. Resultados reales.", "SEO para Pymes — Posicionamiento en Google sin Arruinarte", "SEO Pymes"),
    ("/servicios/seo-para-clinicas-dentales/", "SEO para Clínicas Dentales | Más Pacientes — Comunikoo", "SEO para clínicas dentales: posicionamiento local en Google, Google Maps y captación de pacientes online.", "SEO para Clínicas Dentales — Aparece Cuando Buscan Dentista", "SEO Clínicas Dentales"),
    ("/servicios/seo-para-empresas/", "SEO para Empresas | Estrategia Corporativa — Comunikoo", "SEO para empresas: estrategia de posicionamiento corporativo en Google. Auditoría, contenido y linkbuilding.", "SEO para Empresas — Posicionamiento Corporativo en Google", "SEO Empresas"),
    ("/servicios/seo-para-dentistas/", "SEO para Dentistas | Más Pacientes Online — Comunikoo", "SEO para dentistas: posicionamiento local, Google Maps y estrategia de contenido dental que atrae pacientes.", "SEO para Dentistas — Que Te Encuentren en Google", "SEO Dentistas"),
    ("/servicios/seo-para-restaurantes/", "SEO para Restaurantes | SEO Local + Maps — Comunikoo", "SEO para restaurantes: posicionamiento local, Google Maps, reseñas y ficha de negocio optimizada.", "SEO para Restaurantes — Aparece Primero en Google Maps", "SEO Restaurantes"),
    ("/servicios/seo-para-inmobiliarias/", "SEO para Inmobiliarias | Leads de Compradores — Comunikoo", "SEO para inmobiliarias: posicionamiento de propiedades, zonas y servicios inmobiliarios en Google.", "SEO para Inmobiliarias — Leads Orgánicos de Compradores y Vendedores", "SEO Inmobiliarias"),
    ("/servicios/seo-para-startups/", "SEO para Startups | Crecimiento Orgánico — Comunikoo", "SEO para startups: estrategia de crecimiento orgánico escalable. Product-led SEO y contenido técnico.", "SEO para Startups — Crecimiento Orgánico Escalable", "SEO Startups"),
    ("/servicios/seo-para-hoteles/", "SEO para Hoteles | Reservas Directas — Comunikoo", "SEO para hoteles: posicionamiento orgánico que genera reservas directas y reduce dependencia de OTAs.", "SEO para Hoteles — Más Reservas Directas desde Google", "SEO Hoteles"),
    ("/servicios/seo-para-clinicas/", "SEO para Clínicas | Posicionamiento Médico — Comunikoo", "SEO para clínicas médicas y centros de salud: posicionamiento local, reputación online y captación de pacientes.", "SEO para Clínicas — Posicionamiento Médico en Google", "SEO Clínicas"),
    ("/servicios/seo-para-autonomos/", "SEO para Autónomos | Visibilidad Online — Comunikoo", "SEO para autónomos: posicionamiento en Google asequible y efectivo. Compite con los grandes desde tu presupuesto.", "SEO para Autónomos — Compite en Google sin Ser una Gran Empresa", "SEO Autónomos"),
    ("/servicios/agencia-seo-para-pymes/", "Agencia SEO para Pymes | Especialistas — Comunikoo", "Agencia SEO especializada en pymes: planes desde 400€/mes. Posicionamiento real, reporting mensual y sin permanencia.", "Agencia SEO para Pymes — Planes Adaptados a Tu Presupuesto", "Agencia SEO Pymes"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Servicio de SEO especializado por sector.", sections=[sec("que-es", "Qué es", f"¿Por qué necesitas SEO especializado en tu sector?"), sec("servicios", "Qué incluye", f"Qué incluye nuestro servicio de {pg[4].lower()}"), sec("proceso", "Proceso", "Nuestro proceso de trabajo"), sec("resultados", "Resultados", "Casos de éxito en tu sector")], faqs=[("¿Cuánto cuesta el SEO?", "Planes desde 400€/mes para pymes. El precio depende de la competencia en tu sector y tus objetivos. Presupuesto cerrado."), ("¿Cuándo veré resultados?", "Los primeros resultados aparecen entre 2-4 meses. El SEO es una inversión a medio plazo con retorno acumulativo."), ("¿Qué garantías ofrecéis?", "No garantizamos posiciones (nadie puede), pero sí reporting transparente, mejoras medibles y trabajo constante.")]))

# --- OPORTUNIDAD 8: PRECIOS DISEÑO WEB (740 vol combinado) ---
ALL_PAGES.append(svc(
    "/precios-diseno-web/",
    "Precios Diseño Web 2026 | Cuánto Cuesta una Web — Comunikoo",
    "¿Cuánto cuesta un diseño web? Precios diseño web 2026: web corporativa desde 2.000€, tienda online desde 3.500€, web a medida desde 5.000€. Presupuesto sin compromiso.",
    "Precios Diseño Web 2026 — Cuánto Cuesta una Página Web Profesional",
    "Precios Diseño Web",
    "Guía completa de precios de diseño web en España. Transparencia total: qué incluye cada plan y cuánto cuesta.",
    sections=[
        sec("precios", "Precios", "Nuestros planes y precios de diseño web"),
        sec("que-incluye", "Qué incluye", "Qué está incluido en cada plan"),
        sec("comparativa", "Comparativa", "Comparativa de precios del mercado"),
        sec("proceso", "Proceso", "Cómo trabajamos"),
    ],
    faqs=[
        ("¿Cuánto cuesta una página web profesional?", "Web corporativa: 2.000-5.000€. Tienda online: 3.500-12.000€. Web a medida: desde 5.000€. Siempre presupuesto cerrado."),
        ("¿Por qué hay tanta diferencia de precios?", "Depende de la complejidad: número de páginas, funcionalidades, integraciones, diseño personalizado vs plantilla, etc."),
        ("¿Hay costes mensuales?", "El hosting + mantenimiento básico parte de 30€/mes. El mantenimiento premium con soporte y actualizaciones desde 90€/mes."),
        ("¿Cuánto cuesta una web WordPress?", "Una web WordPress profesional cuesta entre 1.500€ y 8.000€ dependiendo de la complejidad y funcionalidades."),
    ],
))

# --- OPORTUNIDAD 2: DISEÑO WEB PARA [SECTOR] (1400 vol combinado, intent comercial) ---
for pg in [
    ("/servicios/diseno-web-para-abogados/", "Diseño Web para Abogados | Webs que Captan Clientes — Comunikoo", "Diseño web para abogados y despachos: webs profesionales que transmiten confianza y captan clientes. Portfolio real.", "Diseño Web para Abogados — Webs que Transmiten Confianza y Captan Clientes", "Diseño Web Abogados"),
    ("/servicios/diseno-web-para-inmobiliarias/", "Diseño Web para Inmobiliarias | Portal Inmobiliario — Comunikoo", "Diseño web para inmobiliarias: portales con buscador de propiedades, CRM integrado y captación de leads.", "Diseño Web para Inmobiliarias — Tu Portal con Buscador de Propiedades", "Diseño Web Inmobiliarias"),
    ("/servicios/diseno-web-para-restaurantes/", "Diseño Web para Restaurantes | Carta Digital + Reservas — Comunikoo", "Diseño web para restaurantes: carta digital, sistema de reservas, fotos profesionales y SEO local.", "Diseño Web para Restaurantes — Carta Digital y Reservas Online", "Diseño Web Restaurantes"),
    ("/servicios/diseno-web-para-dentistas/", "Diseño Web para Dentistas | Clínicas Dentales — Comunikoo", "Diseño web para clínicas dentales: webs que generan confianza, cita online y SEO local.", "Diseño Web para Dentistas — Webs que Llenan Tu Agenda", "Diseño Web Dentistas"),
    ("/servicios/diseno-web-para-pymes/", "Diseño Web para Pymes | Profesional y Asequible — Comunikoo", "Diseño web para pymes: webs profesionales adaptadas a tu presupuesto. WordPress, responsive y SEO incluido.", "Diseño Web para Pymes — Profesional sin Arruinarte", "Diseño Web Pymes"),
    ("/servicios/diseno-web-para-psicologos/", "Diseño Web para Psicólogos | KD 1 — Comunikoo", "Diseño web para psicólogos: webs que transmiten cercanía, reserva online y contenido que posiciona.", "Diseño Web para Psicólogos — Webs que Conectan con Tus Pacientes", "Diseño Web Psicólogos"),
    ("/servicios/diseno-web-para-emprendedores/", "Diseño Web para Emprendedores | Tu Primera Web — Comunikoo", "Diseño web para emprendedores: webs rápidas, económicas y preparadas para crecer. Lanzamiento en 2 semanas.", "Diseño Web para Emprendedores — Lanza Tu Web en 2 Semanas", "Diseño Web Emprendedores"),
    ("/servicios/diseno-web-para-hoteles/", "Diseño Web para Hoteles | Más Reservas Directas — Comunikoo", "Diseño web para hoteles: motor de reservas, galería, multiidioma y SEO. Reduce comisiones de OTAs.", "Diseño Web para Hoteles — Más Reservas Directas, Menos Comisiones", "Diseño Web Hoteles"),
    ("/servicios/diseno-web-para-terapeutas/", "Diseño Web para Terapeutas | Consultas Online — Comunikoo", "Diseño web para terapeutas y profesionales de la salud: reserva online, blog y contenido ético.", "Diseño Web para Terapeutas — Webs que Transmiten Profesionalidad", "Diseño Web Terapeutas"),
    ("/servicios/diseno-web-para-autonomos/", "Diseño Web para Autónomos | Económica y Profesional — Comunikoo", "Diseño web para autónomos: presencia online profesional desde 800€. WordPress, SEO y responsive.", "Diseño Web para Autónomos — Presencia Online Profesional", "Diseño Web Autónomos"),
]:
    ALL_PAGES.append(svc(pg[0], pg[1], pg[2], pg[3], pg[4], "Servicio de diseño web especializado por sector.", sections=[sec("que-es", "Qué es", f"¿Por qué necesitas un diseño web especializado?"), sec("servicios", "Qué incluye", f"Qué incluye nuestro servicio de {pg[4].lower()}"), sec("proceso", "Proceso", "Nuestro proceso de trabajo"), sec("portfolio", "Portfolio", "Ejemplos reales de proyectos")], faqs=[("¿Cuánto cuesta el diseño web?", "Depende de la complejidad. Webs corporativas desde 2.000€, con tienda online desde 3.500€. Presupuesto cerrado tras analizar requisitos."), ("¿Cuánto tardáis en entregar?", "Web corporativa: 3-4 semanas. Tienda online: 5-8 semanas. Siempre con plazos claros."), ("¿Incluye SEO?", "Sí, todas nuestras webs incluyen SEO técnico y on-page de base.")]))

# --- OPORTUNIDAD 4: AGENCIA DE MARKETING BARCELONA (880 vol, KD 27) ---
ALL_PAGES.append(svc(
    "/agencia-marketing-barcelona/",
    "Agencia de Marketing Barcelona | Resultados Medibles — Comunikoo",
    "Agencia de marketing en Barcelona con equipo local. SEO, Google Ads, diseño web, redes sociales. +487 proyectos. Sin permanencia. Auditoría gratuita.",
    "Agencia de Marketing en Barcelona — Resultados Medibles, Sin Permanencia",
    "Agencia Marketing Barcelona",
    "Equipo local en Barcelona con conocimiento del mercado catalán. Estrategias a medida para empresas barcelonesas.",
    sections=[
        sec("que-es", "Qué hacemos", "Servicios de marketing digital en Barcelona"),
        sec("servicios", "Servicios", "SEO, Google Ads, diseño web, redes sociales y más"),
        sec("proceso", "Proceso", "Nuestro proceso de trabajo"),
        sec("resultados", "Resultados", "Casos de éxito en Barcelona"),
    ],
    faqs=[
        ("¿Tenéis oficina en Barcelona?", "Sí, estamos en Aragó 4, Barcelona 08015. Atendemos con cita previa."),
        ("¿Cuánto cuesta contratar una agencia de marketing?", "Depende de los servicios. Desde 500€/mes para SEO básico hasta planes integrales. Siempre sin permanencia."),
        ("¿Trabajáis solo en Barcelona?", "No, trabajamos con empresas de toda España. Pero nuestra base está en Barcelona y conocemos el mercado local a fondo."),
    ],
))

# --- VERTICALES ---
VERTICALS = [
    ("/marketing-para-restaurantes/", "Marketing para Restaurantes | Llena Tu Local — Comunikoo", "Marketing digital para restaurantes: SEO local, Google Maps, redes sociales y campañas. Especialistas en hostelería.", "Marketing para Restaurantes — Estrategias Digitales para Llenar Tu Local", "Marketing Restaurantes", "restaurantes", "El 90% busca restaurante en Google antes de ir."),
    ("/marketing-para-hoteles/", "Marketing para Hoteles | Más Reservas Directas — Comunikoo", "Marketing digital para hoteles: aumenta reservas directas, reduce comisiones OTAs. SEO hotelero y Google Hotel Ads.", "Marketing para Hoteles — Más Reservas Directas, Menos Comisiones", "Marketing Hoteles", "hoteles", "Reduce comisiones del 15-25% a OTAs."),
    ("/marketing-para-clinicas-dentales/", "Marketing para Clínicas Dentales | Más Pacientes — Comunikoo", "Marketing digital para clínicas dentales: SEO, Google Ads, redes sociales. +300% en leads.", "Marketing para Clínicas Dentales — Captamos Pacientes para Tu Agenda", "Marketing Dental", "clínicas dentales", "El 80% de pacientes busca dentista online."),
    ("/marketing-para-clinicas-esteticas/", "Marketing para Clínicas Estéticas | Pacientes Premium — Comunikoo", "Marketing digital para clínicas de medicina estética. Captamos pacientes premium.", "Marketing para Clínicas Estéticas — Captamos Pacientes Premium", "Marketing Estética", "clínicas estéticas", "Sector que crece un 15% anual."),
    ("/marketing-para-psicologos/", "Marketing para Psicólogos | Más Pacientes — Comunikoo", "Marketing digital para psicólogos: web, SEO, Google Ads. Captación ética y efectiva.", "Marketing para Psicólogos — Conecta con Quienes Necesitan Tu Ayuda", "Marketing Psicólogos", "psicólogos", "La demanda de psicología se ha triplicado."),
    ("/marketing-para-veterinarias/", "Marketing para Veterinarias | Más Clientes — Comunikoo", "Marketing digital para clínicas veterinarias: SEO local, Google Maps y redes sociales.", "Marketing para Veterinarias — Atrae Más Dueños de Mascotas", "Marketing Veterinarias", "veterinarias", "El sector pet está en pleno auge."),
    ("/marketing-para-abogados/", "Marketing para Abogados | Captar Clientes — Comunikoo", "Marketing digital para despachos de abogados: SEO, Google Ads y contenido legal.", "Marketing para Abogados — Más Clientes para Tu Despacho", "Marketing Abogados", "abogados", "El 96% busca abogado en Google."),
    ("/marketing-para-asesorias/", "Marketing para Asesorías | Diferénciate — Comunikoo", "Marketing digital para asesorías y gestorías: web, SEO y captación de clientes.", "Marketing para Asesorías — Diferénciate en un Mercado Saturado", "Marketing Asesorías", "asesorías", "Diferénciate cuando todos ofrecen lo mismo."),
    ("/marketing-para-inmobiliarias/", "Marketing para Inmobiliarias | Leads Cualificados — Comunikoo", "Marketing digital para inmobiliarias: SEO, Google Ads y captación de leads.", "Marketing para Inmobiliarias — Leads de Compradores y Vendedores", "Marketing Inmobiliarias", "inmobiliarias", "Captamos leads de compradores Y vendedores."),
    ("/marketing-para-empresas-de-reformas/", "Marketing para Reformas | Más Presupuestos — Comunikoo", "Marketing digital para empresas de reformas: SEO local, Google Ads y portfolio.", "Marketing para Empresas de Reformas — Más Presupuestos Solicitados", "Marketing Reformas", "empresas de reformas", "Tu cliente busca en Google, no en Páginas Amarillas."),
    ("/marketing-para-autoescuelas/", "Marketing para Autoescuelas | Más Alumnos — Comunikoo", "Marketing digital para autoescuelas: SEO local, Google Ads y redes sociales.", "Marketing para Autoescuelas — Más Alumnos Matriculados", "Marketing Autoescuelas", "autoescuelas", "Los jóvenes buscan autoescuela en Google."),
    ("/marketing-para-talleres-de-coches/", "Marketing para Talleres | Más Clientes — Comunikoo", "Marketing digital para talleres mecánicos: SEO local, Google Maps y reseñas.", "Marketing para Talleres de Coches — Más Clientes en Tu Taller", "Marketing Talleres", "talleres de coches", "El conductor busca taller en Google Maps."),
    ("/marketing-para-gimnasios/", "Marketing para Gimnasios | Más Socios — Comunikoo", "Marketing digital para gimnasios: SEO local, campañas y retención. Más socios todo el año.", "Marketing para Gimnasios — Más Socios Todo el Año", "Marketing Gimnasios", "gimnasios", "Más socios todo el año, no solo en enero."),
    ("/marketing-para-academias/", "Marketing para Academias | Captación Alumnos — Comunikoo", "Marketing digital para academias: SEO, Google Ads y web con matrícula online.", "Marketing para Academias — Captación de Alumnos Online", "Marketing Academias", "academias", "La captación de alumnos se ha digitalizado."),
    ("/marketing-para-ecommerce/", "Marketing para Ecommerce | Estrategia 360 — Comunikoo", "Marketing digital para ecommerce: SEO + Ads + email + CRO. Escala tu tienda online.", "Marketing para Ecommerce — Estrategia 360 para Escalar", "Marketing Ecommerce", "ecommerce", "Solo el 3% de tiendas online son rentables."),
    ("/marketing-para-empresas-b2b/", "Marketing B2B | Leads Cualificados — Comunikoo", "Marketing digital para empresas B2B: LinkedIn, SEO, contenido y generación de leads.", "Marketing B2B — Generación de Leads Cualificados", "Marketing B2B", "empresas B2B", "El contenido de valor es el rey en B2B."),
    # --- OPORTUNIDAD 1: PYMES (KD 4, 1600 vol combinado) ---
    ("/marketing-para-pymes/", "Marketing Digital para Pymes | Resultados Reales — Comunikoo", "Marketing digital para pymes: SEO, Google Ads, web y redes sociales. Estrategias adaptadas a presupuestos de pequeñas empresas. Sin permanencia.", "Marketing Digital para Pymes — Estrategias que Caben en Tu Presupuesto", "Marketing Pymes", "pymes y pequeñas empresas", "El 70% de pymes que invierten en marketing digital crecen un 30%."),
    # --- OPORTUNIDAD 6: NUEVOS SECTORES ---
    ("/marketing-para-farmacias/", "Marketing para Farmacias | Más Clientes — Comunikoo", "Marketing digital para farmacias y ópticas: SEO local, Google Maps, redes sociales y campañas de captación.", "Marketing para Farmacias — Más Clientes en Tu Zona", "Marketing Farmacias", "farmacias", "El 65% de consumidores busca farmacia cerca en Google."),
    ("/marketing-para-fisioterapeutas/", "Marketing para Fisioterapeutas | Más Pacientes — Comunikoo", "Marketing digital para fisioterapeutas: web profesional, SEO local y Google Ads. Captación ética de pacientes.", "Marketing para Fisioterapeutas — Conecta con Pacientes que Te Necesitan", "Marketing Fisioterapeutas", "fisioterapeutas", "La fisioterapia privada crece un 12% anual."),
    ("/marketing-para-nutricionistas/", "Marketing para Nutricionistas | Más Pacientes — Comunikoo", "Marketing digital para nutricionistas y dietistas: web, SEO, contenido y captación online.", "Marketing para Nutricionistas — Más Pacientes para Tu Consulta", "Marketing Nutricionistas", "nutricionistas", "El interés por la nutrición se ha disparado un 40%."),
    ("/marketing-para-peluquerias/", "Marketing para Peluquerías | Más Citas — Comunikoo", "Marketing digital para peluquerías y centros de estética: Google Maps, redes sociales e Instagram.", "Marketing para Peluquerías — Agenda Completa Todo el Año", "Marketing Peluquerías", "peluquerías y centros de estética", "Instagram es el escaparate de tu peluquería."),
    ("/marketing-para-coaches/", "Marketing para Coaches | Más Clientes — Comunikoo", "Marketing digital para coaches y terapeutas: web profesional, SEO, contenido y embudos de captación.", "Marketing para Coaches — Atrae Clientes que Valoran Tu Trabajo", "Marketing Coaches", "coaches y profesionales del desarrollo personal", "El coaching en España crece un 20% anual."),
    ("/marketing-para-arquitectos/", "Marketing para Arquitectos | Más Proyectos — Comunikoo", "Marketing digital para estudios de arquitectura: portfolio web, SEO y captación de proyectos.", "Marketing para Arquitectos — Proyectos que Llegan Solos", "Marketing Arquitectos", "arquitectos y estudios de arquitectura", "El 85% de clientes busca arquitecto en Google."),
    ("/marketing-para-agencias-de-viajes/", "Marketing para Agencias de Viajes | Más Reservas — Comunikoo", "Marketing digital para agencias de viajes: SEO, Google Ads, redes sociales y campañas estacionales.", "Marketing para Agencias de Viajes — Más Reservas Online", "Marketing Viajes", "agencias de viajes", "El turismo se ha recuperado y la competencia online es feroz."),
    ("/marketing-para-centros-de-formacion/", "Marketing para Centros de Formación | Más Matrículas — Comunikoo", "Marketing digital para centros de formación y academias: SEO, Google Ads y captación de alumnos.", "Marketing para Centros de Formación — Más Matrículas Online", "Marketing Formación", "centros de formación", "La formación online compite con la presencial: destaca."),
]

for v in VERTICALS:
    svcs = [
        {"title": "SEO Local", "desc": f"Posicionamiento en Google para {v[5]}"},
        {"title": "Google Ads", "desc": f"Campañas de captación para {v[5]}"},
        {"title": "Redes Sociales", "desc": f"Contenido y comunidad para {v[5]}"},
    ]
    ALL_PAGES.append(vert(v[0], v[1], v[2], v[3], v[4], f"Servicio especializado de marketing digital para {v[5]}.", v[5], v[6], svcs,
        faqs=[("¿Cuánto cuesta el marketing para este sector?", "Depende de tus objetivos y competencia. Solicita presupuesto personalizado."), (f"¿Tenéis experiencia con {v[5]}?", f"Sí, tenemos experiencia demostrable trabajando con {v[5]}."), ("¿Qué resultados puedo esperar?", "Resultados medibles desde los primeros meses. Te mostramos casos reales.")]))

# --- GEO PAGES ---
BCN_ZONES = ["Eixample", "Gràcia", "Sarrià-Sant Gervasi", "Born", "Sant Martí", "Poblenou (22@)", "Les Corts", "Hospitalet", "Badalona", "Sant Cugat"]
MAD_ZONES = ["Centro", "Salamanca", "Chamberí", "Retiro", "Chamartín", "Moncloa", "Arganzuela", "Pozuelo", "Las Rozas", "Alcobendas"]

GEO_SERVICES_BCN = [
    ("agencia-marketing-digital", "Agencia Marketing Digital", "Agencia de Marketing Digital Barcelona"),
    ("agencia-seo", "Agencia SEO", "Agencia SEO Barcelona"),
    ("agencia-seo-local", "SEO Local", "SEO Local Barcelona"),
    ("agencia-meta-ads", "Meta Ads", "Agencia Meta Ads Barcelona"),
    ("agencia-facebook-ads", "Facebook Ads", "Agencia Facebook Ads Barcelona"),
    ("diseno-web", "Diseño Web", "Diseño Web Barcelona"),
    ("diseno-web-wordpress", "Diseño WordPress", "Diseño WordPress Barcelona"),
    ("disenador-web", "Diseñador Web", "Diseñador Web Barcelona"),
    ("programador-wordpress", "Programador WordPress", "Programador WordPress Barcelona"),
    ("agencia-wordpress", "Agencia WordPress", "Agencia WordPress Barcelona"),
    ("mantenimiento-wordpress", "Mantenimiento WordPress", "Mantenimiento WordPress Barcelona"),
    ("community-manager", "Community Manager", "Community Manager Barcelona"),
    ("google-ads", "Google Ads", "Google Ads Barcelona"),
    ("experto-google-ads", "Experto Google Ads", "Experto Google Ads Barcelona"),
    ("consultor-google-ads", "Consultor Google Ads", "Consultor Google Ads Barcelona"),
    ("freelance-google-ads", "Freelance Google Ads", "Freelance Google Ads Barcelona"),
    ("gestion-redes-sociales", "Gestión Redes Sociales", "Gestión Redes Sociales Barcelona"),
    ("tienda-online", "Tienda Online", "Tienda Online Barcelona"),
    ("agencia-ecommerce", "Agencia Ecommerce", "Agencia Ecommerce Barcelona"),
    ("diseno-tienda-online", "Diseño Tienda Online", "Diseño Tienda Online Barcelona"),
    ("seo-ecommerce", "SEO Ecommerce", "SEO Ecommerce Barcelona"),
    ("agencia-shopify", "Agencia Shopify", "Agencia Shopify Barcelona"),
    ("agencia-woocommerce", "Agencia WooCommerce", "Agencia WooCommerce Barcelona"),
    ("google-shopping", "Google Shopping", "Google Shopping Barcelona"),
    ("desarrollo-web", "Desarrollo Web", "Desarrollo Web Barcelona"),
]

# Mapping for slugs whose national page is NOT at /servicios/{slug}/
GEO_NATIONAL_URL_OVERRIDES = {
    "agencia-marketing-digital": "/servicios/estrategia-digital/",
    "agencia-seo": "/agencia-seo/",
    "diseno-web": "/diseno-web/",
    "disenador-web": "/diseno-web/",
    "community-manager": "/community-manager/",
    "google-ads": "/agencia-google-ads/",
    "tienda-online": "/tienda-online/",
    "seo-ecommerce": "/servicios/seo-para-ecommerce/",
}

def _national_url(slug):
    """Return the correct national URL for a geo service slug."""
    return GEO_NATIONAL_URL_OVERRIDES.get(slug, f"/servicios/{slug}/")

for slug, svc_name, full_name in GEO_SERVICES_BCN:
    url = f"/{slug}-barcelona/"
    ALL_PAGES.append(geo(
        url,
        f"{full_name} | Expertos Locales — Comunikoo",
        f"{full_name}: equipo local, resultados medibles. +487 proyectos completados con 98% satisfacción. Sin permanencia. Auditoría gratis.",
        f"{full_name} — Expertos Locales en la Ciudad Condal",
        full_name, f"Servicio de {svc_name.lower()} en Barcelona con equipo local y conocimiento del mercado barcelonés.",
        "Barcelona", svc_name, BCN_ZONES,
        [{"url": _national_url(slug), "label": f"{svc_name} (nacional)"}],
        faqs=[
            (f"¿Cuánto cuesta {svc_name.lower()} en Barcelona?", "Solicita presupuesto personalizado. Los precios dependen de tu proyecto y objetivos."),
            ("¿Tenéis oficina en Barcelona?", "Sí, estamos en Aragó 4, Barcelona 08015. Atendemos con cita previa."),
            (f"¿Trabajáis solo en Barcelona ciudad?", "No, también trabajamos con empresas del área metropolitana: Hospitalet, Badalona, Sant Cugat, etc."),
        ],
        address="Aragó 4, Barcelona 08015",
    ))

# Same for Madrid
for slug, svc_name, full_name_bcn in GEO_SERVICES_BCN:
    full_name = full_name_bcn.replace("Barcelona", "Madrid")
    url = f"/{slug}-madrid/"
    ALL_PAGES.append(geo(
        url,
        f"{full_name} | Presencia en Madrid — Comunikoo",
        f"{full_name}: presencia activa, resultados medibles. +487 proyectos completados con 98% satisfacción. Sin permanencia. Auditoría gratis.",
        f"{full_name} — Presencia Activa en la Capital",
        full_name, f"Servicio de {svc_name.lower()} en Madrid con conocimiento del mercado madrileño.",
        "Madrid", svc_name, MAD_ZONES,
        [{"url": _national_url(slug), "label": f"{svc_name} (nacional)"}],
        faqs=[
            (f"¿Cuánto cuesta {svc_name.lower()} en Madrid?", "Solicita presupuesto personalizado sin compromiso."),
            ("¿Tenéis equipo en Madrid?", "Sí, contamos con presencia activa en Madrid y atendemos clientes en toda la Comunidad de Madrid."),
        ],
    ))

# --- OPORTUNIDAD 5: GEO PAGES VALENCIA Y SEVILLA ---
VLC_ZONES = ["Ciutat Vella", "Eixample", "Ruzafa", "Benimaclet", "Campanar", "Patraix", "Jesús", "Poblats Marítims", "L'Olivereta", "Torrent"]
SVQ_ZONES = ["Centro", "Triana", "Nervión", "Macarena", "Los Remedios", "Santa Cruz", "San Pablo", "Bermejales", "Este-Alcosa", "Dos Hermanas"]

GEO_SERVICES_VLC = [
    ("agencia-marketing-digital", "Agencia Marketing Digital", "Agencia Marketing Digital Valencia"),
    ("agencia-seo", "Agencia SEO", "Agencia SEO Valencia"),
    ("diseno-web", "Diseño Web", "Diseño Web Valencia"),
    ("google-ads", "Google Ads", "Google Ads Valencia"),
    ("community-manager", "Community Manager", "Community Manager Valencia"),
    ("tienda-online", "Tienda Online", "Tienda Online Valencia"),
]

for slug, svc_name, full_name in GEO_SERVICES_VLC:
    url = f"/{slug}-valencia/"
    ALL_PAGES.append(geo(
        url,
        f"{full_name} | Agencia Local — Comunikoo",
        f"{full_name}: equipo profesional, resultados medibles. +487 proyectos completados con 98% satisfacción. Sin permanencia. Auditoría gratis.",
        f"{full_name} — Agencia con Presencia en Valencia",
        full_name, f"Servicio de {svc_name.lower()} en Valencia con conocimiento del mercado valenciano.",
        "Valencia", svc_name, VLC_ZONES,
        [{"url": _national_url(slug), "label": f"{svc_name} (nacional)"}],
        faqs=[
            (f"¿Cuánto cuesta {svc_name.lower()} en Valencia?", "Solicita presupuesto personalizado. Los precios dependen de tu proyecto y objetivos."),
            ("¿Tenéis presencia en Valencia?", "Sí, atendemos clientes en Valencia y toda la Comunitat Valenciana."),
            (f"¿Trabajáis solo en Valencia ciudad?", "No, también trabajamos con empresas de Alicante, Castellón y toda la Comunitat."),
        ],
    ))

GEO_SERVICES_SVQ = [
    ("agencia-marketing-digital", "Agencia Marketing Digital", "Agencia Marketing Digital Sevilla"),
    ("agencia-seo", "Agencia SEO", "Agencia SEO Sevilla"),
    ("diseno-web", "Diseño Web", "Diseño Web Sevilla"),
    ("google-ads", "Google Ads", "Google Ads Sevilla"),
]

for slug, svc_name, full_name in GEO_SERVICES_SVQ:
    url = f"/{slug}-sevilla/"
    ALL_PAGES.append(geo(
        url,
        f"{full_name} | Presencia en Sevilla — Comunikoo",
        f"{full_name}: resultados medibles. +487 proyectos completados con 98% satisfacción. Sin permanencia. Auditoría gratis.",
        f"{full_name} — Presencia Activa en Sevilla",
        full_name, f"Servicio de {svc_name.lower()} en Sevilla con conocimiento del mercado andaluz.",
        "Sevilla", svc_name, SVQ_ZONES,
        [{"url": _national_url(slug), "label": f"{svc_name} (nacional)"}],
        faqs=[
            (f"¿Cuánto cuesta {svc_name.lower()} en Sevilla?", "Solicita presupuesto personalizado sin compromiso."),
            ("¿Tenéis equipo en Sevilla?", "Sí, atendemos clientes en Sevilla y toda Andalucía."),
        ],
    ))

# --- PAGES: static ---
STATIC_PAGES = [
    ("/nosotros/", "Sobre Nosotros | Comunikoo — Agencia Marketing Digital Barcelona"),
    ("/contacto/", "Contacto | Comunikoo — Solicita Presupuesto"),
    ("/presupuesto/", "Solicita Presupuesto | Comunikoo"),
    ("/casos-de-exito/", "Casos de Éxito | Comunikoo — Resultados Reales"),
    ("/blog/", "Blog de Marketing Digital | Comunikoo"),
    ("/politica-de-privacidad/", "Política de Privacidad | Comunikoo"),
    ("/aviso-legal/", "Aviso Legal | Comunikoo"),
    ("/politica-de-cookies/", "Política de Cookies | Comunikoo"),
]

# ============================================================
# GENERATOR
# ============================================================

def url_to_path(url):
    """Convert URL to file path: /agencia-seo/ -> servicios/agencia-seo/index.html"""
    if url == '/':
        return 'index.html'
    clean = url.strip('/')
    return f'{clean}/index.html'


def write_page(url, html):
    path = OUTPUT_DIR / url_to_path(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding='utf-8')


def generate():
    print("Generating Comunikoo site...")

    # Load full-content pages from content/ modules
    content_pages, vertical_content = load_content_pages()

    # Override ALL_PAGES with full content where available
    for i, page in enumerate(ALL_PAGES):
        if page['url'] in content_pages:
            ALL_PAGES[i] = content_pages[page['url']]
        elif page['url'] in vertical_content:
            vc = vertical_content[page['url']]
            ALL_PAGES[i].update(vc)
            print(f"  [content] Applied vertical content: {page['url']}")

    # HOME
    write_page('/', build_home())
    print("  ✓ /")

    # SERVICE + VERTICAL + GEO pages
    for page in ALL_PAGES:
        if page['type'] == 'service':
            html = build_service_page(page)
        elif page['type'] == 'vertical':
            html = build_vertical_page(page)
        elif page['type'] == 'geo':
            html = build_geo_page(page)
        else:
            continue
        write_page(page['url'], html)
        print(f"  ✓ {page['url']}")

    # SERVICIOS HUB
    hub_body = '<section class="section"><div class="wrap"><h1>Todos nuestros servicios</h1><p class="text-muted" style="font-size:var(--text-lg)">Encuentra el servicio que necesitas. Cada enlace es una página con información detallada.</p>'
    silos = {
        'SEO': [p for p in ALL_PAGES if p['type']=='service' and '/servicios/agencia-seo' in p['url'] or '/servicios/auditoria' in p['url'] or '/servicios/consultoria-seo' in p['url'] or '/servicios/posicionamiento' in p['url'] or '/servicios/linkbuilding' in p['url']],
    }
    # Simplified hub: list all service pages
    hub_body += '<div style="margin-top:var(--space-8);columns:2;column-gap:var(--space-8)">'
    for p in ALL_PAGES:
        if p['type'] == 'service':
            hub_body += f'<p style="break-inside:avoid"><a href="{p["url"]}">{p["h1_short"]}</a></p>'
    hub_body += '</div></div></section>'
    write_page('/servicios/', base_html("Todos los Servicios | Comunikoo", "Todos los servicios de marketing digital de Comunikoo: SEO, diseño web, Google Ads, redes sociales, ecommerce y más.", "/servicios/", hub_body))
    print("  ✓ /servicios/")

    # STATIC pages (placeholder)
    for url, title in STATIC_PAGES:
        body = f'<section class="section"><div class="wrap-narrow"><h1>{title.split("|")[0].strip()}</h1><p>[Contenido pendiente]</p></div></section>'
        write_page(url, base_html(title, "", url, body))
        print(f"  ✓ {url}")

    # COUNT
    total = 1 + len(ALL_PAGES) + 1 + len(STATIC_PAGES)
    print(f"\n✅ {total} páginas generadas correctamente.")


if __name__ == '__main__':
    generate()
