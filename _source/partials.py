# Shared snippets used to generate the static pages once.
import pathlib
SCR = pathlib.Path(__file__).resolve().parent
# Changes whenever styles.css or script.js change, so phones don't keep an old cached copy
import hashlib
ASSET_V = hashlib.md5(b''.join((SCR.parent / f).read_bytes() for f in ('styles.css', 'script.js'))).hexdigest()[:8]
def mark(root, lazy=False, alt=''):
    lz = ' loading="lazy"' if lazy else ''
    return (f'<img class="logo__mark" src="{root}assets/logo-mark-88.webp" srcset="{root}assets/logo-mark-176.webp 2x, {root}assets/logo-mark-264.webp 3x" '
            f'width="149" height="88" alt="{alt}"{lz} decoding="async">')
def mark_anim(root, cls='logo__mark', lazy=False, label='', big=False):
    # Logo in three layers so the ring can draw itself around the letters (script.js plays it)
    lz = ' loading="lazy"' if lazy else ''
    def layer(n):
        if big:  # large logo (About photo): pick by width so phones get a sharp copy
            src = (f'src="{root}assets/logo-{n}-264.webp" srcset="{root}assets/logo-{n}-264.webp 447w, {root}assets/logo-{n}-528.webp 894w, '
                   f'{root}assets/logo-{n}-792.webp 1340w" sizes="(min-width: 900px) 300px, 80vw"')
        else:
            src = f'src="{root}assets/logo-{n}-88.webp" srcset="{root}assets/logo-{n}-176.webp 2x, {root}assets/logo-{n}-264.webp 3x"'
        return f'<img class="logo__layer logo__layer--{n}" {src} width="149" height="88" alt=""{lz} decoding="async">'
    aria = f' role="img" aria-label="{label}"' if label else ''
    return f'<span class="{cls} logo__mark--anim"{aria}>{layer("back")}{layer("mdv")}{layer("front")}{layer("star1")}{layer("star2")}</span>'
SKY = (SCR / 'skyline.txt').read_text().strip()
SKY2 = (SCR / 'skyline2.svg').read_text().strip()
BAY_MAP = (SCR / 'bay-map.svg').read_text().strip()
SF_SKY = '\n'.join(l for l in (SCR / 'sf-skyline.svg').read_text().splitlines() if not l.strip().startswith('<!--'))

def icon(name, cls=''):
    paths = {
        'arrow-right': '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
        'arrow-left': '<path d="M19 12H5"/><path d="m11 18-6-6 6-6"/>',
        'menu': '<path d="M4 9h16"/><path d="M4 15h16"/>',
        'close': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
        'phone': '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
        'smartphone': '<rect x="5" y="2" width="14" height="20" rx="2.5"/><path d="M12 18h.01"/>',
        'zap': '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
        'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        'split': '<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M12 3v18"/><path d="m8 10-2 2 2 2"/><path d="m16 10 2 2-2 2"/>',
        'pin': '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
        'search': '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
        'mail': '<rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="m22 7-10 6L2 7"/>',
        'check': '<path d="M20 6 9 17l-5-5"/>',
        'grip': '<path d="m9 7-5 5 5 5"/><path d="m15 7 5 5-5 5"/>',
        'store': '<path d="M3 9l1.5-5h15L21 9"/><path d="M4 9v11h16V9"/><path d="M9.5 20v-6h5v6"/>',
        'sparkle': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
        'form': '<rect x="4" y="3" width="16" height="18" rx="2.5"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    }
    c = f' class="{cls}"' if cls else ''
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{paths[name]}</svg>')

NAV = [('work', 'Work'), ('benefits', 'What you get'), ('process', 'Process'), ('about', 'About'), ('contact', 'Contact')]

def head(root, title, desc, path, extra_fonts='', preload=''):
    url = 'https://mdvwebdesign.com/' + path
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- SITE_URL: https://mdvwebdesign.com  (swap this domain here, in sitemap.xml and robots.txt when the domain changes) -->
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#F3F7FD">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="MDV Web Design">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://mdvwebdesign.com/assets/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="MDV Web Design: websites for local businesses in the Bay Area">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="https://mdvwebdesign.com/assets/og.png">
  <link rel="icon" href="{root}favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Racing+Sans+One&family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600&family=Caveat:wght@700&family=Instrument+Serif:ital@1&display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Racing+Sans+One&family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600&family=Caveat:wght@700&family=Instrument+Serif:ital@1&display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Racing+Sans+One&family=Inter+Tight:wght@700;800&family=Inter:wght@400;500;600&family=Caveat:wght@700&family=Instrument+Serif:ital@1&display=swap"></noscript>{extra_fonts}{preload}
  <link rel="stylesheet" href="{root}styles.css?v={ASSET_V}">
  <script>document.documentElement.classList.add('js');</script>'''

def header(root, home=True):
    base = '' if home else f'{root}index.html'
    links = '\n'.join(f'        <li><a href="{base}#{i}">{t}</a></li>' for i, t in NAV)
    return f'''  <a class="skip-link" href="#main">Skip to content</a>
  <div class="frame">
    <header class="site-header" id="top">
      <a class="logo" href="{root}index.html" aria-label="MDV Web Design, home">{mark_anim(root)}<span class="logo__text" aria-hidden="true"><span class="logo__name">MDV Web Design</span><span class="logo__tag">Bay Area Websites</span></span></a>
      <nav class="site-nav" aria-label="Main">
        <ul role="list">
{links}
        </ul>
      </nav>
      <div class="header-actions">
        <a class="btn btn--dark btn--sm" href="{base}#contact">Free concept</a>
        <button class="btn btn--light btn--sm menu-toggle" type="button" aria-expanded="false" aria-controls="menu">Menu {icon('menu')}</button>
      </div>
    </header>'''

def menu(root, home=True):
    base = '' if home else f'{root}index.html'
    links = '\n'.join(f'        <li><a href="{base}#{i}"><small>0{n+1}</small>{t}</a></li>' for n, (i, t) in enumerate(NAV))
    return f'''  <div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="menu__top">
      {mark_anim(root, label='MDV Web Design')}
      <button class="btn btn--ghost-dark btn--sm menu-close" type="button">Close {icon('close')}</button>
    </div>
    <nav class="menu__nav" aria-label="Menu">
      <ul role="list">
{links}
      </ul>
    </nav>
    <div class="menu__foot">
      <a class="btn btn--lime" href="{base}#contact">Get my free concept {icon('arrow-right')}</a>
      <a class="mail" href="mailto:markdv.webdesign@gmail.com">markdv.webdesign@gmail.com</a>
    </div>
  </div>'''

def footer(root):
    return f'''    <footer class="site-footer tone-dark">
      <div class="container">
        <div class="site-footer__skyline" aria-hidden="true">{SKY2}</div>
        <div class="site-footer__row">
          <a class="logo" href="{root}index.html" aria-label="MDV Web Design, home">{mark_anim(root, lazy=True)}</a>
          <p class="site-footer__tag">Websites for local businesses, all around the Bay.</p>
          <a class="site-footer__mail" href="mailto:markdv.webdesign@gmail.com">markdv.webdesign@gmail.com</a>
        </div>
        <div class="site-footer__bottom">
          <p>&copy; <span data-year>2026</span> MDV Web Design</p>
          <p>Hayward, CA &middot; Serving the whole Bay Area</p>
        </div>
      </div>
    </footer>
  </div>'''

def tail(root):
    return f'''  <script src="{root}script.js?v={ASSET_V}" defer></script>
</body>
</html>
'''

def compare(before_src, before_srcset, after_src, after_srcset, w, h, before_alt, after_alt, label, sizes, cid, eager=False):
    lz = '' if eager else ' loading="lazy"'
    return f'''<div class="compare" data-compare style="--pos:50%">
  <img class="compare__after" src="{after_src}" srcset="{after_srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{after_alt}"{lz} decoding="async">
  <img class="compare__before" src="{before_src}" srcset="{before_srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{before_alt}"{lz} decoding="async">
  <span class="compare__line" aria-hidden="true"></span>
  <span class="compare__handle" aria-hidden="true">{icon('grip')}</span>
  <span class="compare__tag compare__tag--before" aria-hidden="true">Before</span>
  <span class="compare__tag compare__tag--after" aria-hidden="true">After</span>
  <label class="sr-only" for="{cid}">{label}. Use the arrow keys to move between Before and After.</label>
  <input class="compare__range" id="{cid}" type="range" min="0" max="100" value="50" step="1">
</div>'''
