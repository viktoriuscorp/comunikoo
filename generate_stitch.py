#!/usr/bin/env python3
"""
COMUNIKOO — Static Site Generator v2 (Stitch Design)
Generates all HTML pages using Tailwind CSS + Manrope/Inter fonts
Based on Google Stitch design system
"""
import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR
sys.path.insert(0, str(BASE_DIR))

# ============================================================
# SVG ICONS (replace Material Symbols — saves 1MB font download)
# ============================================================
SVG_ICONS = {
    "search": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "web": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "ads_click": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 2a9 9 0 1 0 5.5 16.1"/><path d="m11 11 5 5"/><path d="m16 16 4.5 4.5"/><circle cx="11" cy="11" r="3"/></svg>',
    "share": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4"/><path d="m8.6 10.5 6.8-4"/></svg>',
    "shopping_cart": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.1 2.1h3.5l2.6 12.5a2 2 0 0 0 2 1.5h7.7a2 2 0 0 0 2-1.5L22 7H6"/></svg>',
    "mail": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    "arrow_forward": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>',
    "expand_more": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>',
    "menu": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>',
    "close": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>',
    "verified": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 L15 8.5 22 9.3 17 14 18.2 21 12 17.8 5.8 21 7 14 2 9.3 9 8.5Z"/></svg>',
    "trending_up": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    "star": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.1 8.3 22 9.2 17 14.1 18.2 21 12 17.8 5.8 21 7 14.1 2 9.2 8.9 8.3 12 2"/></svg>',
    "location_on": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
    "groups": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "schedule": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "dashboard": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
    "lock_open": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>',
    "call": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3.1-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7 12.8 12.8 0 0 0 .7 2.8 2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5 12.8 12.8 0 0 0 2.8.7 2 2 0 0 1 1.7 2z"/></svg>',
    # Fallback icons used in ICONS list
    "edit_note": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4Z"/></svg>',
    "tune": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y1="12" y2="3"/><line x1="2" x2="6" y1="14" y2="14"/><line x1="10" x2="14" y1="8" y2="8"/><line x1="18" x2="22" y1="16" y2="16"/></svg>',
    "link": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.6 1.6"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.6-1.6"/></svg>',
    "speed": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 14 4-4"/><path d="M3.3 19a9.9 9.9 0 0 1 17.4 0"/></svg>',
    "insights": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m7 16 4-8 4 4 4-6"/></svg>',
    "build": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.2 6.2a2.1 2.1 0 0 1-3-3l6.2-6.2a6 6 0 0 1 7.9-7.9z"/></svg>',
    "rocket_launch": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.3-2 5-2 5s3.7-.5 5-2c.7-.7 1-1.8.5-2.5-.5-.7-1.6-.8-2.4-.5z"/><path d="M12 13l-1-1"/><path d="M15 10l-1-1"/><path d="M6 22c0-4 4-8 12-12C22 6 22 2 22 2S18 2 14 6c-4 8-8 12-12 12z"/></svg>',
    "psychology": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a8 8 0 0 0-8 8c0 3.4 2.1 6.3 5 7.5V22h6v-4.5c2.9-1.2 5-4.1 5-7.5a8 8 0 0 0-8-8z"/><path d="M10 17h4"/></svg>',
    "timeline": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m7 12 4-4 4 4 4-6"/></svg>',
    "workspace_premium": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M8.2 14.5 6 22l6-3 6 3-2.2-7.5"/></svg>',
    "auto_awesome": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15 9 22 9.3 17 14 18.5 21 12 17 5.5 21 7 14 2 9.3 9 9"/></svg>',
}

def icon(name, size=24, cls=""):
    """Return SVG icon inline, replacing Material Symbols font."""
    svg = SVG_ICONS.get(name, SVG_ICONS.get('star', ''))
    # Adjust size
    if size != 24:
        svg = svg.replace('width="24"', f'width="{size}"').replace('height="24"', f'height="{size}"')
    if cls:
        svg = svg.replace('<svg ', f'<svg class="{cls}" ')
    return svg

# ============================================================
# RELATIVE URL SYSTEM
# ============================================================
def rel(target_url, current_url):
    """Convert absolute URL to relative path for local file browsing"""
    if target_url == '/':
        target_parts = []
    else:
        target_parts = [p for p in target_url.strip('/').split('/') if p]

    if current_url == '/':
        current_parts = []
    else:
        current_parts = [p for p in current_url.strip('/').split('/') if p]

    ups = len(current_parts)
    if ups == 0:
        if len(target_parts) == 0:
            return "index.html"
        return '/'.join(target_parts) + '/index.html'
    else:
        prefix = '../' * ups
        if len(target_parts) == 0:
            return prefix + 'index.html'
        return prefix + '/'.join(target_parts) + '/index.html'


# ============================================================
# LOAD CONTENT FROM content/ MODULES
# ============================================================
def load_content_pages():
    pages = {}
    verticals = {}
    profiles = {}
    subpages = {}
    content_dir = BASE_DIR / 'content'
    if content_dir.exists():
        for f in content_dir.glob('*.py'):
            if f.name.startswith('__'):
                continue
            mod_name = f.stem
            spec = __import__(f'content.{mod_name}', fromlist=['PAGE_DATA', 'VERTICAL_CONTENT', 'PROFILE_PAGES'])
            if hasattr(spec, 'PAGE_DATA'):
                pd = spec.PAGE_DATA
                pages[pd['url']] = pd
            if hasattr(spec, 'VERTICAL_CONTENT'):
                verticals.update(spec.VERTICAL_CONTENT)
            if hasattr(spec, 'PROFILE_PAGES'):
                profiles.update(spec.PROFILE_PAGES)
    # Load sub-pages from content/subpages/
    subpages_dir = content_dir / 'subpages'
    if subpages_dir.exists():
        for f in subpages_dir.glob('*.py'):
            if f.name.startswith('__'):
                continue
            mod_name = f.stem
            spec = __import__(f'content.subpages.{mod_name}', fromlist=['SUBPAGES'])
            if hasattr(spec, 'SUBPAGES'):
                subpages.update(spec.SUBPAGES)
                print(f"  [subpages] Loaded {len(spec.SUBPAGES)} sub-pages from {f.name}")
    return pages, verticals, profiles, subpages

# ============================================================
# TAILWIND CONFIG — now compiled locally, no CDN needed
TAILWIND_CONFIG = ''  # Kept for compatibility, CSS is in /css/style.css

# ============================================================
# HTML TEMPLATES
# ============================================================

def head_html(title, meta_desc, canonical, schema=""):
    return f'''<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script>setTimeout(function(){{var s=document.createElement('script');s.src='https://www.googletagmanager.com/gtag/js?id=G-WCHWH6J2KC';s.async=true;document.head.appendChild(s);window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-WCHWH6J2KC')}},3000);</script>
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://comunikoo.es{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="CSSPLACEHOLDER">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"></noscript>
{TAILWIND_CONFIG}
<style>
.icon-inline {{ display: inline-flex; align-items: center; vertical-align: middle; }}
details summary {{ cursor: pointer; }}
details summary::-webkit-details-marker {{ display: none; }}

/* Mega menu: no gap between trigger and dropdown */
.mega-trigger {{ position: relative; }}
.mega-trigger > .mega-panel {{ display: none; position: fixed; left: 0; right: 0; top: 72px; z-index: 100; }}
.mega-trigger:hover > .mega-panel {{ display: block; }}
.mega-panel::before {{ content: ''; position: absolute; top: -20px; left: 0; right: 0; height: 20px; }}

/* ── Container (PeterLead style: 1100px max, always centered) ── */
.container {{ max-width: 1100px; margin: 0 auto; padding: 0 2rem; }}

/* ── Section blocks with clear separation ── */
.sec-block {{ padding: 4.5rem 0; }}
@media(min-width:768px) {{ .sec-block {{ padding: 5.5rem 0; }} }}

/* ── Cards: white, shadow, uniform, centered content ── */
.svc-card {{ background: #fff; border-radius: 10px; padding: 2rem 1.5rem; box-shadow: 0 2px 12px rgba(0,0,0,.07); border: 1px solid rgba(0,0,0,.06); text-align: center; transition: all .25s ease; }}
.svc-card:hover {{ box-shadow: 0 6px 24px rgba(0,0,0,.12); border-color: rgba(0,0,0,.1); transform: translateY(-2px); }}
.svc-card .svc-icon {{ width: 52px; height: 52px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-family: 'Manrope', sans-serif; font-weight: 800; font-size: 1.1rem; }}
.svc-card h3 {{ font-family: 'Manrope', sans-serif; font-size: .85rem; font-weight: 700; color: #001e40; margin-bottom: .4rem; }}
.svc-card p {{ font-size: .78rem; line-height: 1.7; color: #43474f; margin: 0; }}

/* ── Card grid: always symmetric ── */
.card-grid {{ display: grid; gap: 1.25rem; margin: 0 auto; }}
.card-grid.g2 {{ grid-template-columns: repeat(2,1fr); max-width: 580px; }}
.card-grid.g3 {{ grid-template-columns: repeat(3,1fr); max-width: 860px; }}
.card-grid.g4 {{ grid-template-columns: repeat(2,1fr); max-width: 580px; }}
.card-grid.g5 {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 1.25rem; max-width: 860px; }}
.card-grid.g5 > * {{ width: calc(33.33% - 1rem); min-width: 200px; }}
.card-grid.g6 {{ grid-template-columns: repeat(3,1fr); max-width: 860px; }}
@media(max-width:767px) {{
  .card-grid {{ grid-template-columns: 1fr !important; max-width: 100% !important; gap: 1rem !important; }}
  .card-grid.g5 > * {{ width: 100% !important; min-width: 0 !important; }}
  .svc-card {{ padding: 1.5rem 1.25rem !important; }}
  .svc-card h3 {{ font-size: .95rem !important; }}
  .svc-card p {{ font-size: .85rem !important; line-height: 1.6 !important; }}
  .svc-card .svc-icon {{ width: 48px !important; height: 48px !important; }}
  .sec-block {{ padding: 2.5rem 0 !important; }}
  .sec-heading h2 {{ font-size: 1.4rem !important; }}
  .sec-intro {{ font-size: .9rem !important; }}
  .prose-block {{ font-size: .9rem !important; }}
  .prose-block h3 {{ font-size: 1rem !important; }}
  .container {{ padding: 0 1.25rem !important; }}
  [style*="grid-template-columns:1fr 1fr"] {{ grid-template-columns: 1fr !important; }}
  [style*="grid-template-columns:repeat"] {{ grid-template-columns: 1fr !important; }}
  [style*="display:grid;grid-template-columns:repeat"] {{ grid-template-columns: repeat(2, 1fr) !important; gap: 1rem !important; }}
}}
@media(max-width:400px) {{
  .card-grid {{ grid-template-columns: 1fr !important; max-width: 320px !important; margin-inline: auto !important; }}
}}

/* Nav pills scrollable on mobile */
.scrollbar-hide {{ -ms-overflow-style: none; scrollbar-width: none; }}
.scrollbar-hide::-webkit-scrollbar {{ display: none; }}

/* Hero & body text responsive */
@media(max-width:767px) {{
  .font-headline.text-3xl {{ font-size: 1.5rem !important; }}
  .font-headline.text-4xl {{ font-size: 1.75rem !important; }}
  p.text-base {{ font-size: .95rem !important; }}
  p.text-lg {{ font-size: 1rem !important; }}
}}

/* ── Prose: text always inside container, left-aligned, readable ── */
.prose-block {{ max-width: 720px; margin: 0 auto; }}
.prose-block h3 {{ font-family: 'Manrope', sans-serif; font-size: 1.1rem; font-weight: 700; color: #001e40; margin: 2.5rem 0 .75rem; display: flex; align-items: center; gap: .5rem; }}
.prose-block p {{ font-size: .9rem; line-height: 1.7; color: #43474f; margin-bottom: 1rem; }}
.prose-block ul {{ padding-left: 1.25rem; margin: 1rem 0; }}
.prose-block li {{ font-size: .9rem; line-height: 1.7; color: #43474f; margin-bottom: .5rem; }}
.prose-block strong {{ color: #001e40; font-weight: 600; }}
.prose-block a {{ color: #904d00; text-decoration: underline; text-underline-offset: 2px; }}
.prose-block a:hover {{ color: #fd8b00; }}

/* ── Section heading ── */
.sec-heading {{ text-align: center; margin-bottom: 2.5rem; }}
.sec-heading h2 {{ font-family: 'Manrope', sans-serif; font-size: 1.65rem; font-weight: 800; color: #001e40; margin: 0; }}
@media(min-width:768px) {{ .sec-heading h2 {{ font-size: 2rem; }} }}
.sec-heading .bar {{ width: 50px; height: 3px; background: #fd8b00; margin: .75rem auto 0; border-radius: 2px; }}

/* ── Intro paragraph (always centered, narrower) ── */
.sec-intro {{ max-width: 640px; margin: 0 auto 2.5rem; text-align: center; font-size: .95rem; line-height: 1.7; color: #43474f; }}
</style>
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://comunikoo.es{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
{schema}
</head>'''


def nav_html(current_url="/"):
    r = lambda target: rel(target, current_url)
    return f'''<nav class="fixed top-0 w-full z-50 bg-white/95 backdrop-blur-lg border-b border-outline-variant/15" style="box-shadow:0 1px 8px rgba(0,0,0,.04)">
<div class="flex justify-between items-center px-6 lg:px-8 py-5 max-w-7xl mx-auto">
<a href="{r('/')}" class="text-2xl font-black tracking-tighter text-primary">Comunikoo</a>
<div class="hidden lg:flex gap-10 items-center font-headline font-bold text-sm tracking-tight">
<div class="mega-trigger">
<a class="text-primary hover:text-secondary-container transition-colors py-4 inline-block" href="{r('/servicios/')}">Servicios</a>
<div class="mega-panel">
<div style="background:#fff;border-top:2px solid #fd8b00;box-shadow:0 12px 40px rgba(0,0,0,.12);padding:2.5rem 0">
<div style="max-width:960px;margin:0 auto;padding:0 2rem;display:grid;grid-template-columns:repeat(4,1fr);gap:2.5rem">
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">SEO</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/agencia-seo/')}">Agencia SEO</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/agencia-seo-local/')}">SEO Local</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/consultoria-seo/')}">Consultoría SEO</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/auditoria-seo/')}">Auditoría SEO</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/posicionamiento-web/')}">Posicionamiento Web</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/linkbuilding/')}">Linkbuilding</a>
</div>
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">Diseño Web</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/diseno-web/')}">Diseño Web</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/diseno-web-wordpress/')}">WordPress</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/tienda-online/')}">Tiendas Online</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/desarrollo-web/')}">Desarrollo Web</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/landing-pages/')}">Landing Pages</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/mantenimiento-web/')}">Mantenimiento Web</a>
</div>
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">Publicidad</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/agencia-google-ads/')}">Google Ads</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/agencia-facebook-ads/')}">Facebook Ads</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/agencia-meta-ads/')}">Meta Ads</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/instagram-ads/')}">Instagram Ads</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/youtube-ads/')}">YouTube Ads</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/publicidad-en-google/')}">Publicidad Google</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/google-shopping/')}">Google Shopping</a>
</div>
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">Redes Sociales</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/community-manager/')}">Community Manager</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/gestion-redes-sociales/')}">Gestión Redes</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/email-marketing/')}">Email Marketing</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/marketing-de-contenidos/')}">Marketing Contenidos</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/servicios/branding/')}">Branding</a>
</div>
</div>
</div>
</div>
</div>
<div class="mega-trigger">
<a class="text-primary hover:text-secondary-container transition-colors py-4 inline-block" href="#">Sectores</a>
<div class="mega-panel">
<div style="background:#fff;border-top:2px solid #fd8b00;box-shadow:0 12px 40px rgba(0,0,0,.12);padding:2rem 0">
<div style="max-width:800px;margin:0 auto;padding:0 2rem;display:grid;grid-template-columns:repeat(4,1fr);gap:2rem">
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">Salud</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-clinicas-dentales/')}">Clínicas Dentales</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-clinicas-esteticas/')}">Clínicas Estéticas</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-psicologos/')}">Psicólogos</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-veterinarias/')}">Veterinarias</a>
</div>
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">Hostelería</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-restaurantes/')}">Restaurantes</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-hoteles/')}">Hoteles</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-gimnasios/')}">Gimnasios</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-academias/')}">Academias</a>
</div>
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">Servicios</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-abogados/')}">Abogados</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-asesorias/')}">Asesorías</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-inmobiliarias/')}">Inmobiliarias</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-empresas-de-reformas/')}">Reformas</a>
</div>
<div>
<h4 style="font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:#737780;margin-bottom:1rem;font-weight:700">Empresas</h4>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-ecommerce/')}">Ecommerce</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-empresas-b2b/')}">Empresas B2B</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-autoescuelas/')}">Autoescuelas</a>
<a class="block text-sm text-primary hover:text-secondary-container py-1.5 font-medium" href="{r('/marketing-para-talleres-de-coches/')}">Talleres</a>
</div>
</div>
</div>
</div>
</div>
<a class="text-primary hover:text-secondary-container transition-colors py-2" href="{r('/nosotros/')}">Nosotros</a>
<a class="text-primary hover:text-secondary-container transition-colors py-2" href="{r('/blog/')}">Blog</a>
<a class="bg-primary text-on-primary px-7 py-2.5 rounded-lg hover:bg-primary-container transition-all active:scale-95" href="{r('/contacto/')}">Auditoría gratis</a>
</div>
<button class="lg:hidden text-primary" id="mobile-menu-btn" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')">
<span class="material-symbols-outlined text-3xl">menu</span>
</button>
</div>
</nav>
<div id="mobile-menu" class="hidden fixed inset-0 z-[200] bg-white lg:hidden">
<div class="flex justify-between items-center px-6 py-5 border-b">
<a href="{r('/')}" class="text-2xl font-black tracking-tighter text-primary">Comunikoo</a>
<button onclick="document.getElementById('mobile-menu').classList.add('hidden')">
<span class="material-symbols-outlined text-3xl text-primary">close</span>
</button>
</div>
<div class="px-6 py-6 overflow-y-auto" style="max-height:calc(100vh - 75px)">

<details style="border-bottom:1px solid #e5e7eb">
<summary style="padding:1rem 0;font-family:Manrope,sans-serif;font-weight:700;font-size:1rem;color:#001e40;display:flex;justify-content:space-between;align-items:center;cursor:pointer">Servicios <span class="material-symbols-outlined" style="font-size:1.2rem">expand_more</span></summary>
<div style="padding:0 0 1rem .75rem;display:flex;flex-direction:column;gap:.25rem">
<p style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#737780;font-weight:700;margin:.5rem 0 .25rem">SEO</p>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/agencia-seo/')}">Agencia SEO</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/agencia-seo-local/')}">SEO Local</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/consultoria-seo/')}">Consultoría SEO</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/posicionamiento-web/')}">Posicionamiento Web</a>
<p style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#737780;font-weight:700;margin:.75rem 0 .25rem">Diseño Web</p>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/diseno-web/')}">Diseño Web</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/diseno-web-wordpress/')}">WordPress</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/tienda-online/')}">Tiendas Online</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/desarrollo-web/')}">Desarrollo Web</a>
<p style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#737780;font-weight:700;margin:.75rem 0 .25rem">Publicidad</p>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/agencia-google-ads/')}">Google Ads</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/agencia-facebook-ads/')}">Facebook Ads</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/agencia-meta-ads/')}">Meta Ads</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/instagram-ads/')}">Instagram Ads</a>
<p style="font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:#737780;font-weight:700;margin:.75rem 0 .25rem">Redes Sociales</p>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/community-manager/')}">Community Manager</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/servicios/email-marketing/')}">Email Marketing</a>
</div>
</details>

<details style="border-bottom:1px solid #e5e7eb">
<summary style="padding:1rem 0;font-family:Manrope,sans-serif;font-weight:700;font-size:1rem;color:#001e40;display:flex;justify-content:space-between;align-items:center;cursor:pointer">Sectores <span class="material-symbols-outlined" style="font-size:1.2rem">expand_more</span></summary>
<div style="padding:0 0 1rem .75rem;display:flex;flex-direction:column;gap:.25rem">
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-restaurantes/')}">Restaurantes</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-hoteles/')}">Hoteles</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-clinicas-dentales/')}">Clínicas Dentales</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-clinicas-esteticas/')}">Clínicas Estéticas</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-abogados/')}">Abogados</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-inmobiliarias/')}">Inmobiliarias</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-ecommerce/')}">Ecommerce</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-gimnasios/')}">Gimnasios</a>
<a style="font-size:.9rem;color:#001e40;padding:.35rem 0;text-decoration:none" href="{r('/marketing-para-empresas-b2b/')}">Empresas B2B</a>
</div>
</details>

<a style="display:block;padding:1rem 0;font-family:Manrope,sans-serif;font-weight:700;font-size:1rem;color:#001e40;text-decoration:none;border-bottom:1px solid #e5e7eb" href="{r('/nosotros/')}">Nosotros</a>
<a style="display:block;padding:1rem 0;font-family:Manrope,sans-serif;font-weight:700;font-size:1rem;color:#001e40;text-decoration:none;border-bottom:1px solid #e5e7eb" href="{r('/blog/')}">Blog</a>
<a style="display:block;padding:1rem 0;font-family:Manrope,sans-serif;font-weight:700;font-size:1rem;color:#001e40;text-decoration:none;border-bottom:1px solid #e5e7eb" href="{r('/contacto/')}">Contacto</a>

<a style="display:block;background:#001e40;color:#fff;text-align:center;font-family:Manrope,sans-serif;font-weight:700;padding:1rem;border-radius:10px;margin-top:1.5rem;text-decoration:none;font-size:1rem" href="{r('/contacto/')}">Auditoría gratuita</a>
</div>
</div>'''


def footer_html(current_url="/"):
    r = lambda target: rel(target, current_url)
    return f'''<footer class="bg-primary w-full py-16 px-6 lg:px-8">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 max-w-7xl mx-auto">
<div class="space-y-4 lg:col-span-1">
<div class="text-xl font-black text-secondary-container">Comunikoo</div>
<p class="text-on-primary-container text-sm max-w-xs">Agencia de Marketing Digital en Barcelona. Expertos en SEO, SEM y Resultados.</p>
<p class="text-on-primary-container text-sm"><a href="mailto:hola@comunikoo.es" class="hover:text-white">hola@comunikoo.es</a></p>
</div>
<div class="space-y-3">
<h4 class="text-white font-bold text-sm uppercase tracking-widest">Servicios</h4>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/agencia-seo/')}">Agencia SEO</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/diseno-web/')}">Diseño Web</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/agencia-google-ads/')}">Google Ads</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/community-manager/')}">Community Manager</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/tienda-online/')}">Tiendas Online</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/email-marketing/')}">Email Marketing</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/branding/')}">Branding</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/agencia-facebook-ads/')}">Facebook Ads</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/desarrollo-web/')}">Desarrollo Web</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/servicios/landing-pages/')}">Landing Pages</a>
</div>
<div class="space-y-3">
<h4 class="text-white font-bold text-sm uppercase tracking-widest">Sectores</h4>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-restaurantes/')}">Restaurantes</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-hoteles/')}">Hoteles</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-clinicas-dentales/')}">Clínicas Dentales</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-clinicas-esteticas/')}">Clínicas Estéticas</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-psicologos/')}">Psicólogos</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-veterinarias/')}">Veterinarias</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-abogados/')}">Abogados</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-inmobiliarias/')}">Inmobiliarias</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-ecommerce/')}">Ecommerce</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-empresas-b2b/')}">B2B</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-gimnasios/')}">Gimnasios</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-asesorias/')}">Asesorías</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-autoescuelas/')}">Autoescuelas</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-academias/')}">Academias</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-empresas-de-reformas/')}">Reformas</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/marketing-para-talleres-de-coches/')}">Talleres</a>
</div>
<div class="space-y-3">
<h4 class="text-white font-bold text-sm uppercase tracking-widest">Ciudades</h4>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/agencia-marketing-digital-barcelona/')}">Barcelona</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/agencia-marketing-digital-madrid/')}">Madrid</a>
<h4 class="text-white font-bold text-sm uppercase tracking-widest mt-6">Recursos</h4>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/nosotros/')}">Nosotros</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/contacto/')}">Contacto</a>
</div>
<div class="space-y-3">
<h4 class="text-white font-bold text-sm uppercase tracking-widest">Legal</h4>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/politica-de-privacidad/')}">Privacidad</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/aviso-legal/')}">Aviso Legal</a>
<a class="block text-on-primary-container text-sm hover:text-white transition-all" href="{r('/politica-de-cookies/')}">Cookies</a>
</div>
</div>
<div class="max-w-7xl mx-auto pt-10 mt-10 border-t border-white/10 flex flex-col md:flex-row justify-between gap-4">
<p class="text-on-primary-container/60 text-sm">&copy; 2026 Comunikoo. Todos los derechos reservados.</p>
<div class="flex gap-4 text-on-primary-container/60 text-sm">
<a href="{r('/politica-de-privacidad/')}" class="hover:text-white">Privacidad</a>
<a href="{r('/aviso-legal/')}" class="hover:text-white">Aviso Legal</a>
<a href="{r('/politica-de-cookies/')}" class="hover:text-white">Cookies</a>
</div>
</div>
</footer>'''


def breadcrumb_html(items, current_url="/"):
    r = lambda target: rel(target, current_url)
    parts = ['<nav class="max-w-7xl mx-auto px-6 lg:px-8 pt-4 pb-2 text-sm text-on-surface-variant" aria-label="Breadcrumb">']
    for i, (label, url) in enumerate(items):
        if i > 0:
            parts.append('<span class="mx-2">›</span>')
        if i < len(items) - 1:
            parts.append(f'<a href="{r(url)}" class="hover:text-secondary-container">{label}</a>')
        else:
            parts.append(f'<span class="text-primary font-semibold">{label}</span>')
    parts.append('</nav>')
    return ''.join(parts)


def faq_html(faqs):
    h = '<div class="space-y-4 max-w-3xl mx-auto">\n'
    for q, a in faqs:
        h += f'''<details class="bg-surface-container-lowest p-6 rounded-xl group">
<summary class="font-headline font-bold text-primary flex justify-between items-center">
{q}
<span class="material-symbols-outlined group-open:rotate-180 transition-transform">expand_more</span>
</summary>
<p class="text-on-surface-variant mt-4 leading-relaxed">{a}</p>
</details>\n'''
    h += '</div>'
    return h


def faq_schema(faqs):
    items = []
    for q, a in faqs:
        clean_a = a.replace('"', '\\"')
        clean_q = q.replace('"', '\\"')
        items.append(f'{{"@type":"Question","name":"{clean_q}","acceptedAnswer":{{"@type":"Answer","text":"{clean_a}"}}}}')
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(items)}]}}
</script>'''


def service_schema(name, desc):
    clean_name = name.replace('"', '\\"')
    clean_desc = desc.replace('"', '\\"')
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Service","name":"{clean_name}","description":"{clean_desc}","provider":{{"@type":"Organization","name":"Comunikoo","url":"https://comunikoo.es","address":{{"@type":"PostalAddress","streetAddress":"Aragó 4","addressLocality":"Barcelona","postalCode":"08015","addressCountry":"ES"}},"telephone":"+34608721015"}},"areaServed":{{"@type":"Country","name":"España"}}}}
</script>'''


def local_business_schema(city, service_name):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"LocalBusiness","name":"Comunikoo - {service_name} {city}","address":{{"@type":"PostalAddress","addressLocality":"{city}","addressCountry":"ES"}},"telephone":"+34608721015","url":"https://comunikoo.es","openingHours":"Mo-Fr 09:00-20:00"}}
</script>'''


# ============================================================
# SERVICE PAGE BUILDER
# ============================================================
def build_service_page(page):
    p = page
    current_url = p['url']
    r = lambda target: rel(target, current_url)
    sections_data = p.get('sections', [])
    faqs = p.get('faqs', [])
    faq_schema_tag = faq_schema(faqs) if faqs else ''
    schema = service_schema(p.get('h1_short', ''), p.get('meta_desc', ''))
    if faq_schema_tag:
        schema += '\n' + faq_schema_tag

    # Breadcrumbs: 3 levels for services, 4 levels for sub-pages
    if p.get('_is_subpage') and p.get('parent'):
        breadcrumbs = breadcrumb_html([
            ("Inicio", "/"),
            ("Servicios", "/servicios/"),
            (p.get('parent_name', 'Servicio'), p['parent']),
            (p['h1_short'], p['url']),
        ], current_url)
    else:
        breadcrumbs = breadcrumb_html([("Inicio", "/"), ("Servicios", "/servicios/"), (p['h1_short'], p['url'])], current_url)

    raw_stats = p.get('sidebar_stats', [
        {"number": "+320%", "label": "tráfico medio"},
        {"number": "487", "label": "proyectos"},
        {"number": "98%", "label": "satisfacción"},
        {"number": "0€", "label": "permanencia"},
    ])
    # Normalize stats: accept both dict and tuple formats
    stats = []
    for s in raw_stats:
        if isinstance(s, dict):
            stats.append(s)
        elif isinstance(s, (list, tuple)) and len(s) >= 2:
            stats.append({"label": s[0], "number": s[1]})

    import re

    def make_clean_summary(raw_text):
        """Create a clean, complete summary from raw text. Never truncated."""
        raw = re.sub(r'<[^>]+>', '', raw_text).strip()
        if not raw:
            return ''
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', raw)
        if not sentences:
            return raw[:80] + '.' if len(raw) > 80 else raw

        first = sentences[0].strip()

        # If first sentence has a colon, use only the part before it (the main statement)
        if ':' in first and len(first) > 80:
            before_colon = first.split(':')[0].strip()
            if len(before_colon) > 20:
                return before_colon + '.'

        # If first sentence is short enough, use it complete
        if len(first) <= 120:
            # Ensure it ends with punctuation
            if not first[-1] in '.!?':
                first += '.'
            return first

        # First sentence too long: take first two clauses (split by comma)
        clauses = first.split(',')
        result = clauses[0].strip()
        if len(clauses) > 1 and len(result + ', ' + clauses[1].strip()) <= 100:
            result = result + ', ' + clauses[1].strip()
        if not result[-1] in '.!?,;:':
            result += '.'
        return result

    def split_section(html):
        parts = re.split(r'<h3[^>]*>', html)
        intro = parts[0].strip() if parts else ''
        items = []
        for part in parts[1:]:
            m = re.match(r'(.*?)</h3>(.*)', part, re.DOTALL)
            if m:
                title = m.group(1).strip()
                body = m.group(2).strip()
                first_p = re.search(r'<p>(.*?)</p>', body, re.DOTALL)
                summary = make_clean_summary(first_p.group(1)) if first_p else ''
                items.append({'title': title, 'summary': summary, 'body': body})
        return intro, items

    PROSE = '[&_p]:mb-4 [&_p]:leading-relaxed [&_ul]:space-y-2 [&_ul]:my-4 [&_ul]:list-disc [&_ul]:pl-6 [&_li]:text-on-surface-variant [&_strong]:text-on-surface [&_strong]:font-semibold [&_a]:text-secondary-container [&_a]:hover:text-secondary [&_a]:underline [&_a]:underline-offset-2'
    ICONS = ['search', 'edit_note', 'tune', 'link', 'speed', 'location_on', 'insights', 'build', 'trending_up', 'verified', 'rocket_launch', 'psychology', 'timeline', 'star', 'workspace_premium', 'auto_awesome']

    # SVG placeholder (inline, 0 weight)
    def svg_img(seed, w=480, h=320):
        cs = [('#003366','#fd8b00','#f0f1f2'), ('#001e40','#904d00','#f3f4f5'), ('#003366','#592300','#edeeef')]
        c = cs[seed % 3]
        return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto rounded-xl"><rect width="{w}" height="{h}" rx="12" fill="{c[2]}"/><rect x="{w//5}" y="{h//4}" width="{w//3}" height="{h//3}" rx="8" fill="{c[0]}" opacity=".1"/><circle cx="{w*2//3}" cy="{h//3}" r="{h//5}" fill="{c[1]}" opacity=".12"/><rect x="{w//6}" y="{h*2//3}" width="{w*2//3}" height="3" rx="2" fill="{c[0]}" opacity=".08"/></svg>'

    BG = ['', 'bg-[#f4f6fa]', '', 'bg-[#edf1f7]', '', 'bg-[#f7f5f0]']

    def detect_layout(section_index, title, items, raw_html):
        t = title.lower()
        n = len(items)
        if '<div class="step' in raw_html or 'paso' in t or 'proceso' in t or 'cómo trabajamos' in t:
            return 'steps'
        if 'caso' in t or 'resultado' in t or 'éxito' in t:
            return 'cases'
        # First section: text + image side by side (not cards)
        if section_index == 0:
            return 'text-image'
        if n >= 4:
            return 'cards'
        if 1 <= n <= 3:
            return 'cards'
        return 'prose'

    content_blocks = ''
    for i, s in enumerate(sections_data):
        raw_html = s.get('html', '<p>Contenido en desarrollo.</p>')
        intro, items = split_section(raw_html)
        bg = BG[i % len(BG)]
        n = len(items)
        layout = detect_layout(i, s['title'], items, raw_html)

        heading = f'<div class="sec-heading"><h2>{s["title"]}</h2><div class="bar"></div></div>'

        intro_html = ''
        if intro:
            clean = re.sub(r'</?p>', '', intro).strip()
            intro_html = f'<div class="sec-intro">{clean}</div>'

        body_html = ''

        # ═══════════════════════════════════════════
        # LAYOUT: TEXT-IMAGE — intro corto + imagen 50/50, luego tarjetas
        # ═══════════════════════════════════════════
        if layout == 'text-image':
            svg_c = [('#003366','#fd8b00','#eef1f6'), ('#001e40','#904d00','#f3f4f5')][i % 2]
            svg = f'<svg viewBox="0 0 460 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;border-radius:16px"><rect width="460" height="400" rx="16" fill="{svg_c[2]}"/><rect x="40" y="50" width="180" height="130" rx="12" fill="{svg_c[0]}" opacity=".08"/><rect x="250" y="80" width="160" height="100" rx="8" fill="{svg_c[1]}" opacity=".1"/><circle cx="140" cy="290" r="70" fill="{svg_c[0]}" opacity=".06"/><circle cx="350" cy="310" r="50" fill="{svg_c[1]}" opacity=".08"/></svg>'

            intro_html = ''  # No intro text — cards are self-explanatory
            # Cards only, no intro paragraph duplicating card content
            if items:
                gcls = f'g{min(n, 6) if n != 4 else 4}'
                card_list = ''
                for ci, item in enumerate(items):
                    icon = ICONS[(i * 4 + ci) % len(ICONS)]
                    badge = f'<div class="svc-icon" style="background:#f0f4ff"><span class="material-symbols-outlined" style="color:#fd8b00;font-size:1.4rem">{icon}</span></div>'
                    card_list += f'<div class="svc-card">{badge}<h3>{item["title"]}</h3><p>{item["summary"]}</p></div>\n'
                body_html = f'<div class="card-grid {gcls}">{card_list}</div>'
            else:
                body_html = f'<div class="prose-block">{raw_html}</div>'

        # ═══════════════════════════════════════════
        # LAYOUT: CARDS — tarjetas uniformes, SIN duplicar
        # ═══════════════════════════════════════════
        elif layout == 'cards':
            intro_html = ''
            gcls = f'g{min(n, 6) if n != 4 else 4}'
            card_list = ''
            for ci, item in enumerate(items):
                icon = ICONS[(i * 4 + ci) % len(ICONS)]
                if n <= 4:
                    badge = f'<div class="svc-icon" style="background:#001e40;color:#fff">{ci+1}</div>'
                else:
                    badge = f'<div class="svc-icon" style="background:#f0f4ff"><span class="material-symbols-outlined" style="color:#fd8b00;font-size:1.4rem">{icon}</span></div>'
                card_list += f'<div class="svc-card">{badge}<h3>{item["title"]}</h3><p>{item["summary"]}</p></div>\n'
            body_html = f'<div class="card-grid {gcls}">{card_list}</div>'

            # Expandable details below for full SEO content (not duplicated — different depth)
            body_html += '\n<div style="max-width:700px;margin:2.5rem auto 0;display:flex;flex-direction:column;gap:.5rem">'
            for ci, item in enumerate(items):
                icon = ICONS[(i * 4 + ci) % len(ICONS)]
                body_html += f'''<details style="background:#fff;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.03);border:1px solid rgba(0,0,0,.04)">
<summary style="padding:.875rem 1.25rem;font-family:Manrope,sans-serif;font-weight:600;font-size:.82rem;color:#001e40;display:flex;align-items:center;gap:.5rem;cursor:pointer">
<span class="material-symbols-outlined" style="color:#fd8b00;font-size:1rem">{icon}</span> {item["title"]} — Leer más</summary>
<div class="prose-block" style="padding:.5rem 1.25rem 1rem 2.75rem;max-width:none;margin:0;font-size:.82rem">{item["body"]}</div>
</details>\n'''
            body_html += '</div>'

        # ═══════════════════════════════════════════
        # LAYOUT: STEPS — tarjetas numeradas en fila
        # ═══════════════════════════════════════════
        elif layout == 'steps':
            intro_html = ''  # Steps cards are self-explanatory
            # Parse: <div class="step-num">01</div>...<h4>Title</h4><p>Desc</p>
            step_blocks = re.findall(r'<div[^>]*class="step-num[^"]*"[^>]*>(.*?)</div>.*?<h4>(.*?)</h4>\s*\n?\s*<p>(.*?)</p>', raw_html, re.DOTALL)
            if not step_blocks:
                # Fallback: try just <h4>+<p>
                step_blocks = [(f'0{si+1}', t, d) for si, (t, d) in enumerate(re.findall(r'<h4>(.*?)</h4>.*?<p>(.*?)</p>', raw_html, re.DOTALL))]
            if step_blocks:
                # Render as numbered cards — short summary only
                gcls = f'g{min(len(step_blocks), 4)}'
                card_list = ''
                for si, (num, stitle, sdesc) in enumerate(step_blocks):
                    short = make_clean_summary(sdesc)
                    card_list += f'''<div class="svc-card">
<div class="svc-icon" style="background:#001e40;color:#fff">{num.strip()}</div>
<h3>{stitle.strip()}</h3>
<p>{short}</p>
</div>\n'''
                body_html = f'<div class="card-grid {gcls}">{card_list}</div>'
            else:
                body_html = f'<div class="prose-block">{raw_html}</div>'

        # ═══════════════════════════════════════════
        # LAYOUT: CASES — stats en tarjetas + casos en tarjetas
        # ═══════════════════════════════════════════
        elif layout == 'cases':
            intro_html = ''  # Stats cards speak for themselves
            # Parse stats: <div class="stat-number ...">value</div><div class="stat-label">label</div>
            stat_matches = re.findall(r'class="[^"]*stat-number[^"]*"[^>]*>(.*?)</div>\s*<div[^>]*class="[^"]*stat-label[^"]*"[^>]*>(.*?)</div>', raw_html, re.DOTALL)
            if stat_matches:
                gcls = f'g{min(len(stat_matches), 4)}'
                body_html += f'<div class="card-grid {gcls}" style="margin-bottom:2.5rem">'
                for sval, slabel in stat_matches:
                    cv = re.sub(r'<[^>]+>', '', sval).strip()
                    cl = re.sub(r'<[^>]+>', '', slabel).strip()
                    body_html += f'''<div class="svc-card">
<div style="font-family:Manrope,sans-serif;font-weight:800;font-size:2.2rem;color:#fd8b00;margin-bottom:.25rem">{cv}</div>
<p style="font-size:.72rem;text-transform:uppercase;letter-spacing:.04em">{cl}</p></div>\n'''
                body_html += '</div>'

            # Cases as cards (from H3 items)
            if items:
                for item in items:
                    body_html += f'''<div style="background:#fff;border-radius:10px;padding:1.75rem;box-shadow:0 2px 12px rgba(0,0,0,.07);border:1px solid rgba(0,0,0,.06);max-width:700px;margin:1.25rem auto">
<h3 style="font-family:Manrope,sans-serif;font-weight:700;font-size:.95rem;color:#001e40;margin:0 0 .6rem">{item["title"]}</h3>
<div class="prose-block" style="max-width:none;margin:0">{item["body"]}</div></div>\n'''

            # Testimonial quote if present
            quote_match = re.search(r'<em>"?(.*?)"?</em>', raw_html, re.DOTALL)
            author_match = re.search(r'—\s*(.*?)(?:</p>|$)', raw_html, re.DOTALL)
            if quote_match:
                quote = quote_match.group(1).strip()
                author = author_match.group(1).strip() if author_match else ''
                body_html += f'''<div style="max-width:700px;margin:2rem auto;text-align:center;padding:2rem;background:#fff;border-radius:10px;box-shadow:0 2px 12px rgba(0,0,0,.07);border:1px solid rgba(0,0,0,.06);border-left:4px solid #fd8b00">
<p style="font-size:.95rem;font-style:italic;color:#001e40;line-height:1.7;margin:0 0 .75rem">"{quote}"</p>
<p style="font-size:.8rem;color:#737780;margin:0">— {author}</p></div>'''

            if not stat_matches and not items:
                body_html = f'<div class="prose-block">{raw_html}</div>'

        # ═══════════════════════════════════════════
        # LAYOUT: PROSE — texto + imagen al lado
        # ═══════════════════════════════════════════
        else:
            # First section (i==0) gets image beside intro text
            if i == 0 and intro:
                flip = 'flex-row-reverse' if i % 2 else ''
                svg_c = [('#003366','#fd8b00','#eef1f6'), ('#001e40','#904d00','#f3f4f5')][i % 2]
                svg = f'<svg viewBox="0 0 480 480" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;border-radius:12px"><rect width="480" height="480" rx="12" fill="{svg_c[2]}"/><rect x="60" y="60" width="160" height="160" rx="12" fill="{svg_c[0]}" opacity=".08"/><circle cx="320" cy="200" r="100" fill="{svg_c[1]}" opacity=".1"/><rect x="80" y="360" width="320" height="4" rx="2" fill="{svg_c[0]}" opacity=".07"/><rect x="120" y="380" width="240" height="4" rx="2" fill="{svg_c[0]}" opacity=".05"/></svg>'
                # Override intro — use it in two-col layout
                intro_html = ''
                clean = re.sub(r'</?p>', '', intro).strip()
                body_html = f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center;max-width:900px;margin:0 auto" class="{flip}">
<div class="prose-block" style="max-width:none;margin:0"><p style="font-size:.95rem;line-height:1.7;color:#43474f">{clean}</p></div>
<div>{svg}</div>
</div>
<style>@media(max-width:767px){{[style*="grid-template-columns:1fr 1fr"]{{grid-template-columns:1fr!important}}}}</style>'''
            else:
                body_html = f'<div class="prose-block">{raw_html}</div>'

        # ── MID CTA (after every 2nd section for max conversions) ──
        mid_cta = ''
        if i % 2 == 1:
            cta_msgs = [
                "Solicita tu auditoría gratuita — sin compromiso",
                "Habla con un experto sobre tu proyecto",
                "Descubre qué podemos hacer por tu negocio",
            ]
            msg = cta_msgs[(i // 2) % len(cta_msgs)]
            mid_cta = f'''<div style="text-align:center;margin-top:3rem;padding:2.5rem 2rem;background:#001e40;border-radius:12px;max-width:700px;margin-left:auto;margin-right:auto">
<p style="font-family:Manrope,sans-serif;font-weight:700;font-size:1.1rem;color:#fff;margin:0 0 .75rem">{msg}</p>
<a style="display:inline-flex;align-items:center;gap:.5rem;background:#fd8b00;color:#603100;padding:.85rem 2.5rem;border-radius:8px;font-family:Manrope,sans-serif;font-weight:700;font-size:.95rem;text-decoration:none" href="{r('/contacto/')}">
{p.get("cta_button_short", "Auditoría gratis")} →</a>
</div>'''

        content_blocks += f'''
<section id="{s["id"]}" class="{bg} sec-block scroll-mt-20">
<div class="container">
{heading}
{intro_html}
{body_html}
{mid_cta}
</div>
</section>\n'''

    # --- FAQ ---
    faq_section = ''
    if faqs:
        faq_section = f'''
<section id="faq" class="bg-surface py-20 lg:py-24 px-6 lg:px-8 scroll-mt-20">
<div class="max-w-4xl mx-auto">
<div class="text-center mb-12">
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-primary">Preguntas frecuentes</h2>
<div class="h-1 w-16 bg-secondary-container mx-auto mt-4"></div>
</div>
{faq_html(faqs)}
</div>
</section>'''

    # --- RELATED SERVICES (always 6 items → 3+3 symmetric) ---
    # ── CONTEXTUAL RELATED SERVICES (by cluster) ──
    SERVICE_CLUSTERS = {
        'seo': [
            ("Agencia SEO", "/servicios/agencia-seo/"),
            ("SEO Local", "/servicios/agencia-seo-local/"),
            ("Auditoría SEO", "/servicios/auditoria-seo/"),
            ("Consultoría SEO", "/servicios/consultoria-seo/"),
            ("Posicionamiento Web", "/servicios/posicionamiento-web/"),
            ("Linkbuilding", "/servicios/linkbuilding/"),
            ("SEO Ecommerce", "/servicios/seo-para-ecommerce/"),
            ("Marketing Contenidos", "/servicios/marketing-de-contenidos/"),
            ("Analítica Web", "/servicios/analitica-web/"),
        ],
        'web': [
            ("Diseño Web", "/servicios/diseno-web/"),
            ("WordPress", "/servicios/diseno-web-wordpress/"),
            ("Desarrollo Web", "/servicios/desarrollo-web/"),
            ("Landing Pages", "/servicios/landing-pages/"),
            ("Mantenimiento Web", "/servicios/mantenimiento-web/"),
            ("Diseño a Medida", "/servicios/diseno-web-a-medida/"),
            ("Web para Empresas", "/servicios/diseno-web-para-empresas/"),
            ("Optimización CRO", "/servicios/optimizacion-cro/"),
        ],
        'ads': [
            ("Google Ads", "/servicios/agencia-google-ads/"),
            ("Facebook Ads", "/servicios/agencia-facebook-ads/"),
            ("Meta Ads", "/servicios/agencia-meta-ads/"),
            ("Instagram Ads", "/servicios/instagram-ads/"),
            ("YouTube Ads", "/servicios/youtube-ads/"),
            ("Publicidad Google", "/servicios/publicidad-en-google/"),
            ("Google Shopping", "/servicios/google-shopping/"),
            ("Landing Pages", "/servicios/landing-pages/"),
        ],
        'social': [
            ("Community Manager", "/servicios/community-manager/"),
            ("Gestión Redes", "/servicios/gestion-redes-sociales/"),
            ("Social Media", "/servicios/social-media-marketing/"),
            ("Publicidad Redes", "/servicios/publicidad-redes-sociales/"),
            ("Marketing Contenidos", "/servicios/marketing-de-contenidos/"),
            ("Inbound Marketing", "/servicios/inbound-marketing/"),
            ("Email Marketing", "/servicios/email-marketing/"),
            ("Branding", "/servicios/branding/"),
        ],
        'ecommerce': [
            ("Tienda Online", "/servicios/tienda-online/"),
            ("Agencia Ecommerce", "/servicios/agencia-ecommerce/"),
            ("Shopify", "/servicios/agencia-shopify/"),
            ("WooCommerce", "/servicios/agencia-woocommerce/"),
            ("PrestaShop", "/servicios/agencia-prestashop/"),
            ("SEO Ecommerce", "/servicios/seo-para-ecommerce/"),
            ("Google Shopping", "/servicios/google-shopping/"),
            ("Email Ecommerce", "/servicios/email-marketing-ecommerce/"),
        ],
    }

    # Detect which cluster this service belongs to
    url_lower = current_url.lower()
    if any(k in url_lower for k in ['seo', 'posicionamiento', 'linkbuilding', 'auditoria']):
        cluster_key = 'seo'
    elif any(k in url_lower for k in ['diseno', 'wordpress', 'desarrollo', 'landing', 'mantenimiento', 'cro', 'web-a-medida', 'web-para-empresa']):
        cluster_key = 'web'
    elif any(k in url_lower for k in ['ads', 'sem', 'publicidad', 'shopping', 'youtube-ads']):
        cluster_key = 'ads'
    elif any(k in url_lower for k in ['community', 'redes', 'social', 'contenidos', 'inbound', 'branding']):
        cluster_key = 'social'
    elif any(k in url_lower for k in ['ecommerce', 'tienda', 'shopify', 'woocommerce', 'prestashop']):
        cluster_key = 'ecommerce'
    else:
        cluster_key = 'seo'

    # Get same-cluster services (excluding self) + 2 from another cluster
    same_cluster = [(n, u) for n, u in SERVICE_CLUSTERS[cluster_key] if u != current_url][:4]
    other_keys = [k for k in SERVICE_CLUSTERS if k != cluster_key]
    cross_cluster = []
    for ok in other_keys:
        for n, u in SERVICE_CLUSTERS[ok]:
            if u != current_url and (n, u) not in same_cluster:
                cross_cluster.append((n, u))
                if len(cross_cluster) >= 2:
                    break
        if len(cross_cluster) >= 2:
            break
    related_items = same_cluster + cross_cluster

    related_cards = ''
    for name, url in related_items:
        related_cards += f'''<a href="{r(url)}" class="svc-card" style="padding:1.25rem;text-decoration:none">
<h3 style="font-size:.8rem">{name}</h3>
</a>\n'''

    # ── VERTICAL LINKS (sectores donde se aplica este servicio) ──
    VERTICAL_LINKS = [
        ("Restaurantes", "/marketing-para-restaurantes/"),
        ("Hoteles", "/marketing-para-hoteles/"),
        ("Clínicas Dentales", "/marketing-para-clinicas-dentales/"),
        ("Clínicas Estéticas", "/marketing-para-clinicas-esteticas/"),
        ("Abogados", "/marketing-para-abogados/"),
        ("Inmobiliarias", "/marketing-para-inmobiliarias/"),
        ("Ecommerce", "/marketing-para-ecommerce/"),
        ("Gimnasios", "/marketing-para-gimnasios/"),
        ("Psicólogos", "/marketing-para-psicologos/"),
        ("Empresas B2B", "/marketing-para-empresas-b2b/"),
        ("Veterinarias", "/marketing-para-veterinarias/"),
        ("Asesorías", "/marketing-para-asesorias/"),
    ]
    # Show 6 verticals
    vert_cards = ''
    for vn, vu in VERTICAL_LINKS[:6]:
        vert_cards += f'''<a href="{r(vu)}" class="svc-card" style="padding:1rem;text-decoration:none">
<h3 style="font-size:.75rem">{vn}</h3>
</a>\n'''

    related_section = f'''
<section class="bg-[#f4f6fa] sec-block">
<div class="container">
<div class="sec-heading"><h2 style="font-size:1.3rem">Servicios relacionados</h2><div class="bar"></div></div>
<div class="card-grid g3">
{related_cards}
</div>
<div style="margin-top:2.5rem">
<div class="sec-heading"><h2 style="font-size:1.1rem">Sectores donde aplicamos este servicio</h2><div class="bar"></div></div>
<div class="card-grid g6" style="margin-top:1.5rem">
{vert_cards}
</div>
</div>
</div>
</section>'''

    # --- STATS BAR ---
    stats_items = ''
    for si, s in enumerate(stats):
        border = 'md:border-l border-outline-variant/20 md:pl-8' if si > 0 else ''
        stats_items += f'''<div class="text-center md:text-left {border}">
<div class="font-headline font-black text-3xl lg:text-4xl text-primary tracking-tighter">{s["number"]}</div>
<p class="text-on-surface-variant font-semibold uppercase tracking-widest text-[10px] mt-1">{s["label"]}</p>
</div>\n'''

    # --- NAV PILLS ---
    nav_pills = ''
    for s in sections_data:
        nav_pills += f'<a href="#{s["id"]}" class="px-4 py-2 rounded-full bg-surface-container-lowest border border-outline-variant/10 text-xs font-bold text-primary hover:bg-secondary-container hover:text-on-secondary-container hover:border-secondary-container transition-all whitespace-nowrap">{s["nav_label"]}</a>\n'
    if faqs:
        nav_pills += '<a href="#faq" class="px-4 py-2 rounded-full bg-surface-container-lowest border border-outline-variant/10 text-xs font-bold text-primary hover:bg-secondary-container hover:text-on-secondary-container hover:border-secondary-container transition-all whitespace-nowrap">FAQ</a>\n'

    # --- SUB-PAGES GRID (for parent pages that have sub-pages) ---
    subpages_section = ''
    child_pages = p.get('_subpages', [])
    if child_pages:
        sp_cards = ''
        SUBPAGE_ICONS = ['description', 'link', 'speed', 'search', 'edit_note', 'auto_awesome', 'insights', 'tune', 'campaign', 'smart_display', 'shopping_cart', 'trending_up', 'replay', 'play_circle', 'laptop', 'phone_iphone', 'brush', 'refresh', 'web', 'photo_camera', 'work', 'music_note', 'create', 'analytics', 'compare', 'inventory', 'payments', 'local_shipping', 'schedule', 'newspaper', 'mail']
        for si, (sp_url, sp_name) in enumerate(child_pages):
            icon = SUBPAGE_ICONS[si % len(SUBPAGE_ICONS)]
            sp_cards += f'''<a href="{r(sp_url)}" class="svc-card" style="text-decoration:none;cursor:pointer">
<div class="svc-icon" style="background:#f0f4ff"><span class="material-symbols-outlined" style="color:#fd8b00;font-size:1.4rem">{icon}</span></div>
<h3>{sp_name}</h3>
<p style="font-size:.75rem;color:#fd8b00;margin-top:.5rem">Ver más →</p>
</a>\n'''
        gcls = f'g{min(len(child_pages), 6) if len(child_pages) != 4 else 4}'
        subpages_section = f'''
<section class="sec-block" style="background:#f0f4f8">
<div class="container">
<div class="sec-heading"><h2>Profundiza en nuestros servicios</h2><div class="bar"></div></div>
<div class="card-grid {gcls}">{sp_cards}</div>
</div>
</section>'''

    # --- SIBLING SUB-PAGES NAVIGATION ---
    siblings_section = ''
    siblings = p.get('siblings', [])
    if siblings:
        sib_cards = ''
        for sib_url, sib_name in siblings:
            sib_cards += f'''<a href="{r(sib_url)}" class="svc-card" style="padding:1.25rem;text-decoration:none">
<span class="material-symbols-outlined" style="font-size:1.4rem;color:#fd8b00;margin-bottom:.4rem">arrow_forward</span>
<h3 style="font-size:.8rem">{sib_name}</h3>
</a>\n'''
        parent_name = p.get('parent_name', 'Servicio')
        parent_url = p.get('parent', '/servicios/')
        siblings_section = f'''
<section class="sec-block" style="background:#edf1f7">
<div class="container">
<div class="sec-heading"><h2 style="font-size:1.3rem">Más sobre {parent_name}</h2><div class="bar"></div></div>
<div class="card-grid g3">{sib_cards}</div>
<div style="text-align:center;margin-top:1.5rem">
<a style="font-family:Manrope,sans-serif;font-weight:700;font-size:.85rem;color:#001e40;text-decoration:none" href="{r(parent_url)}">← Volver a {parent_name}</a>
</div>
</div>
</section>'''

    # ── PAIN POINTS (dynamic by service cluster) ──
    PAIN_POINTS = {
        'seo': [
            # Avatar: empresario que ve a su competencia por delante
            ("Tu competencia aparece en Google antes que tú", "Cada día que no trabajas tu SEO, tus competidores captan los clientes que deberían ser tuyos. Y una vez se posicionan, adelantarlos es más difícil."),
            # Avatar: el que tiene web pero no le llega tráfico
            ("Inviertes en una web pero no genera visitas", "Tener una web bonita sin SEO es como tener una tienda en un callejón sin salida. Nadie la encuentra."),
            # Avatar: el que depende de ads y quiere reducir costes
            ("Dependes de los anuncios para tener visibilidad", "Cuando dejas de pagar, desapareces. El SEO genera tráfico constante sin coste por clic — y el retorno crece cada mes."),
            # Avatar: el que ya contrató una agencia y no funcionó
            ("Ya probaste con otra agencia SEO y no funcionó", "La mayoría de agencias venden humo con informes bonitos. Nosotros medimos en leads y ventas, no en impresiones."),
            # Avatar: el autónomo/pyme con presupuesto ajustado
            ("Crees que el SEO solo es para empresas grandes", "El SEO local permite a negocios pequeños competir de tú a tú con grandes marcas en su zona. Y con menos inversión de lo que piensas."),
        ],
        'web': [
            # Avatar: el que tiene web antigua
            ("Tu web no transmite la profesionalidad de tu negocio", "Los visitantes juzgan tu empresa en 3 segundos. Una web anticuada genera desconfianza y pierdes clientes antes de que lean una sola línea."),
            # Avatar: el frustrado con la velocidad
            ("Tu web es lenta y los usuarios se van", "El 53% de los usuarios abandona si la web tarda más de 3 segundos en cargar. Google también te penaliza por ello."),
            # Avatar: el que tiene visitas pero no convierte
            ("Tu web no genera contactos ni ventas", "Tener visitas sin conversiones es quemar dinero. Tu web debe estar diseñada para vender, no solo para informar."),
            # Avatar: el que no puede actualizar su web
            ("Dependes de un técnico para cada pequeño cambio", "Cada vez que quieres cambiar un texto o subir una imagen, tienes que esperar días y pagar. Eso se acabó."),
            # Avatar: el que necesita web nueva desde cero
            ("No sabes por dónde empezar con tu web", "Briefing, diseño, desarrollo, textos, SEO, hosting... Te acompañamos en todo el proceso sin que tengas que preocuparte de nada."),
        ],
        'ads': [
            # Avatar: el que gasta sin retorno
            ("Gastas en publicidad pero no ves retorno", "Sin optimización profesional, podrías estar tirando el 40-60% de tu presupuesto publicitario en clics que nunca convierten."),
            # Avatar: el que no mide resultados
            ("No sabes si tu inversión en ads es rentable", "Si no mides cada euro invertido con tracking de conversiones, estás tomando decisiones a ciegas."),
            # Avatar: el que compite contra grandes presupuestos
            ("Tu competencia aparece antes que tú en Google Ads", "No gana quien más gasta, sino quien mejor optimiza. Con la estrategia correcta, puedes superar a competidores con más presupuesto."),
            # Avatar: el que gestiona campañas él mismo
            ("Gestionas las campañas tú mismo y no tienes tiempo", "Google Ads cambia constantemente. Sin dedicación diaria y conocimiento actualizado, tu rendimiento cae y tu coste sube."),
            # Avatar: el que tuvo mala experiencia
            ("Tu anterior agencia no te daba explicaciones claras", "Tienes derecho a entender exactamente en qué se gasta tu dinero. Dashboard en tiempo real y reporting transparente."),
        ],
        'social': [
            # Avatar: el que publica sin resultados
            ("Publicas en redes pero no generas clientes", "Tener seguidores no es tener clientes. Necesitas una estrategia que convierta likes en leads y leads en ventas."),
            # Avatar: el empresario sin tiempo
            ("No tienes tiempo para gestionar tus redes", "Tu negocio te necesita vendiendo y gestionando, no pensando qué publicar en Instagram a las 7 de la tarde."),
            # Avatar: el que no conecta con su público
            ("Tu marca no conecta con tu audiencia online", "Las redes sociales son conversación, no escaparate. Si solo hablas de ti, nadie te escucha."),
            # Avatar: el que no sabe qué publicar
            ("Te quedas en blanco sin saber qué contenido crear", "Creamos un calendario editorial completo con contenido estratégico que atrae, educa y convierte a tu cliente ideal."),
            # Avatar: el que publica pero no crece
            ("Llevas meses publicando y tus seguidores no crecen", "Crecer orgánicamente requiere estrategia de hashtags, colaboraciones, contenido viral y publicidad segmentada. No solo constancia."),
        ],
        'ecommerce': [
            # Avatar: el que tiene tienda pero no vende
            ("Tu tienda online no vende lo que debería", "El 97% de los visitantes se van sin comprar. Con optimización de fichas, CRO y SEO cambiamos esa cifra."),
            # Avatar: el que depende de Amazon
            ("Dependes de marketplaces y pagas comisiones altas", "Amazon y otros se llevan un 15-30% de cada venta. Tu tienda propia te da el control, el margen y los datos de tus clientes."),
            # Avatar: el que pierde ventas por abandonos
            ("No sabes por qué los usuarios abandonan el carrito", "El 70% de los carritos se abandonan. Con automatizaciones de email y optimización del checkout, recuperamos una parte significativa."),
            # Avatar: el que no sabe qué plataforma elegir
            ("No sabes si elegir Shopify, WooCommerce o PrestaShop", "Cada plataforma tiene sus ventajas según tu caso. Te asesoramos para que elijas la que mejor se adapta a tu negocio y presupuesto."),
            # Avatar: el que vende pero no escala
            ("Vendes pero no consigues escalar tu facturación", "Escalar un ecommerce requiere SEO, publicidad, email marketing y logística optimizada trabajando en conjunto. No canales sueltos."),
        ],
    }

    pain_points = PAIN_POINTS.get(cluster_key, PAIN_POINTS['seo'])

    pain_html = ''
    for pi, (pain_title, pain_desc) in enumerate(pain_points):
        pain_html += f'''<div class="flex gap-4 items-start">
<div style="flex-shrink:0;width:40px;height:40px;border-radius:50%;background:#fff1f0;display:flex;align-items:center;justify-content:center;font-size:1.2rem">✗</div>
<div>
<h3 style="font-family:Manrope,sans-serif;font-weight:700;font-size:.95rem;color:#001e40;margin:0 0 .25rem">{pain_title}</h3>
<p style="font-size:.85rem;line-height:1.7;color:#43474f;margin:0">{pain_desc}</p>
</div>
</div>\n'''

    # ── SOLUTION BRIDGE (unique per cluster) ──
    service_short = p.get('h1_short', 'nuestro servicio')
    SOLUTION_TEXTS = {
        'seo': f'El SEO no es suerte ni trucos — es estrategia, datos y ejecución constante. Nuestro equipo ha posicionado más de 487 proyectos en Google. Sabemos exactamente qué hacer para que tu negocio escale posiciones y capte el tráfico que tu competencia se lleva hoy.',
        'web': f'Una web profesional no es un gasto, es tu mejor comercial — trabaja para ti 24/7, 365 días al año. Diseñamos webs que transmiten confianza en 3 segundos, cargan en menos de 2 y convierten visitantes en clientes reales.',
        'ads': f'Cada euro que inviertes en publicidad debe volver multiplicado. Gestionamos más de 5.8 millones de euros en campañas con un enfoque obsesivo en el ROAS. Si tu publicidad no es rentable, cambiamos la estrategia hasta que lo sea.',
        'social': f'Las redes sociales no van de publicar bonito — van de construir una comunidad que confíe en tu marca y compre. Convertimos seguidores en clientes con contenido estratégico, no aleatorio.',
        'ecommerce': f'Tu tienda online puede facturar mucho más de lo que factura hoy. Optimizamos cada paso del funnel — desde que el usuario te encuentra hasta que completa la compra — para que cada visita cuente.',
    }
    solution_text = SOLUTION_TEXTS.get(cluster_key, f'Con {service_short} de Comunikoo transformamos estos problemas en oportunidades de crecimiento para tu negocio.')

    body = f'''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20">

<!-- HERO -->
<section class="relative bg-gradient-to-b from-surface-container-low to-surface px-6 lg:px-8 overflow-hidden">
<div class="max-w-7xl mx-auto py-16 lg:py-24 text-center relative z-10">
{breadcrumbs}
<span class="inline-block px-4 py-1.5 rounded-full bg-white/80 border border-outline-variant/20 text-primary font-bold text-xs uppercase tracking-widest mt-6 mb-6">{p["h1_short"]}</span>
<h1 class="font-headline font-extrabold text-4xl md:text-5xl lg:text-6xl text-primary leading-[1.08] tracking-tight max-w-4xl mx-auto">{p["h1"]}</h1>
<p class="text-base md:text-lg text-on-surface-variant max-w-2xl mx-auto mt-6 leading-relaxed">{p.get("intro", "")}</p>
<div class="flex flex-wrap gap-4 justify-center mt-8">
<a class="bg-secondary-container text-on-secondary-container px-8 py-4 rounded-lg font-bold shadow-xl shadow-secondary-container/20 hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">{p.get("cta_button_short", "Auditoría gratis")}</a>
<a class="px-8 py-4 rounded-lg font-bold text-primary border-2 border-primary/10 hover:bg-white transition-all" href="#problema">¿Te suena esto? ↓</a>
</div>
</div>
<div class="absolute top-10 right-10 w-64 h-64 bg-secondary-container/5 rounded-full blur-3xl"></div>
<div class="absolute bottom-10 left-10 w-48 h-48 bg-primary/5 rounded-full blur-3xl"></div>
</section>

<!-- PAIN POINTS — Conexión emocional -->
<section id="problema" class="bg-[#fdf6f3] py-16 px-6 lg:px-8 scroll-mt-20">
<div style="max-width:700px;margin:0 auto">
<p style="text-align:center;font-family:Manrope,sans-serif;font-weight:700;font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:#c0392b;margin-bottom:1rem">¿Te identificas con alguno de estos problemas?</p>
<div style="display:flex;flex-direction:column;gap:1.5rem">
{pain_html}
</div>
</div>
</section>

<!-- SOLUTION BRIDGE — De problema a solución -->
<section class="bg-primary py-14 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<p class="text-secondary-container font-bold text-sm uppercase tracking-widest mb-3">La solución</p>
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-white mb-4">{solution_text}</h2>
<a class="inline-block bg-secondary-container text-on-secondary-container px-8 py-3.5 rounded-lg font-bold hover:bg-secondary transition-all active:scale-95 mt-2" href="{r('/contacto/')}">Cuéntanos tu caso →</a>
</div>
</section>

<!-- STATS -->
<section class="bg-surface border-y border-outline-variant/15 py-10">
<div class="max-w-5xl mx-auto px-6 lg:px-8">
<div class="grid grid-cols-2 md:grid-cols-{len(stats)} gap-6 md:gap-4">
{stats_items}
</div>
</div>
</section>

<!-- NAV PILLS -->
<section class="py-5 px-6 lg:px-8 border-b border-outline-variant/10 sticky top-[64px] bg-surface/95 backdrop-blur-md z-30">
<div class="max-w-5xl mx-auto flex gap-2 overflow-x-auto scrollbar-hide justify-center">
{nav_pills}
</div>
</section>

<!-- CONTENT BLOCKS -->
{content_blocks}

{faq_section}

{subpages_section}

{siblings_section}

{related_section}

<!-- CTA FINAL — Detalle de lo que incluye -->
<section class="bg-primary py-24 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<p class="text-secondary-container font-bold text-sm uppercase tracking-widest mb-4">Da el primer paso</p>
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-white mb-4">{p.get("cta_title", "¿Empezamos?")}</h2>
<p class="text-on-primary-container text-base mb-6">{p.get("cta_desc", "Solicita tu auditoría gratuita. Sin compromiso.")}</p>
<div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-md mx-auto mb-8 text-left">
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container">✓</span> Análisis completo de tu situación</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container">✓</span> Estudio de tu competencia</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container">✓</span> Plan de acción personalizado</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container">✓</span> Sin compromiso ni permanencia</p>
</div>
<a class="inline-block bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">{p.get("cta_button", "Auditoría gratuita")} →</a>
<p class="text-on-primary-container/50 text-xs mt-4">Respuesta en menos de 24h. Sin llamadas no deseadas.</p>
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''

    return head_html(p['title'], p.get('meta_desc', ''), p['url'], schema) + '\n' + body


# ============================================================
# VERTICAL (SECTOR) PAGE BUILDER
# ============================================================
def build_vertical_page(page):
    p = page
    current_url = p['url']
    r = lambda target: rel(target, current_url)
    faqs = p.get('faqs', [])
    faq_schema_tag = faq_schema(faqs) if faqs else ''
    schema = service_schema(p.get('h1_short', ''), p.get('meta_desc', ''))
    if faq_schema_tag:
        schema += '\n' + faq_schema_tag

    breadcrumbs = breadcrumb_html([("Inicio", "/"), ("Sectores", "#"), (p['h1_short'], p['url'])], current_url)

    services_cards = ''
    for svc in p.get('services', []):
        services_cards += f'''<div class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] group hover:bg-primary transition-all duration-500">
<div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center mb-6 group-hover:bg-secondary-container transition-colors">
<span class="material-symbols-outlined text-primary group-hover:text-on-secondary-container">star</span>
</div>
<h3 class="font-headline font-bold text-xl text-primary mb-3 group-hover:text-white">{svc["title"]}</h3>
<p class="text-on-surface-variant group-hover:text-white/80 leading-relaxed text-sm">{svc["desc"]}</p>
</div>\n'''

    faq_section = ''
    if faqs:
        faq_section = f'''<section class="py-24 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-4xl mx-auto">
<h2 class="font-headline font-extrabold text-3xl md:text-4xl text-primary mb-10 text-center">Preguntas frecuentes</h2>
{faq_html(faqs)}
</div>
</section>'''

    # Testimonial
    testimonial = ''
    if p.get('testimonial_quote'):
        author_parts = p.get('testimonial_author', 'Cliente').split(',', 1)
        name = author_parts[0].strip()
        role = author_parts[1].strip() if len(author_parts) > 1 else ''
        testimonial = f'''<section class="py-24 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<div class="text-secondary-container mb-6 flex gap-1 justify-center">
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
</div>
<p class="text-xl italic text-on-surface leading-relaxed mb-8">"{p["testimonial_quote"]}"</p>
<p class="font-bold text-primary">{name}</p>
<p class="text-xs text-on-surface-variant">{role}</p>
</div>
</section>'''

    body = f'''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20">
{breadcrumbs}

<!-- HERO -->
<section class="px-6 lg:px-8 max-w-7xl mx-auto py-16 lg:py-24 text-center">
<span class="inline-block px-4 py-1.5 rounded-full bg-secondary-container/20 text-secondary font-bold text-xs uppercase tracking-widest mb-6">{p.get("sector_name", "Sector").title()}</span>
<h1 class="font-headline font-extrabold text-4xl md:text-5xl lg:text-6xl text-primary leading-[1.08] tracking-tight max-w-4xl mx-auto">{p["h1"]}</h1>
<p class="text-base md:text-lg text-on-surface-variant max-w-2xl mx-auto mt-6 leading-relaxed">{p.get("intro", "")}</p>
<p class="font-headline font-extrabold text-xl md:text-2xl text-secondary-container mt-8">{p.get("hook_stat", "")}</p>
<a class="inline-block bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg shadow-xl shadow-secondary-container/20 hover:bg-secondary transition-all active:scale-95 mt-8" href="{r('/contacto/')}">{p.get("cta_button", "Auditoría gratuita")}</a>
</section>

<!-- SERVICES GRID -->
<section class="py-24 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-7xl mx-auto">
<h2 class="font-headline font-extrabold text-3xl md:text-4xl text-primary mb-12 text-center">Lo que hacemos para <span class="text-secondary-container">{p.get("sector_name", "tu sector")}</span></h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{services_cards}
</div>
</div>
</section>

{testimonial}

<!-- SERVICIOS RELACIONADOS PARA ESTE SECTOR -->
<section class="py-20 px-6 lg:px-8 bg-[#f4f6fa]">
<div class="max-w-5xl mx-auto">
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-primary mb-4 text-center">Servicios de marketing digital para {p.get("sector_name", "tu sector")}</h2>
<p class="text-on-surface-variant text-center max-w-2xl mx-auto mb-10">Combinamos diferentes canales de marketing digital para maximizar los resultados en tu sector.</p>
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
<a href="{r('/servicios/agencia-seo/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">SEO y Posicionamiento</h3><p style="font-size:.7rem">Posiciona tu negocio en Google</p></a>
<a href="{r('/servicios/agencia-seo-local/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">SEO Local</h3><p style="font-size:.7rem">Google Maps y pack local</p></a>
<a href="{r('/servicios/diseno-web/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">Diseño Web</h3><p style="font-size:.7rem">Web profesional que convierte</p></a>
<a href="{r('/servicios/agencia-google-ads/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">Google Ads</h3><p style="font-size:.7rem">Clientes desde el primer día</p></a>
<a href="{r('/servicios/community-manager/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">Redes Sociales</h3><p style="font-size:.7rem">Contenido que conecta</p></a>
<a href="{r('/servicios/email-marketing/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">Email Marketing</h3><p style="font-size:.7rem">Fideliza y genera repetición</p></a>
<a href="{r('/servicios/branding/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">Branding</h3><p style="font-size:.7rem">Identidad de marca</p></a>
<a href="{r('/servicios/optimizacion-cro/')}" class="svc-card" style="padding:1.25rem;text-decoration:none"><h3 style="font-size:.8rem">CRO</h3><p style="font-size:.7rem">Optimización de conversión</p></a>
</div>
</div>
</section>

<!-- OTROS SECTORES -->
<section class="py-16 px-6 lg:px-8">
<div class="max-w-5xl mx-auto">
<h2 class="font-headline font-bold text-xl text-primary mb-8 text-center">También trabajamos con otros sectores</h2>
<div class="flex flex-wrap justify-center gap-3">'''

    other_verticals = [
        ("Restaurantes", "/marketing-para-restaurantes/"),
        ("Hoteles", "/marketing-para-hoteles/"),
        ("Clínicas Dentales", "/marketing-para-clinicas-dentales/"),
        ("Clínicas Estéticas", "/marketing-para-clinicas-esteticas/"),
        ("Abogados", "/marketing-para-abogados/"),
        ("Inmobiliarias", "/marketing-para-inmobiliarias/"),
        ("Ecommerce", "/marketing-para-ecommerce/"),
        ("Gimnasios", "/marketing-para-gimnasios/"),
        ("Psicólogos", "/marketing-para-psicologos/"),
        ("B2B", "/marketing-para-empresas-b2b/"),
        ("Veterinarias", "/marketing-para-veterinarias/"),
        ("Asesorías", "/marketing-para-asesorias/"),
        ("Academias", "/marketing-para-academias/"),
        ("Autoescuelas", "/marketing-para-autoescuelas/"),
        ("Reformas", "/marketing-para-empresas-de-reformas/"),
        ("Talleres", "/marketing-para-talleres-de-coches/"),
    ]
    vert_pills = ''
    for vn, vu in other_verticals:
        if vu != current_url:
            vert_pills += f'<a href="{r(vu)}" class="px-4 py-2 rounded-full bg-white border border-black/[.06] shadow-[0_1px_4px_rgba(0,0,0,.05)] text-xs font-bold text-primary hover:bg-primary hover:text-white transition-all no-underline">{vn}</a>\n'

    body_end = f'''{vert_pills}
</div>
</div>
</section>

{faq_section}

<!-- CTA -->
<section class="bg-primary py-24 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<h2 class="font-headline font-extrabold text-3xl md:text-4xl text-white mb-6">{p.get("cta_title", "¿Empezamos?")}</h2>
<a class="inline-block bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">{p.get("cta_button", "Auditoría gratuita")}</a>
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''

    return head_html(p['title'], p.get('meta_desc', ''), p['url'], schema) + '\n' + body + body_end


# ============================================================
# GEO PAGE BUILDER
# ============================================================
def build_geo_page(page):
    p = page
    current_url = p['url']
    r = lambda target: rel(target, current_url)
    city = p['city']
    faqs = p.get('faqs', [])
    faq_schema_tag = faq_schema(faqs) if faqs else ''
    schema = local_business_schema(city, p['service_name'])
    if faq_schema_tag:
        schema += '\n' + faq_schema_tag

    breadcrumbs = breadcrumb_html([("Inicio", "/"), (city, f"/agencia-marketing-digital-{city.lower()}/"), (p['h1_short'], p['url'])], current_url)

    services_links = ''
    for svc in p.get('related_services', []):
        services_links += f'<a href="{r(svc["url"])}" class="block bg-surface-container-lowest p-6 rounded-xl hover:bg-primary group transition-all duration-300"><h3 class="font-headline font-bold text-primary group-hover:text-white">{svc["label"]}</h3></a>\n'

    zones = ', '.join(p.get('zones', []))

    faq_section = ''
    if faqs:
        faq_section = f'''<section class="py-24 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-4xl mx-auto">
<h2 class="font-headline font-extrabold text-3xl text-primary mb-10 text-center">Preguntas frecuentes sobre {p["service_name"]} en {city}</h2>
{faq_html(faqs)}
</div>
</section>'''

    body = f'''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20">
{breadcrumbs}

<section class="px-6 lg:px-8 max-w-7xl mx-auto py-16 lg:py-24 text-center">
<span class="inline-block px-4 py-1.5 rounded-full bg-surface-container-high text-primary font-bold text-xs uppercase tracking-widest mb-6">{city}</span>
<h1 class="font-headline font-extrabold text-4xl md:text-5xl lg:text-6xl text-primary leading-[1.1] tracking-tighter max-w-4xl mx-auto">{p["h1"]}</h1>
<p class="text-lg md:text-xl text-on-surface-variant max-w-2xl mx-auto mt-6 leading-relaxed">{p.get("intro", "")}</p>
<p class="text-on-surface-variant mt-4">Barcelona, España · <a href="mailto:hola@comunikoo.es" class="text-secondary-container">hola@comunikoo.es</a></p>
</section>

<section class="py-16 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-7xl mx-auto">
<h2 class="font-headline font-extrabold text-3xl text-primary mb-8 text-center">Nuestros servicios en {city}</h2>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{services_links}
</div>
</div>
</section>

<section class="py-16 px-6 lg:px-8">
<div class="max-w-4xl mx-auto text-center">
<h2 class="font-headline font-extrabold text-2xl text-primary mb-4">Zonas de {city} donde trabajamos</h2>
<p class="text-on-surface-variant">{zones}</p>
</div>
</section>

{faq_section}

<section class="bg-primary py-24 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<h2 class="font-headline font-extrabold text-3xl text-white mb-6">¿Buscas {p["service_name"]} en {city}?</h2>
<a class="inline-block bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">Solicita presupuesto</a>
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''

    return head_html(p['title'], p.get('meta_desc', ''), p['url'], schema) + '\n' + body


# ============================================================
# HOME PAGE BUILDER
# ============================================================
def build_home():
    current_url = "/"
    r = lambda target: rel(target, current_url)

    org_schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Comunikoo","url":"https://comunikoo.es","logo":"https://comunikoo.es/img/logo.svg","address":{"@type":"PostalAddress","streetAddress":"Aragó 4","addressLocality":"Barcelona","postalCode":"08015","addressCountry":"ES"},"telephone":"+34608721015","email":"hola@comunikoo.es","sameAs":[]}
</script>'''

    home_faqs = [
        ("¿Cuánto cuesta contratar una agencia de marketing digital?",
         "El coste de contratar una agencia de marketing digital depende del tipo de servicio, la competencia en tu sector y tus objetivos de negocio. En Comunikoo, los planes de SEO empiezan desde 490 euros al mes, las campañas de Google Ads desde 350 euros al mes de gestión (más inversión publicitaria), y el diseño web desde 1.200 euros. Ofrecemos presupuesto personalizado sin compromiso para que sepas exactamente qué inversión necesitas."),
        ("¿Qué servicios ofrece una agencia de marketing digital?",
         "Una agencia de marketing digital completa como Comunikoo ofrece servicios de SEO y posicionamiento web, diseño y desarrollo web, publicidad en Google Ads y redes sociales, gestión de redes sociales con community manager, email marketing, branding, tiendas online y analítica web. El objetivo es cubrir todos los canales digitales para maximizar la visibilidad y las ventas de tu negocio."),
        ("¿Cuánto tiempo tardan en verse resultados?",
         "Los resultados dependen del canal. La publicidad en Google Ads y redes sociales genera resultados casi inmediatos desde la primera semana. El SEO es una estrategia a medio-largo plazo: los primeros resultados se ven entre 3 y 6 meses, con crecimiento sostenido a partir de ahí. El diseño web tiene impacto inmediato en la imagen de marca y la conversión. En todos los casos, proporcionamos reporting mensual para que veas la evolución."),
        ("¿Necesito contratar todos los servicios o puedo elegir?",
         "Puedes elegir exactamente los servicios que necesitas. No obligamos a contratar paquetes cerrados. Muchos clientes empiezan con un servicio (por ejemplo, SEO o Google Ads) y van ampliando según resultados. Te asesoramos sobre qué canales tienen más sentido para tu negocio y presupuesto."),
        ("¿Cómo mido el ROI del marketing digital?",
         "En Comunikoo proporcionamos un dashboard en tiempo real donde puedes ver métricas clave: tráfico web, posiciones en Google, leads generados, coste por adquisición, tasa de conversión y retorno de inversión. Además, enviamos informes mensuales detallados con análisis y recomendaciones. Configuramos el tracking completo con Google Analytics 4 y Google Tag Manager para que cada euro invertido sea medible."),
        ("¿Trabajáis con empresas pequeñas?",
         "Sí, trabajamos con empresas de todos los tamaños: desde autónomos y startups hasta pymes y grandes empresas. Adaptamos la estrategia y el presupuesto a cada caso. Muchos de nuestros mejores casos de éxito son pequeñas empresas que han multiplicado su facturación gracias al marketing digital."),
        ("¿Trabajáis con clientes de toda España?",
         "Sí, aunque nuestra sede está en Barcelona, trabajamos con clientes de toda España. Atendemos tanto de forma presencial como por videoconferencia. Tenemos presencia activa en Barcelona y Madrid, y gestionamos proyectos en todas las comunidades autónomas."),
        ("¿Ofrecéis contrato sin permanencia?",
         "Sí, todos nuestros servicios son sin permanencia. Trabajamos mes a mes y nos ganamos tu confianza con resultados, no con contratos de larga duración. Puedes cancelar en cualquier momento con un preaviso de 30 días. El 98 por ciento de nuestros clientes renuevan porque ven resultados reales."),
    ]

    faq_schema_tag = faq_schema(home_faqs)

    schema = org_schema + '\n' + faq_schema_tag

    # All 49 services organized by category for the complete grid
    all_services_grid = ''

    seo_services = [
        ("Agencia SEO", "Posicionamiento web orgánico en Google", "/servicios/agencia-seo/"),
        ("SEO Local", "Google Maps y pack local para negocios", "/servicios/agencia-seo-local/"),
        ("Consultoría SEO", "Asesoramiento estratégico SEO experto", "/servicios/consultoria-seo/"),
        ("Auditoría SEO", "Diagnóstico completo de tu web", "/servicios/auditoria-seo/"),
        ("Posicionamiento Web", "Primeras posiciones en buscadores", "/servicios/posicionamiento-web/"),
        ("Linkbuilding", "Backlinks de calidad para autoridad", "/servicios/linkbuilding/"),
        ("SEO para Ecommerce", "SEO especializado en tiendas online", "/servicios/seo-para-ecommerce/"),
    ]

    web_services = [
        ("Diseño Web", "Webs profesionales que convierten", "/servicios/diseno-web/"),
        ("WordPress", "Diseño web en WordPress a medida", "/servicios/diseno-web-wordpress/"),
        ("Desarrollo Web", "Programación a medida y APIs", "/servicios/desarrollo-web/"),
        ("Landing Pages", "Páginas de alta conversión", "/servicios/landing-pages/"),
        ("Mantenimiento Web", "Soporte técnico y seguridad", "/servicios/mantenimiento-web/"),
        ("Diseño Web a Medida", "Sin plantillas, diseño único", "/servicios/diseno-web-a-medida/"),
        ("Diseño Web Empresas", "Webs corporativas profesionales", "/servicios/diseno-web-para-empresas/"),
        ("Agencia WordPress", "Partner WordPress especializado", "/servicios/agencia-wordpress/"),
        ("Mantenimiento WordPress", "Seguridad y actualizaciones WP", "/servicios/mantenimiento-wordpress/"),
    ]

    ads_services = [
        ("Google Ads", "Campañas rentables en Google", "/servicios/agencia-google-ads/"),
        ("Facebook Ads", "Publicidad en Facebook", "/servicios/agencia-facebook-ads/"),
        ("Meta Ads", "Ecosistema Meta completo", "/servicios/agencia-meta-ads/"),
        ("Instagram Ads", "Publicidad visual en Instagram", "/servicios/instagram-ads/"),
        ("YouTube Ads", "Publicidad en video", "/servicios/youtube-ads/"),
        ("Publicidad en Google", "Anúnciate en Google", "/servicios/publicidad-en-google/"),
        ("Google Shopping", "Tus productos en Google", "/servicios/google-shopping/"),
        ("Social Ads", "Publicidad en redes sociales", "/servicios/publicidad-redes-sociales/"),
        ("Publicidad Ecommerce", "Campañas para tiendas online", "/servicios/publicidad-tiendas-online/"),
    ]

    ecommerce_services = [
        ("Tiendas Online", "Ecommerce listo para vender", "/servicios/tienda-online/"),
        ("Agencia Ecommerce", "Estrategia 360 para tiendas", "/servicios/agencia-ecommerce/"),
        ("Diseño Tienda Online", "Ecommerce que enamora", "/servicios/diseno-tienda-online/"),
        ("Agencia Shopify", "Partner Shopify España", "/servicios/agencia-shopify/"),
        ("Agencia WooCommerce", "WordPress para ecommerce", "/servicios/agencia-woocommerce/"),
        ("Agencia PrestaShop", "Desarrollo PrestaShop", "/servicios/agencia-prestashop/"),
        ("CRO Ecommerce", "Optimización de conversión", "/servicios/cro-ecommerce/"),
        ("Email Ecommerce", "Automatizaciones de email", "/servicios/email-marketing-ecommerce/"),
    ]

    social_services = [
        ("Community Manager", "Gestión profesional de redes", "/servicios/community-manager/"),
        ("Gestión Redes Sociales", "Estrategia y ejecución", "/servicios/gestion-redes-sociales/"),
        ("Email Marketing", "Campañas con el mayor ROI", "/servicios/email-marketing/"),
        ("Marketing de Contenidos", "Contenido que posiciona", "/servicios/marketing-de-contenidos/"),
        ("Social Media Marketing", "Redes con ROI", "/servicios/social-media-marketing/"),
        ("Inbound Marketing", "Atrae clientes con valor", "/servicios/inbound-marketing/"),
    ]

    branding_services = [
        ("Branding", "Identidad de marca potente", "/servicios/branding/"),
        ("Estrategia Digital", "Plan de marketing integral", "/servicios/estrategia-digital/"),
        ("Analítica Web", "GA4, datos y dashboards", "/servicios/analitica-web/"),
        ("CRO", "Optimización de conversión", "/servicios/optimizacion-cro/"),
    ]

    def render_service_category(cat_name, services):
        cards = ''
        for name, desc, url in services:
            cards += f'<a href="{r(url)}" class="bg-white p-5 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] hover:bg-primary hover:border-primary group transition-all duration-300 no-underline"><h4 class="font-headline font-bold text-sm text-primary group-hover:text-white">{name}</h4><p class="text-xs text-on-surface-variant group-hover:text-white/70 mt-1">{desc}</p></a>\n'
        return f'''<div class="mb-8">
<h3 class="font-headline font-bold text-xl text-primary mb-4">{cat_name}</h3>
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
{cards}
</div>
</div>'''

    all_services_grid = (
        render_service_category("SEO y Posicionamiento Web", seo_services)
        + render_service_category("Diseño y Desarrollo Web", web_services)
        + render_service_category("Publicidad Digital", ads_services)
        + render_service_category("Ecommerce y Tiendas Online", ecommerce_services)
        + render_service_category("Redes Sociales y Contenidos", social_services)
        + render_service_category("Branding y Estrategia", branding_services)
    )

    # All 16 sectors
    sectors = [
        ("Restaurantes", "SEO local + reseñas + Google Maps", "/marketing-para-restaurantes/"),
        ("Hoteles", "Reservas directas, menos comisiones OTAs", "/marketing-para-hoteles/"),
        ("Clínicas Dentales", "+300% leads de pacientes", "/marketing-para-clinicas-dentales/"),
        ("Clínicas Estéticas", "Pacientes premium, sector en auge", "/marketing-para-clinicas-esteticas/"),
        ("Psicólogos", "Captación ética y efectiva", "/marketing-para-psicologos/"),
        ("Veterinarias", "Sector pet en pleno crecimiento", "/marketing-para-veterinarias/"),
        ("Abogados", "El 96% busca abogado en Google", "/marketing-para-abogados/"),
        ("Asesorías", "Diferénciate en mercado saturado", "/marketing-para-asesorias/"),
        ("Inmobiliarias", "Leads compradores y vendedores", "/marketing-para-inmobiliarias/"),
        ("Reformas", "Más presupuestos solicitados", "/marketing-para-empresas-de-reformas/"),
        ("Autoescuelas", "Más alumnos matriculados", "/marketing-para-autoescuelas/"),
        ("Talleres", "Más clientes desde Google Maps", "/marketing-para-talleres-de-coches/"),
        ("Gimnasios", "Más socios todo el año", "/marketing-para-gimnasios/"),
        ("Academias", "Captación de alumnos online", "/marketing-para-academias/"),
        ("Ecommerce", "Estrategia 360 para tu tienda", "/marketing-para-ecommerce/"),
        ("B2B", "Leads cualificados para empresas", "/marketing-para-empresas-b2b/"),
    ]

    sectors_grid = ''
    for name, desc, url in sectors:
        sectors_grid += f'''<a href="{r(url)}" class="bg-surface-container-lowest p-6 rounded-xl hover:bg-primary group transition-all duration-300 no-underline text-center">
<h3 class="font-headline font-bold text-primary group-hover:text-white">{name}</h3>
<p class="text-sm text-on-surface-variant group-hover:text-white/70 mt-1">{desc}</p>
</a>\n'''

    # Build FAQ section
    faq_section_html = faq_html(home_faqs)

    body = '''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20 overflow-x-hidden">

<!-- HERO -->
<section class="relative min-h-[80vh] flex items-center justify-center px-6 lg:px-8 max-w-7xl mx-auto py-20 lg:py-32">
<div class="max-w-4xl mx-auto text-center">
<span class="inline-block px-4 py-1.5 rounded-full bg-surface-container-high text-primary font-bold text-xs uppercase tracking-widest mb-6">Agencia de Marketing Digital en Barcelona · Google Partner</span>
<h1 class="font-headline font-extrabold text-4xl md:text-5xl lg:text-6xl text-primary leading-[1.08] tracking-tight">
Agencia de Marketing Digital en Barcelona — <span class="text-secondary-container">Resultados Medibles, Sin Permanencia</span>
</h1>
<p class="text-base md:text-lg text-on-surface-variant max-w-2xl mx-auto mt-6 leading-relaxed">
Agencia de marketing digital en Barcelona especializada en SEO, diseño web, Google Ads y redes sociales. Estrategias basadas en datos que multiplican tu visibilidad y facturación. Sin permanencia. Dashboard en tiempo real.
</p>
<div class="flex flex-wrap gap-4 mt-8 justify-center">
<a class="bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg shadow-xl shadow-secondary-container/20 hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">Auditoría gratuita</a>
<a class="px-10 py-4 rounded-lg font-bold text-lg text-primary border-2 border-primary/10 hover:bg-surface-container-low transition-all" href="{r('/servicios/')}">Ver servicios</a>
</div>
</div>
</section>

<!-- TRUST BAR -->
<section class="py-12 bg-surface-container-lowest border-y border-outline-variant/20">
<div class="max-w-7xl mx-auto px-6 lg:px-8">
<p class="text-center text-xs uppercase tracking-widest text-on-surface-variant font-bold mb-8">Confían en nosotros</p>
<div class="flex flex-wrap justify-center items-center gap-10 md:gap-16 opacity-60">
<span class="font-headline font-black text-xl text-primary">TechStart</span>
<span class="font-headline font-black text-xl text-primary">ClinicaPro</span>
<span class="font-headline font-black text-xl text-primary">FoodGroup</span>
<span class="font-headline font-black text-xl text-primary">LegalPartners</span>
<span class="font-headline font-black text-xl text-primary">SportLife</span>
<span class="font-headline font-black text-xl text-primary">HomeDesign</span>
</div>
</div>
</section>

<!-- STATS -->
<section class="bg-surface-container-low py-20">
<div class="max-w-7xl mx-auto px-6 lg:px-8">
<div class="grid grid-cols-2 md:grid-cols-4 gap-12 md:gap-8">
<div class="text-center md:text-left">
<div class="font-headline font-black text-4xl lg:text-5xl text-primary tracking-tighter">+320%</div>
<p class="text-on-tertiary-container font-semibold uppercase tracking-widest text-xs mt-2">tráfico orgánico medio</p>
</div>
<div class="text-center md:text-left md:border-l border-outline-variant/30 md:pl-8">
<div class="font-headline font-black text-4xl lg:text-5xl text-primary tracking-tighter">5.8M€</div>
<p class="text-on-tertiary-container font-semibold uppercase tracking-widest text-xs mt-2">gestionados en campañas</p>
</div>
<div class="text-center md:text-left md:border-l border-outline-variant/30 md:pl-8">
<div class="font-headline font-black text-4xl lg:text-5xl text-primary tracking-tighter">98%</div>
<p class="text-on-tertiary-container font-semibold uppercase tracking-widest text-xs mt-2">clientes satisfechos</p>
</div>
<div class="text-center md:text-left md:border-l border-outline-variant/30 md:pl-8">
<div class="font-headline font-black text-4xl lg:text-5xl text-secondary-container tracking-tighter">487</div>
<p class="text-on-tertiary-container font-semibold uppercase tracking-widest text-xs mt-2">proyectos entregados</p>
</div>
</div>
</div>
</section>

<!-- CTA 1: PAIN POINT — ¿Tu competencia te está ganando? -->
<section class="bg-primary py-16 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<p class="text-secondary-container font-bold text-sm uppercase tracking-widest mb-4">¿Te suena esto?</p>
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-white mb-4">Tu competencia aparece en Google antes que tú. Tus clientes potenciales los encuentran a ellos, no a ti.</h2>
<p class="text-on-primary-container text-base mb-8 max-w-xl mx-auto">Cada día que pasa sin una estrategia digital, estás regalando clientes. Nosotros lo cambiamos.</p>
<a class="inline-block bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">Solicita tu auditoría gratuita →</a>
<p class="text-on-primary-container/60 text-xs mt-4">Sin compromiso. Te respondemos en menos de 24h.</p>
</div>
</section>

<!-- SERVICES MAIN 6 -->
<section class="py-28 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="mb-16 text-center max-w-3xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-6">Servicios de Marketing Digital — Todo lo que Tu Negocio Necesita</h2>
<p class="text-on-surface-variant text-lg leading-relaxed">En Comunikoo ofrecemos todos los servicios de marketing digital que tu empresa necesita para crecer online. Desde el posicionamiento en Google hasta la gestión de redes sociales, pasando por el diseño web y las campañas de publicidad. Todo bajo un mismo equipo, con una estrategia integrada que maximiza cada euro invertido.</p>
<div class="h-1.5 w-24 bg-secondary-container mx-auto mt-6"></div>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
<a href="{r('/servicios/agencia-seo/')}" class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] group hover:bg-primary transition-all duration-500 no-underline">
<div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center mb-6 group-hover:bg-secondary-container transition-colors"><span class="material-symbols-outlined text-primary group-hover:text-on-secondary-container">search</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3 group-hover:text-white">SEO y Posicionamiento Web</h3>
<p class="text-on-surface-variant group-hover:text-white/80 leading-relaxed text-sm">Posicionamos tu negocio en las primeras posiciones de Google con estrategia de SEO probada. Auditoría técnica, keyword research, contenidos optimizados y link building de calidad. El canal con mejor retorno a largo plazo para cualquier negocio.</p>
</a>
<a href="{r('/servicios/diseno-web/')}" class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] group hover:bg-primary transition-all duration-500 no-underline">
<div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center mb-6 group-hover:bg-secondary-container transition-colors"><span class="material-symbols-outlined text-primary group-hover:text-on-secondary-container">web</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3 group-hover:text-white">Diseño Web Profesional</h3>
<p class="text-on-surface-variant group-hover:text-white/80 leading-relaxed text-sm">Webs rápidas, bonitas y que convierten visitantes en clientes. Diseño responsive, optimizado para SEO y con experiencia de usuario pensada para vender. WordPress, desarrollo a medida y tiendas online.</p>
</a>
<a href="{r('/servicios/agencia-google-ads/')}" class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] group hover:bg-primary transition-all duration-500 no-underline">
<div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center mb-6 group-hover:bg-secondary-container transition-colors"><span class="material-symbols-outlined text-primary group-hover:text-on-secondary-container">ads_click</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3 group-hover:text-white">Google Ads y SEM</h3>
<p class="text-on-surface-variant group-hover:text-white/80 leading-relaxed text-sm">Campañas de publicidad en Google rentables que generan clientes reales desde el primer día. Google Partner con más de 5.8 millones de euros gestionados en campañas. Búsqueda, Shopping, Display y YouTube.</p>
</a>
<a href="{r('/servicios/community-manager/')}" class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] group hover:bg-primary transition-all duration-500 no-underline">
<div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center mb-6 group-hover:bg-secondary-container transition-colors"><span class="material-symbols-outlined text-primary group-hover:text-on-secondary-container">share</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3 group-hover:text-white">Redes Sociales</h3>
<p class="text-on-surface-variant group-hover:text-white/80 leading-relaxed text-sm">Community manager profesional, estrategia de contenido y publicidad en redes sociales. Instagram, Facebook, LinkedIn y TikTok. Contenido que conecta con tu audiencia y convierte seguidores en clientes.</p>
</a>
<a href="{r('/servicios/tienda-online/')}" class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] group hover:bg-primary transition-all duration-500 no-underline">
<div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center mb-6 group-hover:bg-secondary-container transition-colors"><span class="material-symbols-outlined text-primary group-hover:text-on-secondary-container">shopping_cart</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3 group-hover:text-white">Tiendas Online</h3>
<p class="text-on-surface-variant group-hover:text-white/80 leading-relaxed text-sm">Shopify, WooCommerce y PrestaShop. Creamos tiendas online profesionales listas para vender desde el día uno. Diseño orientado a conversión, pasarela de pago integrada y SEO para ecommerce.</p>
</a>
<a href="{r('/servicios/email-marketing/')}" class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] group hover:bg-primary transition-all duration-500 no-underline">
<div class="w-12 h-12 rounded-lg bg-surface-container-high flex items-center justify-center mb-6 group-hover:bg-secondary-container transition-colors"><span class="material-symbols-outlined text-primary group-hover:text-on-secondary-container">mail</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3 group-hover:text-white">Email Marketing</h3>
<p class="text-on-surface-variant group-hover:text-white/80 leading-relaxed text-sm">Automatizaciones, newsletters y campañas de email que convierten. El canal digital con mayor retorno de inversión. Segmentación avanzada, flows automatizados y diseño profesional.</p>
</a>
</div>
</section>

<!-- CTA 2: BENEFIT — Resultados en semanas -->
<section class="py-16 px-6 lg:px-8">
<div class="max-w-4xl mx-auto bg-[#f0f4ff] rounded-2xl p-10 md:p-14 text-center">
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-primary mb-4">¿Quieres saber exactamente qué está fallando en tu marketing digital?</h2>
<p class="text-on-surface-variant text-base max-w-xl mx-auto mb-6">Te hacemos una auditoría completa de tu web, tu SEO, tu publicidad y tus redes sociales. Gratis. Sin letra pequeña. En 48h tienes un informe con acciones concretas para mejorar.</p>
<div class="flex flex-wrap gap-4 justify-center">
<a class="bg-secondary-container text-on-secondary-container px-8 py-4 rounded-lg font-bold hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">Quiero mi auditoría gratis</a>
</div>
<div class="flex flex-wrap justify-center gap-6 mt-6 text-xs text-on-surface-variant">
<span class="flex items-center gap-1">✓ Sin compromiso</span>
<span class="flex items-center gap-1">✓ Respuesta en 24h</span>
<span class="flex items-center gap-1">✓ Sin permanencia</span>
</div>
</div>
</section>

<!-- WHY COMUNIKOO -->
<section class="py-28 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-7xl mx-auto">
<div class="text-center mb-16 max-w-3xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-6">¿Por Qué Elegir Comunikoo como Tu Agencia de Marketing Digital?</h2>
<p class="text-on-surface-variant text-lg leading-relaxed">No somos una agencia de marketing digital más. En Comunikoo nos diferenciamos por nuestro enfoque en resultados reales, transparencia total y un compromiso genuino con el crecimiento de tu negocio. Estas son las razones por las que más de 487 empresas han confiado en nosotros.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="w-12 h-12 rounded-lg bg-secondary-container/20 flex items-center justify-center mb-4"><span class="material-symbols-outlined text-secondary-container">lock_open</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Sin permanencia</h3>
<p class="text-on-surface-variant leading-relaxed text-sm">Trabajamos mes a mes y nos ganamos tu confianza con resultados, no con contratos de larga duración. Puedes cancelar cuando quieras con 30 días de preaviso. El 98 por ciento de nuestros clientes renuevan porque ven retorno real de su inversión en marketing digital.</p>
</div>
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="w-12 h-12 rounded-lg bg-secondary-container/20 flex items-center justify-center mb-4"><span class="material-symbols-outlined text-secondary-container">dashboard</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Dashboard en tiempo real</h3>
<p class="text-on-surface-variant leading-relaxed text-sm">Accede en cualquier momento a tu panel personalizado con todas las métricas de tu proyecto: tráfico, posiciones en Google, leads, conversiones y ROI. Transparencia total sobre qué se está haciendo y qué resultados está generando tu inversión en marketing digital.</p>
</div>
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="w-12 h-12 rounded-lg bg-secondary-container/20 flex items-center justify-center mb-4"><span class="material-symbols-outlined text-secondary-container">trending_up</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Enfocados en ROI</h3>
<p class="text-on-surface-variant leading-relaxed text-sm">No perseguimos métricas vanidosas. Nos enfocamos en lo que importa para tu negocio: leads cualificados, ventas y facturación. Cada estrategia de marketing digital que implementamos tiene un objetivo claro de retorno y lo medimos escrupulosamente.</p>
</div>
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="w-12 h-12 rounded-lg bg-secondary-container/20 flex items-center justify-center mb-4"><span class="material-symbols-outlined text-secondary-container">groups</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Equipo senior dedicado</h3>
<p class="text-on-surface-variant leading-relaxed text-sm">Tu proyecto lo llevan profesionales con más de 5 años de experiencia cada uno. Nada de becarios ni juniors aprendiendo con tu presupuesto. Tienes un interlocutor directo que conoce tu negocio y toma decisiones estratégicas de marketing digital informadas.</p>
</div>
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="w-12 h-12 rounded-lg bg-secondary-container/20 flex items-center justify-center mb-4"><span class="material-symbols-outlined text-secondary-container">verified</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">+487 proyectos completados</h3>
<p class="text-on-surface-variant leading-relaxed text-sm">Más de 487 proyectos de marketing digital completados con éxito en múltiples sectores y ciudades. Desde restaurantes locales hasta empresas B2B con facturación millonaria. Cada proyecto nos ha enseñado algo que aplicamos en el tuyo.</p>
</div>
</div>
</div>
</section>

<!-- METHODOLOGY -->
<section class="py-28 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="text-center mb-16 max-w-3xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-6">Cómo Trabajamos — Metodología Probada en +487 Proyectos</h2>
<p class="text-on-surface-variant text-lg leading-relaxed">Nuestra metodología de trabajo ha sido refinada a lo largo de más de 487 proyectos de marketing digital. Cada fase está diseñada para maximizar resultados y minimizar riesgos. Así es como convertimos tu inversión en crecimiento real.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
<div class="text-center">
<div class="w-16 h-16 rounded-2xl bg-secondary-container flex items-center justify-center mx-auto mb-6"><span class="font-headline font-black text-2xl text-on-secondary-container">1</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Auditoría</h3>
<p class="text-on-surface-variant text-sm leading-relaxed">Analizamos tu web, tu competencia, tu sector y tus canales actuales. Identificamos oportunidades de mejora y definimos el punto de partida de tu estrategia de marketing digital con datos reales.</p>
</div>
<div class="text-center">
<div class="w-16 h-16 rounded-2xl bg-secondary-container flex items-center justify-center mx-auto mb-6"><span class="font-headline font-black text-2xl text-on-secondary-container">2</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Estrategia</h3>
<p class="text-on-surface-variant text-sm leading-relaxed">Diseñamos un plan de acción personalizado con objetivos claros, KPIs medibles y un calendario de implementación. Priorizamos las acciones de mayor impacto para tu negocio y presupuesto.</p>
</div>
<div class="text-center">
<div class="w-16 h-16 rounded-2xl bg-secondary-container flex items-center justify-center mx-auto mb-6"><span class="font-headline font-black text-2xl text-on-secondary-container">3</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Implementación</h3>
<p class="text-on-surface-variant text-sm leading-relaxed">Ejecutamos la estrategia con nuestro equipo senior. SEO técnico y de contenidos, campañas de publicidad, diseño web, gestión de redes sociales y todo lo que tu proyecto necesite para crecer.</p>
</div>
<div class="text-center">
<div class="w-16 h-16 rounded-2xl bg-secondary-container flex items-center justify-center mx-auto mb-6"><span class="font-headline font-black text-2xl text-on-secondary-container">4</span></div>
<h3 class="font-headline font-bold text-xl text-primary mb-3">Reporting</h3>
<p class="text-on-surface-variant text-sm leading-relaxed">Informes mensuales detallados con análisis de resultados, optimizaciones realizadas y próximos pasos. Acceso permanente a tu dashboard en tiempo real con todas las métricas de tu proyecto.</p>
</div>
</div>
</section>

<!-- CTA 3: URGENCY — No pierdas más tiempo -->
<section class="bg-primary py-16 px-6 lg:px-8">
<div class="max-w-4xl mx-auto flex flex-col md:flex-row items-center gap-8">
<div class="flex-1 text-center md:text-left">
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-white mb-3">Cada mes sin estrategia digital es dinero que pierdes</h2>
<p class="text-on-primary-container text-base">Mientras tú dudas, tu competencia está captando los clientes que deberían ser tuyos. Empezamos en menos de 48 horas.</p>
</div>
<div class="flex-shrink-0">
<a class="inline-block bg-secondary-container text-on-secondary-container px-8 py-4 rounded-lg font-bold text-lg hover:bg-secondary transition-all active:scale-95 whitespace-nowrap" href="{r('/contacto/')}">Empezar ahora →</a>
</div>
</div>
</section>

<!-- TESTIMONIALS -->
<section class="py-24 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-7xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-12 text-center">Resultados Reales — Casos de Éxito de Marketing Digital</h2>
<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="text-secondary-container mb-4 flex gap-1">
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
</div>
<p class="text-on-surface italic leading-relaxed mb-6">"Pasamos de 200 a 3.400 visitas orgánicas al mes en 6 meses. Comunikoo entiende de negocio, no solo de SEO. Han transformado nuestra presencia digital por completo."</p>
<p class="font-headline font-bold text-primary text-sm">María López</p>
<p class="text-xs text-on-surface-variant">CEO, Clínica dental — Barcelona</p>
<p class="text-secondary-container font-bold text-sm mt-3">+1.600% tráfico orgánico</p>
</div>
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="text-secondary-container mb-4 flex gap-1">
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
</div>
<p class="text-on-surface italic leading-relaxed mb-6">"Las campañas de Google Ads nos generan un ROAS de 8x. Por cada euro que invertimos en publicidad, recuperamos ocho. El equipo de Comunikoo es excepcional en la optimización."</p>
<p class="font-headline font-bold text-primary text-sm">Carlos Ruiz</p>
<p class="text-xs text-on-surface-variant">Director, Ecommerce moda — Madrid</p>
<p class="text-secondary-container font-bold text-sm mt-3">ROAS 8x en Google Ads</p>
</div>
<div class="bg-surface-container-lowest p-8 rounded-xl">
<div class="text-secondary-container mb-4 flex gap-1">
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
<span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">star</span>
</div>
<p class="text-on-surface italic leading-relaxed mb-6">"Nos rediseñaron la web y montaron una estrategia de SEO local. Ahora somos el restaurante mejor posicionado de nuestra zona. Las reservas online se han triplicado."</p>
<p class="font-headline font-bold text-primary text-sm">Ana Martín</p>
<p class="text-xs text-on-surface-variant">Propietaria, Restaurante — Barcelona</p>
<p class="text-secondary-container font-bold text-sm mt-3">+200% reservas online</p>
</div>
</div>
</div>
</section>

<!-- ALL SERVICES COMPLETE GRID -->
<section class="py-28 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="text-center mb-16 max-w-3xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-6">Todos Nuestros Servicios de Marketing Digital</h2>
<p class="text-on-surface-variant text-lg leading-relaxed">Descubre el catálogo completo de servicios de marketing digital que ofrecemos en Comunikoo. Cada servicio está diseñado para impulsar un aspecto específico de tu presencia online. Puedes contratar servicios individuales o combinarlos en una estrategia integral.</p>
</div>
{all_services_grid}
</section>

<!-- CTA 4: SOCIAL PROOF — Únete a +487 empresas -->
<section class="py-16 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<p class="font-headline font-black text-5xl md:text-6xl text-primary mb-4">487+</p>
<h2 class="font-headline font-bold text-2xl text-primary mb-4">empresas ya han confiado en nosotros para hacer crecer su negocio</h2>
<p class="text-on-surface-variant text-base mb-8 max-w-xl mx-auto">Desde startups hasta empresas consolidadas. En más de 30 sectores diferentes. ¿Será el tuyo el siguiente caso de éxito?</p>
<a class="inline-block bg-secondary-container text-on-secondary-container px-8 py-4 rounded-lg font-bold hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">Quiero ser el próximo caso de éxito</a>
</div>
</section>

<!-- SECTORS -->
<section class="py-28 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-7xl mx-auto">
<div class="text-center mb-16 max-w-3xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-6">Marketing Digital Especializado por Sector</h2>
<p class="text-on-surface-variant text-lg leading-relaxed">Conocemos los retos específicos de cada industria. No es lo mismo el marketing digital para un restaurante que para un despacho de abogados o una tienda online. Por eso ofrecemos estrategias de marketing digital especializadas para cada sector, con conocimiento profundo de sus particularidades, su competencia y el comportamiento de sus clientes.</p>
</div>
<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
{sectors_grid}
</div>
</div>
</section>

<!-- GEO / CITIES -->
<section class="py-28 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="text-center mb-16 max-w-3xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-6">Agencia de Marketing Digital en Barcelona y Madrid</h2>
<p class="text-on-surface-variant text-lg leading-relaxed">Nuestra sede central está en Barcelona, desde donde atendemos a clientes de toda el área metropolitana: Eixample, Gràcia, Sarrià-Sant Gervasi, Born, Poblenou (22@), Les Corts, Hospitalet de Llobregat, Badalona y Sant Cugat. También contamos con presencia activa en Madrid, donde damos servicio a empresas de toda la capital y su zona de influencia.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
<a href="{r('/agencia-marketing-digital-barcelona/')}" class="bg-surface-container-lowest p-10 rounded-2xl hover:shadow-xl transition-all no-underline">
<div class="font-headline font-extrabold text-4xl text-primary mb-2">Barcelona</div>
<p class="text-on-surface-variant">Oficina central — Barcelona</p>
<p class="text-on-surface-variant text-sm mt-2">SEO, diseño web, Google Ads, redes sociales y todos nuestros servicios de marketing digital en Barcelona y área metropolitana.</p>
</a>
<a href="{r('/agencia-marketing-digital-madrid/')}" class="bg-surface-container-lowest p-10 rounded-2xl hover:shadow-xl transition-all no-underline">
<div class="font-headline font-extrabold text-4xl text-primary mb-2">Madrid</div>
<p class="text-on-surface-variant">Presencia activa en la capital</p>
<p class="text-on-surface-variant text-sm mt-2">Todos los servicios de nuestra agencia de marketing digital disponibles para empresas en Madrid, con reuniones presenciales y virtuales.</p>
</a>
</div>
<div class="mt-8 text-center">
<p class="text-on-surface-variant leading-relaxed max-w-3xl mx-auto">Aunque tenemos oficina física en Barcelona, trabajamos con clientes de toda España. Nuestro modelo de trabajo combina reuniones presenciales (cuando es posible) con comunicación digital fluida, dashboard en tiempo real y videollamadas periódicas. No importa dónde esté tu empresa: tendrás el mismo nivel de servicio, atención y resultados.</p>
</div>
</section>

<!-- WHAT IS A DIGITAL MARKETING AGENCY -->
<section class="py-28 px-6 lg:px-8 bg-surface-container-low">
<div class="max-w-4xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-8 text-center">¿Qué es una Agencia de Marketing Digital y Qué Hace?</h2>
<div class="prose prose-lg max-w-none text-on-surface-variant leading-relaxed [&_p]:mb-4 [&_strong]:text-on-surface">
<p>Una <strong>agencia de marketing digital</strong> es una empresa especializada en ayudar a negocios a crecer a través de canales online. A diferencia de las agencias de publicidad tradicional, una agencia de marketing digital trabaja exclusivamente en el entorno digital: buscadores como Google, redes sociales, email, páginas web y plataformas de publicidad online.</p>
<p>Los principales servicios que ofrece una <strong>agencia de marketing digital en Barcelona</strong> como Comunikoo incluyen el <a href="{r('/servicios/agencia-seo/')}">posicionamiento SEO</a> para aparecer en los primeros resultados de Google de forma orgánica, el <a href="{r('/servicios/diseno-web/')}">diseño web profesional</a> orientado a conversión, las <a href="{r('/servicios/agencia-google-ads/')}">campañas de Google Ads</a> para generar clientes de forma inmediata, la <a href="{r('/servicios/community-manager/')}">gestión de redes sociales</a> para construir comunidad y marca, y el <a href="{r('/servicios/email-marketing/')}">email marketing</a> para fidelizar y recuperar clientes.</p>
<p>El valor de contratar una agencia de marketing digital frente a hacerlo internamente radica en la especialización, la experiencia acumulada en múltiples proyectos y sectores, y el acceso a herramientas profesionales que de otra forma tendrían un coste prohibitivo. Una buena agencia de marketing digital no solo ejecuta acciones, sino que diseña una <a href="{r('/servicios/estrategia-digital/')}">estrategia digital</a> integral que alinea todos los canales hacia los objetivos de negocio del cliente.</p>
<p>En el contexto actual, donde más del 90 por ciento de los procesos de compra empiezan con una búsqueda en Google, contar con una agencia de marketing digital competente no es un lujo: es una necesidad para cualquier empresa que quiera competir. Desde pymes locales que necesitan <a href="{r('/servicios/agencia-seo-local/')}">SEO local</a> hasta <a href="{r('/marketing-para-ecommerce/')}">tiendas online</a> que buscan escalar sus ventas, el marketing digital es el motor de crecimiento más potente y medible que existe.</p>
<p>Comunikoo es una agencia de marketing digital en Barcelona con más de 487 proyectos completados, un 98 por ciento de satisfacción y un enfoque radical en resultados medibles. Trabajamos sin permanencia, con dashboard en tiempo real y un equipo senior que conoce tu sector. Si buscas una <strong>agencia de marketing digital</strong> que hable el idioma de tu negocio y no solo de métricas, <a href="{r('/contacto/')}">contacta con nosotros</a>.</p>
</div>
</div>
</section>

<!-- FAQ -->
<section class="py-28 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="max-w-4xl mx-auto">
<h2 class="font-headline font-extrabold text-4xl md:text-5xl text-primary mb-12 text-center">Preguntas Frecuentes sobre Marketing Digital</h2>
{faq_section_html}
</div>
</section>

<!-- CTA FINAL — Full conversion block -->
<section class="bg-primary py-24 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<p class="text-secondary-container font-bold text-sm uppercase tracking-widest mb-4">Da el primer paso</p>
<h2 class="font-headline font-extrabold text-3xl md:text-4xl text-white mb-4">Tu auditoría gratuita incluye:</h2>
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-w-xl mx-auto mb-8 text-left">
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container font-bold">✓</span> Análisis SEO completo de tu web</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container font-bold">✓</span> Estudio de tu competencia</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container font-bold">✓</span> Oportunidades de mejora con impacto</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container font-bold">✓</span> Plan de acción personalizado</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container font-bold">✓</span> Estimación de resultados a 6 meses</p>
<p class="text-on-primary-container text-sm flex items-start gap-2"><span class="text-secondary-container font-bold">✓</span> Sin compromiso ni permanencia</p>
</div>
<a class="inline-block bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">Solicitar auditoría gratuita →</a>
<p class="text-on-primary-container/50 text-xs mt-4">Respuesta en menos de 24 horas. Sin llamadas no deseadas.</p>
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''

    return head_html(
        "Agencia de Marketing Digital Barcelona | SEO, Diseño Web y Google Ads — Comunikoo",
        "Agencia de marketing digital en Barcelona. Expertos en SEO, diseño web, Google Ads y redes sociales. Resultados reales. Sin permanencia. Auditoría gratuita.",
        "/", schema
    ) + '\n' + body


# ============================================================
# STATIC PAGES
# ============================================================
def build_contact_page():
    current_url = "/contacto/"
    r = lambda target: rel(target, current_url)
    schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Organization","name":"Comunikoo","url":"https://comunikoo.es","address":{"@type":"PostalAddress","streetAddress":"Aragó 4","addressLocality":"Barcelona","postalCode":"08015","addressCountry":"ES"},"telephone":"+34608721015","email":"hola@comunikoo.es"}
</script>'''
    body = '''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20">
<section class="py-24 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="bg-surface-container-lowest rounded-3xl overflow-hidden grid grid-cols-1 lg:grid-cols-2 shadow-2xl shadow-primary/5">
<div class="p-10 md:p-16">
<h1 class="font-headline font-extrabold text-4xl text-primary mb-2">Contacta con nosotros</h1>
<p class="text-on-surface-variant mb-8">Cuéntanos tu proyecto. Te respondemos en menos de 24h.</p>
<form class="space-y-5">
<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
<div class="space-y-2">
<label class="text-sm font-bold text-primary uppercase tracking-wider">Nombre</label>
<input class="w-full bg-surface-container-low border-none rounded-lg px-5 py-3.5 focus:ring-2 focus:ring-secondary-container" placeholder="Tu nombre" type="text">
</div>
<div class="space-y-2">
<label class="text-sm font-bold text-primary uppercase tracking-wider">Email</label>
<input class="w-full bg-surface-container-low border-none rounded-lg px-5 py-3.5 focus:ring-2 focus:ring-secondary-container" placeholder="tu@email.com" type="email">
</div>
</div>
<div class="space-y-2">
<label class="text-sm font-bold text-primary uppercase tracking-wider">Teléfono</label>
<input class="w-full bg-surface-container-low border-none rounded-lg px-5 py-3.5 focus:ring-2 focus:ring-secondary-container" placeholder="+34 600 000 000" type="tel">
</div>
<div class="space-y-2">
<label class="text-sm font-bold text-primary uppercase tracking-wider">Mensaje</label>
<textarea class="w-full bg-surface-container-low border-none rounded-lg px-5 py-3.5 focus:ring-2 focus:ring-secondary-container" placeholder="Cuéntanos sobre tu proyecto..." rows="5"></textarea>
</div>
<button class="w-full bg-secondary-container text-on-secondary-container font-bold py-4 rounded-lg hover:bg-secondary transition-all active:scale-95 text-lg" type="submit">Enviar mensaje</button>
</form>
</div>
<div class="bg-primary p-10 md:p-16 text-white flex flex-col justify-between">
<div class="space-y-10">
<div>
<h3 class="font-headline font-bold text-2xl mb-4 flex items-center gap-3">
<span class="material-symbols-outlined text-secondary-container">location_on</span> Oficina Barcelona
</h3>
<p class="text-on-primary-container text-lg leading-relaxed">Barcelona, España</p>
</div>
<div class="space-y-3">
<p class="flex items-center gap-4 text-on-primary-container"><span class="material-symbols-outlined">mail</span> <a href="mailto:hola@comunikoo.es" class="hover:text-white">hola@comunikoo.es</a></p>
<p class="flex items-center gap-4 text-on-primary-container"><span class="material-symbols-outlined">schedule</span> Lunes a Viernes, 9:00 - 20:00</p>
</div>
</div>
</div>
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''
    return head_html("Contacto | Comunikoo — Agencia de Marketing Digital Barcelona", "Contacta con Comunikoo. Agencia de marketing digital en Barcelona. Te respondemos en menos de 24h.", "/contacto/", schema) + '\n' + body


def build_services_index():
    current_url = "/servicios/"
    r = lambda target: rel(target, current_url)

    services_list = [
        ("Agencia SEO", "Posicionamiento web orgánico", "/servicios/agencia-seo/"),
        ("SEO Local", "Google Maps y pack local", "/servicios/agencia-seo-local/"),
        ("Consultoría SEO", "Asesoramiento estratégico", "/servicios/consultoria-seo/"),
        ("Auditoría SEO", "Diagnóstico completo", "/servicios/auditoria-seo/"),
        ("Posicionamiento Web", "Primeras posiciones", "/servicios/posicionamiento-web/"),
        ("Linkbuilding", "Backlinks de calidad", "/servicios/linkbuilding/"),
        ("Diseño Web", "Webs profesionales", "/servicios/diseno-web/"),
        ("Diseño WordPress", "WordPress a medida", "/servicios/diseno-web-wordpress/"),
        ("Tiendas Online", "Ecommerce que vende", "/servicios/tienda-online/"),
        ("Desarrollo Web", "Programación a medida", "/servicios/desarrollo-web/"),
        ("Landing Pages", "Páginas de conversión", "/servicios/landing-pages/"),
        ("Mantenimiento Web", "Soporte técnico", "/servicios/mantenimiento-web/"),
        ("Google Ads", "Campañas rentables", "/servicios/agencia-google-ads/"),
        ("Facebook Ads", "Publicidad en Facebook", "/servicios/agencia-facebook-ads/"),
        ("Meta Ads", "Ecosistema Meta completo", "/servicios/agencia-meta-ads/"),
        ("Instagram Ads", "Publicidad visual", "/servicios/instagram-ads/"),
        ("Community Manager", "Gestión de redes", "/servicios/community-manager/"),
        ("Email Marketing", "El canal con más ROI", "/servicios/email-marketing/"),
        ("Branding", "Identidad de marca", "/servicios/branding/"),
        ("CRO", "Optimización conversión", "/servicios/optimizacion-cro/"),
    ]

    cards = ''
    for n, d, u in services_list:
        cards += f'''<a href="{r(u)}" class="bg-white p-8 rounded-xl shadow-[0_2px_12px_rgba(0,0,0,.07)] border border-black/[.06] hover:bg-primary hover:border-primary group transition-all duration-500 no-underline">
<h3 class="font-headline font-bold text-lg text-primary group-hover:text-white mb-2">{n}</h3>
<p class="text-sm text-on-surface-variant group-hover:text-white/80">{d}</p>
</a>\n'''

    body = '''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20">
<section class="py-24 px-6 lg:px-8 max-w-7xl mx-auto text-center">
<h1 class="font-headline font-extrabold text-5xl md:text-6xl text-primary mb-6">Nuestros Servicios</h1>
<p class="text-lg text-on-surface-variant max-w-2xl mx-auto">Todo lo que tu negocio necesita para dominar el mundo digital. Sin permanencia. Con resultados.</p>
</section>
<section class="pb-24 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{cards}
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''
    return head_html("Servicios de Marketing Digital | Comunikoo", "Todos los servicios de marketing digital de Comunikoo: SEO, diseño web, Google Ads, redes sociales, ecommerce y más.", "/servicios/") + '\n' + body


def build_blog_index():
    current_url = "/blog/"
    r = lambda target: rel(target, current_url)

    # Placeholder articles — to be replaced with real content later
    articles = [
        ("Guía Completa de SEO para Pymes en 2026", "Todo lo que necesita saber una pequeña empresa para posicionar en Google este año. Desde la auditoría inicial hasta la estrategia de contenidos.", "seo", "Próximamente"),
        ("Google Ads vs SEO: ¿Dónde Invertir Tu Presupuesto?", "Analizamos cuándo conviene invertir en publicidad de pago y cuándo en posicionamiento orgánico. Con datos reales de nuestros clientes.", "estrategia", "Próximamente"),
        ("Cómo Elegir la Mejor Agencia de Marketing Digital", "Los 10 criterios que debes evaluar antes de contratar una agencia. Evita errores costosos y elige un partner que genere resultados.", "negocio", "Próximamente"),
        ("SEO Local: Cómo Aparecer en Google Maps", "Guía paso a paso para posicionar tu negocio local en el pack de mapas de Google. Optimización de Google Business Profile incluida.", "seo-local", "Próximamente"),
        ("Diseño Web que Convierte: 15 Principios de CRO", "Las claves de diseño web orientado a conversión que aplicamos en nuestros proyectos. Con ejemplos reales antes y después.", "diseno", "Próximamente"),
        ("Email Marketing para Ecommerce: Automatizaciones que Venden", "Las 7 automatizaciones de email que toda tienda online debería tener activas. Recuperación de carrito, post-compra y más.", "ecommerce", "Próximamente"),
    ]

    CATS = {'seo': 'SEO', 'estrategia': 'Estrategia', 'negocio': 'Negocio', 'seo-local': 'SEO Local', 'diseno': 'Diseño Web', 'ecommerce': 'Ecommerce'}

    cards = ''
    for title, desc, cat, status in articles:
        cat_label = CATS.get(cat, cat.title())
        cards += f'''<div class="svc-card" style="text-align:left;padding:2rem">
<span style="display:inline-block;padding:.25rem .75rem;border-radius:50px;background:#f0f4ff;color:#001e40;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:1rem">{cat_label}</span>
<h3 style="font-size:1.1rem;margin-bottom:.5rem">{title}</h3>
<p style="font-size:.85rem;line-height:1.7">{desc}</p>
<p style="font-size:.75rem;color:#fd8b00;font-weight:700;margin-top:1rem">{status}</p>
</div>\n'''

    body = '''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20">

<section class="py-24 px-6 lg:px-8 max-w-7xl mx-auto text-center">
<h1 class="font-headline font-extrabold text-4xl md:text-5xl lg:text-6xl text-primary mb-6">Blog de Marketing Digital</h1>
<p class="text-lg text-on-surface-variant max-w-2xl mx-auto">Artículos, guías y recursos sobre SEO, Google Ads, diseño web, redes sociales y estrategia digital. Escrito por profesionales con experiencia real.</p>
</section>

<section class="pb-24 px-6 lg:px-8 max-w-7xl mx-auto">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
{cards}
</div>
</section>

<!-- CTA -->
<section class="bg-primary py-20 px-6 lg:px-8">
<div class="max-w-3xl mx-auto text-center">
<h2 class="font-headline font-extrabold text-2xl md:text-3xl text-white mb-4">¿Quieres que apliquemos estas estrategias en tu negocio?</h2>
<p class="text-on-primary-container text-base mb-8">Solicita tu auditoría gratuita y te mostramos qué podemos hacer por ti.</p>
<a class="inline-block bg-secondary-container text-on-secondary-container px-10 py-4 rounded-lg font-bold text-lg hover:bg-secondary transition-all active:scale-95" href="{r('/contacto/')}">Auditoría gratuita</a>
</div>
</section>

<!-- SERVICIOS -->
<section class="py-16 px-6 lg:px-8 bg-[#f4f6fa]">
<div class="max-w-5xl mx-auto text-center">
<h2 class="font-headline font-bold text-xl text-primary mb-8">Nuestros servicios de marketing digital</h2>
<div class="flex flex-wrap justify-center gap-3">
<a href="{r('/servicios/agencia-seo/')}" class="px-4 py-2 rounded-full bg-white border border-black/[.06] shadow-[0_1px_4px_rgba(0,0,0,.05)] text-xs font-bold text-primary hover:bg-primary hover:text-white transition-all no-underline">SEO</a>
<a href="{r('/servicios/diseno-web/')}" class="px-4 py-2 rounded-full bg-white border border-black/[.06] shadow-[0_1px_4px_rgba(0,0,0,.05)] text-xs font-bold text-primary hover:bg-primary hover:text-white transition-all no-underline">Diseño Web</a>
<a href="{r('/servicios/agencia-google-ads/')}" class="px-4 py-2 rounded-full bg-white border border-black/[.06] shadow-[0_1px_4px_rgba(0,0,0,.05)] text-xs font-bold text-primary hover:bg-primary hover:text-white transition-all no-underline">Google Ads</a>
<a href="{r('/servicios/community-manager/')}" class="px-4 py-2 rounded-full bg-white border border-black/[.06] shadow-[0_1px_4px_rgba(0,0,0,.05)] text-xs font-bold text-primary hover:bg-primary hover:text-white transition-all no-underline">Redes Sociales</a>
<a href="{r('/servicios/tienda-online/')}" class="px-4 py-2 rounded-full bg-white border border-black/[.06] shadow-[0_1px_4px_rgba(0,0,0,.05)] text-xs font-bold text-primary hover:bg-primary hover:text-white transition-all no-underline">Tiendas Online</a>
<a href="{r('/servicios/email-marketing/')}" class="px-4 py-2 rounded-full bg-white border border-black/[.06] shadow-[0_1px_4px_rgba(0,0,0,.05)] text-xs font-bold text-primary hover:bg-primary hover:text-white transition-all no-underline">Email Marketing</a>
</div>
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''
    return head_html("Blog de Marketing Digital | Comunikoo", "Artículos, guías y recursos sobre SEO, Google Ads, diseño web y estrategia digital. Escrito por profesionales.", "/blog/") + '\n' + body


def build_simple_page(title, meta_desc, url, h1, content_html_str):
    current_url = url
    body = '''<body class="bg-surface font-body text-on-background">
''' + nav_html(current_url) + f'''
<main class="pt-20">
<section class="py-24 px-6 lg:px-8 max-w-3xl mx-auto">
<h1 class="font-headline font-extrabold text-4xl text-primary mb-8">{h1}</h1>
<div class="prose prose-lg max-w-none text-on-surface-variant leading-relaxed [&_h2]:font-headline [&_h2]:font-bold [&_h2]:text-2xl [&_h2]:text-primary [&_h2]:mt-10 [&_h2]:mb-4 [&_h3]:font-headline [&_h3]:font-bold [&_h3]:text-xl [&_h3]:text-primary [&_h3]:mt-8 [&_h3]:mb-3 [&_p]:mb-4 [&_ul]:space-y-2 [&_li]:text-on-surface-variant [&_strong]:text-on-surface">
{content_html_str}
</div>
</section>
</main>
''' + footer_html(current_url) + '''
</body></html>'''
    return head_html(title, meta_desc, url) + '\n' + body


# ============================================================
# MAIN GENERATOR
# ============================================================
import re as _re

def _replace_material_icons(html):
    """Replace <span class="material-symbols-outlined...">icon_name</span> with inline SVG."""
    def _repl(m):
        attrs = m.group(1)
        icon_name = m.group(2).strip()
        # Extract style/class info
        style_match = _re.search(r'style="([^"]*)"', attrs)
        style = style_match.group(1) if style_match else ''
        # Get size from font-size in style
        size = 24
        size_match = _re.search(r'font-size:\s*([\d.]+)rem', style)
        if size_match:
            size = int(float(size_match.group(1)) * 16)
        size_match2 = _re.search(r'text-(\d)xl', attrs)
        if size_match2:
            sizes = {'2': 24, '3': 30}
            size = sizes.get(size_match2.group(1), 24)
        svg = SVG_ICONS.get(icon_name, SVG_ICONS.get('star', ''))
        if size != 24:
            svg = svg.replace('width="24"', f'width="{size}"').replace('height="24"', f'height="{size}"')
        # Preserve color style
        color_style = ''
        color_match = _re.search(r'color:\s*([^;"]+)', style)
        if color_match:
            color_style = f' style="color:{color_match.group(1)}"'
        return f'<span class="icon-inline"{color_style}>{svg}</span>'
    return _re.sub(r'<span class="material-symbols-outlined([^"]*)"[^>]*>([^<]+)</span>', _repl, html)

def write_page(path, html):
    html = _replace_material_icons(html)
    # Replace CSS placeholder with correct relative path
    css_rel = rel('/css/style.css', path).replace('/index.html', '')
    if path == '/':
        css_rel = 'css/style.css'
    else:
        depth = len([p for p in path.strip('/').split('/') if p])
        css_rel = '../' * depth + 'css/style.css'
    html = html.replace('CSSPLACEHOLDER', css_rel)
    out = OUTPUT_DIR / path.strip('/') / 'index.html' if path != '/' else OUTPUT_DIR / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f"  ✓ {path}")


def main():
    print("COMUNIKOO — Generating site (Stitch Design)...\n")

    # Load content from modules
    content_pages, verticals, profiles, subpages = load_content_pages()
    print(f"  Loaded {len(content_pages)} service content modules")
    print(f"  Loaded {len(verticals)} vertical pages")
    print(f"  Loaded {len(profiles)} profile pages")
    print(f"  Loaded {len(subpages)} sub-pages\n")

    # Import ALL_PAGES from old generate.py data
    # We'll use the content modules + fallback to inline data
    from generate import ALL_PAGES as OLD_PAGES

    count = 0

    # HOME
    write_page('/', build_home())
    count += 1

    # SERVICES INDEX
    write_page('/servicios/', build_services_index())
    count += 1

    # CONTACT
    write_page('/contacto/', build_contact_page())
    count += 1

    # BLOG
    write_page('/blog/', build_blog_index())
    count += 1

    # GROUP SUB-PAGES by parent FIRST (before generating anything)
    subpages_by_parent = {}
    for url, sp in subpages.items():
        parent = sp.get('parent', '')
        if parent not in subpages_by_parent:
            subpages_by_parent[parent] = []
        subpages_by_parent[parent].append((url, sp))

    # SERVICE PAGES (inject sub-page links into parent pages)
    processed_urls = set()
    for url, page_data in content_pages.items():
        # If this service has sub-pages, inject them
        if url in subpages_by_parent:
            page_data['_subpages'] = [(u, s['h1_short']) for u, s in subpages_by_parent[url]]
        write_page(url, build_service_page(page_data))
        processed_urls.add(url)
        count += 1

    # SUB-PAGES
    for url, page_data in subpages.items():
        if url not in processed_urls:
            page_data['url'] = url
            parent = page_data.get('parent', '')
            siblings = [(u, s['h1_short']) for u, s in subpages_by_parent.get(parent, []) if u != url]
            page_data['siblings'] = siblings
            page_data['_is_subpage'] = True
            write_page(url, build_service_page(page_data))
            processed_urls.add(url)
            count += 1

    # PROFILE PAGES (from perfiles_profesionales.py)
    for url, page_data in profiles.items():
        if url not in processed_urls:
            write_page(url, build_service_page(page_data))
            processed_urls.add(url)
            count += 1

    # VERTICAL PAGES (from verticales.py)
    for url, page_data in verticals.items():
        if url not in processed_urls:
            page_data['url'] = url  # ensure url is set
            write_page(url, build_vertical_page(page_data))
            processed_urls.add(url)
            count += 1

    # ALL remaining pages from old generate data
    for page in OLD_PAGES:
        url = page['url']
        if url in processed_urls:
            continue
        if page.get('type') == 'vertical':
            write_page(url, build_vertical_page(page))
        elif page.get('type') == 'geo':
            write_page(url, build_geo_page(page))
        else:
            write_page(url, build_service_page(page))
        processed_urls.add(url)
        count += 1

    # STATIC PAGES
    for title, meta, url, h1, content in [
        ("Nosotros | Comunikoo", "Conoce al equipo de Comunikoo. Agencia de marketing digital en Barcelona.", "/nosotros/", "Sobre Comunikoo", "<p>Somos una agencia de marketing digital con sede en Barcelona. Más de 487 proyectos completados y un 98% de clientes satisfechos nos avalan.</p><h2>Nuestra misión</h2><p>Ayudar a negocios a crecer de forma sostenible a través del marketing digital basado en datos y resultados medibles.</p><h2>Nuestros valores</h2><p><strong>Transparencia:</strong> Dashboard en tiempo real, sin contratos de permanencia.</p><p><strong>Resultados:</strong> Medimos éxito en leads, ventas y facturación.</p><p><strong>Especialización:</strong> Equipo senior con +5 años de experiencia cada uno.</p>"),
        ("Política de Privacidad | Comunikoo", "Política de privacidad de Comunikoo.", "/politica-de-privacidad/", "Política de Privacidad", "<p>En cumplimiento del Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica 3/2018 de Protección de Datos Personales, le informamos sobre el tratamiento de sus datos personales.</p><h2>Responsable del tratamiento</h2><p>Comunikoo · Aragó 4, Barcelona 08015 · hola@comunikoo.es</p><h2>Finalidad</h2><p>Gestión de consultas, presupuestos y prestación de servicios de marketing digital.</p><h2>Derechos</h2><p>Puede ejercer sus derechos de acceso, rectificación, supresión, portabilidad, limitación y oposición enviando un email a hola@comunikoo.es.</p>"),
        ("Aviso Legal | Comunikoo", "Aviso legal de Comunikoo.", "/aviso-legal/", "Aviso Legal", "<p>En cumplimiento de la Ley 34/2002 de Servicios de la Sociedad de la Información y Comercio Electrónico (LSSI).</p><h2>Datos identificativos</h2><p>Comunikoo · Aragó 4, Barcelona 08015 · hola@comunikoo.es · +34 608 721 015</p><h2>Propiedad intelectual</h2><p>Todos los contenidos de este sitio web son propiedad de Comunikoo y están protegidos por las leyes de propiedad intelectual e industrial.</p>"),
        ("Política de Cookies | Comunikoo", "Política de cookies de Comunikoo.", "/politica-de-cookies/", "Política de Cookies", "<p>Este sitio web utiliza cookies propias y de terceros para mejorar la experiencia de navegación y ofrecer contenidos de interés.</p><h2>¿Qué son las cookies?</h2><p>Las cookies son pequeños archivos de texto que se almacenan en su dispositivo al visitar un sitio web.</p><h2>Tipos de cookies que usamos</h2><p><strong>Cookies técnicas:</strong> necesarias para el funcionamiento del sitio.</p><p><strong>Cookies analíticas:</strong> nos ayudan a entender cómo interactúan los usuarios con el sitio (Google Analytics).</p>"),
    ]:
        if url not in processed_urls:
            write_page(url, build_simple_page(title, meta, url, h1, content))
            count += 1

    print(f"\n✅ Generated {count} pages total")


if __name__ == '__main__':
    main()
