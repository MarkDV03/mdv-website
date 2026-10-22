import html
import os
import sys, json
from partials import *

OUT = sys.argv[1]
# Set to True once the businesses give permission to show their case studies.
SHOW_WORK = len(sys.argv) > 2 and sys.argv[2] == 'full'
# Christina's real site. The Work section shows it live, so it updates whenever her site does.
CHRISTINA_URL = os.environ.get('CHRISTINA_URL', 'https://markdv03.github.io/Christinas-salon/')
# Same-origin copy of Christina's site for the scrolling previews (the tour can only drive a page on this domain)
CHRISTINA_PREVIEW = os.environ.get('CHRISTINA_PREVIEW', 'live/christinas-salon/')
I = 'assets/img/work/'

import os, re
def doodle(name, cls=''):
    svg = open(os.path.join(OUT, 'assets', 'doodles', name + '.svg')).read().strip()
    svg = re.sub(r'<metadata>.*?</metadata>\s*', '', svg, flags=re.S).replace(' xmlns:c2pa="http://c2pa.org/manifest"', '')  # drop embedded file credentials, they only bloat the page
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg" ', '').replace('#2F5FD0', 'currentColor')
    return svg.replace('<svg ', f'<svg class="doodle doodle--{name} {cls}" aria-hidden="true" focusable="false" ', 1)



SKY_LOADER_OLD = f'''  <div class="loader" aria-hidden="true">
    <svg viewBox="0 0 1200 180" focusable="false"><path pathLength="1" d="{SKY}"/></svg>
    <p class="loader__text">Loading...</p>
  </div>'''

LOADER_SCRIPT_OLD = '''
  <script>(function(){try{if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&!sessionStorage.getItem('mdv-loader')){document.documentElement.classList.add('show-loader');sessionStorage.setItem('mdv-loader','1');}}catch(e){}})();</script>'''

SKY_LOADER = ''
LOADER_SCRIPT = ''

SCHEMA = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "MDV Web Design",
    "description": "Modern, mobile-friendly websites for Bay Area businesses, based in Hayward. Free concept redesigns.",
    "url": "https://mdvwebdesign.com/",
    "email": "markdv.webdesign@gmail.com",
    "image": "https://mdvwebdesign.com/assets/og.png?v=3",
    "logo": "https://mdvwebdesign.com/assets/logo-mark-512.png",
    "founder": {"@type": "Person", "name": "Mark"},
    "address": {"@type": "PostalAddress", "addressLocality": "Hayward", "addressRegion": "CA", "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": c} for c in
                   ["Hayward", "San Francisco", "Oakland", "San Leandro", "San Lorenzo", "Castro Valley", "Union City", "Fremont", "Newark", "Dublin", "Pleasanton", "Livermore", "Milpitas", "San Jose", "Santa Clara", "Sunnyvale"]],
    "knowsAbout": ["Web design", "Website redesign", "Local SEO", "Mobile-friendly websites"],
}

FAQ_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in [('How much does a website cost?', 'Every business needs something a little different, so every project gets its own quote based on the pages and features you need. The concept is always free, so you see exactly what you would be getting before you spend anything.'), ('Is the free concept really free?', 'Yes. I design a new homepage for your business and send it to you. If you don&rsquo;t love it, you owe nothing and there are no hard feelings.'), ('How long does it take?', 'Most small business sites take about 2 to 4 weeks from the day you say yes to launch day. Having your photos and info ready speeds things up.'), ('I already have a website. Can you redesign it?', 'Absolutely. Most of my work is giving older sites a fresh look that works on phones. I can keep your domain, so customers still find you at the same address.'), ('Do I need to write the text or take photos?', 'No. I can write the words for you based on a quick chat, and use your own photos if you have them. Real photos of your work and your team always help the most.'), ('Will I own my website?', 'Yes. Once it&rsquo;s paid for, the site and the domain are yours. I&rsquo;m happy to stick around for updates, but you&rsquo;re never locked in.'), ('Are there any ongoing costs?', 'If you skip my monthly care plan, you pay the companies that keep your site online directly. Your domain name, like yourbusiness.com, renews every year and usually costs about $10 to $25 a year, depending on the name and the company. Some companies let you pay monthly instead. Hosting for a small site like this is often free, or a few dollars a month. None of that money goes to me. If you&rsquo;d rather not deal with it, my optional care plan covers hosting, monthly checkups and small updates for one monthly fee, and your domain always stays in your name.'), ('Can you help people find me on Google?', 'Every site I build is set up for Google from day one, with your services, hours and service area clearly listed. I can also help you set up or clean up your Google Business Profile.')]],
}

MAC_BAR = ('<div class="mac" aria-hidden="true"><div class="mac__menu"><span class="mac__apps"><b>Safari</b><i>File</i><i>Edit</i><i>View</i><i>History</i><i>Bookmarks</i></span>'
  '<span class="mac__tray"><svg viewBox="0 0 16 12" focusable="false"><path d="M1 4.2a10 10 0 0 1 14 0l-1.4 1.4a8 8 0 0 0-11.2 0zM3.8 7a6 6 0 0 1 8.4 0l-1.4 1.4a4 4 0 0 0-5.6 0zM8 11.6 6.4 10a2.3 2.3 0 0 1 3.2 0z" fill="currentColor"/></svg>'
  '<svg viewBox="0 0 26 12" focusable="false"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="currentColor" stroke-opacity=".5"/><rect x="2.5" y="2.5" width="15" height="7" rx="1.6" fill="currentColor"/><rect x="23.6" y="4" width="1.6" height="4" rx=".8" fill="currentColor" fill-opacity=".5"/></svg><i>Thu 9:41 AM</i></span></div>'
  '<div class="mac__safari"><span class="mac__lights"><i></i><i></i><i></i></span><span class="mac__nav">&lsaquo;&nbsp;&nbsp;&rsaquo;</span>'
  '<span class="mac__url"><svg viewBox="0 0 10 12" focusable="false"><path d="M2.5 5V3.6a2.5 2.5 0 0 1 5 0V5" fill="none" stroke="currentColor" stroke-width="1.3"/><rect x="1" y="5" width="8" height="6.4" rx="1.4" fill="currentColor"/></svg>URL</span><span class="mac__tools"><i>+</i></span></div></div>')

def laptop(src, srcset, sizes, alt, eager=False):
    attrs = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'''<div class="laptop">
  <div class="laptop__lid"><div class="laptop__display">{MAC_BAR.replace('URL', 'yourbusiness.com')}<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="1440" height="900" alt="{alt}"{attrs} decoding="async"></div></div>
  <div class="laptop__base" aria-hidden="true"></div>
</div>'''

def phone(src, srcset, sizes, alt, eager=False, cls=''):
    attrs = '' if eager else ' loading="lazy"'
    return f'''<div class="phone {cls}"><span class="phone__btn phone__btn--action" aria-hidden="true"></span><span class="phone__btn phone__btn--vol" aria-hidden="true"></span><span class="phone__btn phone__btn--vol2" aria-hidden="true"></span><span class="phone__btn phone__btn--power" aria-hidden="true"></span><span class="phone__btn phone__btn--cam" aria-hidden="true"></span><div class="phone__display"><span class="phone__status" aria-hidden="true"><b>9:41</b><svg viewBox="0 0 68 12" focusable="false"><g fill="currentColor"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0.5" width="3" height="11.5" rx="1"/><path d="M31 3.2a9.5 9.5 0 0 1 12.6 0l-1.5 1.6a7.3 7.3 0 0 0-9.6 0zM33.4 5.8a6 6 0 0 1 7.8 0l-1.5 1.6a3.8 3.8 0 0 0-4.8 0zM37.3 11.6 35.6 9.9a2.5 2.5 0 0 1 3.4 0z"/><rect x="48" y="0.5" width="17" height="11" rx="3.2" fill="none" stroke="currentColor" stroke-opacity=".4"/><rect x="50" y="2.5" width="12.5" height="7" rx="1.8"/><rect x="66" y="4" width="1.6" height="4" rx=".8" fill-opacity=".45"/></g></svg></span><img src="{src}" srcset="{srcset}" sizes="{sizes}" width="390" height="844" alt="{alt}"{attrs} decoding="async"></div></div>'''


ICO = dict(drain='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 4h16v4H4zM7 8v4a5 5 0 0 0 10 0V8M12 17v3M9 20h6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>', heat='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="6" y="3" width="12" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 9c-1.5 2-2 3-2 4a2 2 0 0 0 4 0c0-1-.5-2-2-4z" fill="currentColor"/></svg>', drop='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>', pipe='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M3 8h8a3 3 0 0 1 3 3v10M3 13h6v8M14 4h7M17.5 4v3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>', wrench='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-2 2-1.3-1.3-6.4 6.4a2 2 0 0 1-2.8-2.8l6.4-6.4L13.6 9.6l-1.3-1.3a4 4 0 0 1 2.4-2z" fill="currentColor"/></svg>', phone='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11 11 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.6 3.6a1 1 0 0 1-.25 1z" fill="currentColor"/></svg>')

MOCK_DESK = '''<div class="laptop">
  <div class="laptop__lid"><div class="laptop__display">MACBAR<div class="pl pl--desk" role="img" aria-label="Example local business website for a plumber in Hayward: a call button, Google rating, a callback form and a list of services">
    <div class="pl__util"><span>Licensed &amp; insured &middot; Family-run since 2009</span><span><i class="pl__dot"></i>Open now &middot; 24/7 emergencies</span></div>
    <div class="pl__nav"><span class="pl__logo"><span class="pl__mark">{w}</span><span>Your Business<small>Plumbing &amp; Drains</small></span></span><span class="pl__links"><i>Services</i><i>Reviews</i><i>Areas</i><i>About</i></span><span class="pl__call">{ph}(510) 555-0123</span></div>
    <div class="pl__hero">
      <div class="pl__copy">
        <p class="pl__eyebrow">Hayward &middot; Castro Valley &middot; San Leandro &middot; Union City</p>
        <b class="pl__h">Clogged drain? Leaky pipe? We&rsquo;re on the way.</b>
        <p class="pl__sub">Same-day service from a local crew. You get the price before we start, every time.</p>
        <span class="pl__btns"><em>Call now</em><em class="out">Get a free quote</em></span>
        <span class="pl__trust"><span class="pl__g">G</span><span><span class="pl__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 4.9 &middot; 212 Google reviews</span></span>
        <span class="pl__badges"><i>&#10003; Same-day service</i><i>&#10003; Upfront pricing</i><i>&#10003; Licensed &amp; insured</i></span>
      </div>
      <div class="pl__form"><span class="pl__review">&ldquo;Came out the same day and fixed our water heater. Fair price, super clean.&rdquo;<small>&#9733;&#9733;&#9733;&#9733;&#9733; &nbsp;Maria G., Hayward</small></span><b>Request a callback</b><small>We usually call back in 15 minutes.</small><i>Name</i><i>Phone</i><i class="sel">What&rsquo;s going on?</i><em>Call me back</em></div>
    </div>
    <div class="pl__svc"><span>{d}<b>Drain cleaning</b></span><span>{h}<b>Water heaters</b></span><span>{dr}<b>Leak repair</b></span><span>{p}<b>Repiping</b></span></div>
  </div></div></div>
  <div class="laptop__base" aria-hidden="true"></div>
</div>'''.format(w=ICO['wrench'], ph=ICO['phone'], d=ICO['drain'], h=ICO['heat'], dr=ICO['drop'], p=ICO['pipe'])

MOCK_PHONE = '''<div class="phone"><span class="phone__btn phone__btn--action" aria-hidden="true"></span><span class="phone__btn phone__btn--vol" aria-hidden="true"></span><span class="phone__btn phone__btn--vol2" aria-hidden="true"></span><span class="phone__btn phone__btn--power" aria-hidden="true"></span><span class="phone__btn phone__btn--cam" aria-hidden="true"></span><div class="phone__display">STATUS<div class="pl pl--phone" role="img" aria-label="The same plumber website on a phone, with a big tap to call bar at the bottom">
    <div class="pl__util"><span><i class="pl__dot"></i>Open now &middot; 24/7</span></div>
    <div class="pl__nav"><span class="pl__logo"><span class="pl__mark">{w}</span><span>Your Business<small>Plumbing &amp; Drains</small></span></span><span class="pl__burger"></span></div>
    <div class="pl__copy">
      <p class="pl__eyebrow">Hayward &amp; the East Bay</p>
      <b class="pl__h">Clogged drain? Leaky pipe? We&rsquo;re on the way.</b>
      <span class="pl__trust"><span class="pl__g">G</span><span><span class="pl__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 4.9 &middot; 212 reviews</span></span>
    </div>
    <div class="pl__svc"><span>{d}<b>Drain cleaning</b></span><span>{h}<b>Water heaters</b></span><span>{dr}<b>Leak repair</b></span><span>{p}<b>Repiping</b></span></div>
    <div class="pl__quote">&ldquo;Came out the same day and fixed our water heater. Fair price.&rdquo;<small><span class="pl__stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> Maria G., Hayward</small></div>
    <div class="pl__bar"><em>{ph}Call (510) 555-0123</em></div>
  </div></div></div>'''.format(w=ICO['wrench'], ph=ICO['phone'], d=ICO['drain'], h=ICO['heat'], dr=ICO['drop'], p=ICO['pipe'])

def page_index(root=''):
    r = root
    status = phone('x','x','x','x').split('<div class="phone__display">')[1].split('<img')[0]
    mock_phone = MOCK_PHONE.replace('STATUS', status)
    mock_desk = MOCK_DESK.replace('MACBAR', MAC_BAR.replace('URL', 'yourbusiness.com'))
    carr_lap = laptop(f'{I}carrillo-desktop.webp', f'{I}carrillo-desktop-960.webp 960w, {I}carrillo-desktop.webp 1440w, {I}carrillo-desktop-2x.webp 2880w',
                      '(min-width: 1100px) 900px, 84vw', 'J. Carrillo Plumbing concept redesign on a laptop, with the headline Drains cleared, pipes fixed and a call button', eager=True)
    chr_phone = phone(f'{I}christina-mobile.webp', f'{I}christina-mobile-390.webp 390w, {I}christina-mobile.webp 780w, {I}christina-mobile-3x.webp 1170w',
                      '(min-width: 768px) 220px, 34vw', "Christina's Hair Salon concept redesign on a phone", eager=True)
    compare_home = compare(f'{I}christina-old-compare.webp', f'{I}christina-old-compare-720.webp 720w, {I}christina-old-compare.webp 1440w, {I}christina-old-compare-2x.webp 1893w',
                           f'{I}christina-new-compare.webp', f'{I}christina-new-compare-720.webp 720w, {I}christina-new-compare.webp 1440w, {I}christina-new-compare-2x.webp 2880w',
                           1440, 704, "Before: Christina's Hair Salon's old website, a plain page of small text under a photo banner",
                           "After: the MDV concept redesign with a bold salon name, a stylist photo and a call to book button",
                           "Compare Christina's Hair Salon's old website with the redesign", '(min-width: 900px) 640px, 90vw', 'compare-home')
    carr_lap2 = laptop(f'{I}carrillo-desktop.webp', f'{I}carrillo-desktop-960.webp 960w, {I}carrillo-desktop.webp 1440w, {I}carrillo-desktop-2x.webp 2880w',
                       '(min-width: 900px) 600px, 80vw', 'J. Carrillo Plumbing concept redesign, desktop view')
    carr_phone = phone(f'{I}carrillo-mobile.webp', f'{I}carrillo-mobile-390.webp 390w, {I}carrillo-mobile.webp 780w, {I}carrillo-mobile-3x.webp 1170w',
                       '(min-width: 900px) 170px, 24vw', 'J. Carrillo Plumbing concept redesign, phone view with a tap to call button')

    benefits = [
        ('Built for phones first', 'Most people will find you on their phone, so that&rsquo;s where I start.'),
        ('Quick to load', 'No heavy extras. It opens fast, even on one bar of signal.'),
        ('One tap to call', 'Your number is easy to find on every page, and tapping it calls you.'),
        ('Hours and services up front', 'The things people actually look for, without digging.'),
        ('Set up for Google', 'So people searching anywhere from San Francisco to San Jose can find you.'),
        ('Before and after photos', 'Great for trades and salons to show off real results.'),
    ]
    CHECK = '<svg class="benefit__check" viewBox="0 0 40 40" aria-hidden="true" focusable="false"><path d="M7 21c4 3 7 7 9 11C20 21 26 12 34 6" fill="none" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    ben_html = '\n'.join(f'''          <li class="benefit reveal" style="--d:{(n % 3) * 80}ms">
            {CHECK}
            <h3>{t}</h3>
            <p>{d}</p>
          </li>''' for n, (t, d) in enumerate(benefits))

    steps = [
        ('Free look at your current site', 'I check how your site works on a phone, how fast it loads and how easy it is to reach you.', 'Free'),
        ('I design a concept, free', 'You get a real redesign of your homepage to look at. Seeing it costs nothing and you&rsquo;re under no obligation.', 'Free'),
        ('You get a quote to own it', 'Like it? I give you a price for the full site, based on the pages and features your business needs. No surprises.', 'Quoted'),
        ('We refine it and launch', 'Tell me what to change, then I put it live, connect your domain and stay around for updates.', None),
    ]
    step_html = '\n'.join(f'''          <li class="step{' step--free' if badge else ''} reveal" style="--d:{n * 80}ms">
            {f'<span class="step__badge{" step__badge--quote" if badge == "Quoted" else ""}">{badge}</span>' if badge else ''}
            <span class="step__num" aria-hidden="true">{n+1}</span>
            <h3><span class="sr-only">Step {n+1}: </span>{t}</h3>
            <p>{d}</p>
          </li>''' for n, (t, d, badge) in enumerate(steps))

    # Industry showcase: one device stage, a tab per industry. Add a business by adding a row.
    IND = [
        dict(key='salon', tab='Salons &amp; beauty', icon='<path d="M6 3v6a6 6 0 0 0 12 0V3"/><path d="M12 15v6"/><path d="M8 21h8"/>',
             src=CHRISTINA_PREVIEW, live_url=CHRISTINA_URL, url_label='christinas-salon', live=True, name='Christina&rsquo;s Hair Salon', meta='Milpitas, CA &middot; Hair salon',
             text='A warm, easy site where customers see the services, find the salon inside Seafood City and tap to call. This is the real site, running live.',
             tags=['Tap to call', 'Today&rsquo;s hours', 'Directions'], cta='Visit the live site'),
    ]
    def ind_tab(n, d):
        on = n == 0
        return (f'<button class="ind-tab" type="button" role="tab" id="tab-{d["key"]}" aria-controls="panel-{d["key"]}" aria-selected="{"true" if on else "false"}"'
                f'{"" if on else " tabindex=\"-1\""} data-src="{d["src"]}" data-url="{d["url_label"]}">'
                f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{d["icon"]}</svg>{d["tab"]}</button>')
    def ind_panel(n, d):
        badge = ('<p class="ind-badge ind-badge--live"><span class="live-dot" aria-hidden="true"></span>Live client site</p>' if d['live']
                 else '<p class="ind-badge">Design concept</p>')
        tags = ''.join(f'<li>{t}</li>' for t in d['tags'])
        return f"""            <div class="ind-panel" role="tabpanel" id="panel-{d['key']}" aria-labelledby="tab-{d['key']}"{'' if n == 0 else ' hidden'}>
              {badge}
              <h3 class="project__title">{d['name']}</h3>
              <p class="project__meta">{d['meta']}</p>
              <p class="project__text">{d['text']}</p>
              <ul class="tags" role="list">{tags}</ul>
              <a class="btn btn--dark ind-cta" href="{d['live_url']}" target="_blank" rel="noopener">{d['cta']} {icon('arrow-right')}</a>
            </div>"""
    first = IND[0]
    MORE = ['Barbershops', 'Auto repair', 'Bakeries', 'Dentists', 'Gyms', 'Landscapers', 'Cafes', 'Boba shops', 'Cleaners', 'Contractors', 'Florists', 'Pet groomers']
    marquee = ''.join(f'<li>{m}</li>' for m in MORE)
    SHOWCASE = f"""          <div class="showcase reveal" data-showcase>
            <div class="ind-tabs" role="tablist" aria-label="Industries">
              {''.join(ind_tab(n, d) for n, d in enumerate(IND))}
              <span class="ind-soon"><span class="ind-soon__dots" aria-hidden="true"><i></i><i></i><i></i></span>More industries coming soon</span>
            </div>
            <div class="showcase__stage">
              <div class="live-media">
                <div class="laptop live-laptop">
                  <div class="laptop__lid"><div class="laptop__display">{MAC_BAR.replace('URL', '<span data-url-label>' + first['url_label'] + '</span>')}<div class="live-frame" data-w="1440" data-h="900"><iframe src="{first['src']}" title="Website preview, desktop view" width="1440" height="900" loading="lazy" tabindex="-1" scrolling="no"></iframe></div></div></div>
                  <div class="laptop__base" aria-hidden="true"></div>
                </div>
                <div class="live-phone"><div class="phone"><span class="phone__btn phone__btn--action" aria-hidden="true"></span><span class="phone__btn phone__btn--vol" aria-hidden="true"></span><span class="phone__btn phone__btn--vol2" aria-hidden="true"></span><span class="phone__btn phone__btn--power" aria-hidden="true"></span><span class="phone__btn phone__btn--cam" aria-hidden="true"></span><div class="phone__display"><div class="live-frame" data-w="390" data-h="844"><iframe src="{first['src']}" title="Website preview, phone view" width="390" height="844" loading="lazy" tabindex="-1" scrolling="no"></iframe></div></div></div></div>
              </div>
              <div class="showcase__info">
{chr(10).join(ind_panel(n, d) for n, d in enumerate(IND))}
              </div>
            </div>
          </div>
          <div class="ind-more" aria-label="Other businesses I design for">
            <p class="hand">Also great for</p>
            <div class="ind-marquee"><div class="ind-marquee__track"><ul role="list">{marquee}</ul><ul role="list" aria-hidden="true">{marquee}</ul></div></div>
          </div>
          <div class="projects projects--soon">
            <article class="project project--next project--wide reveal">
              <div class="project__body">
                <p class="project__eyebrow hand">Your business could be next</p>
                <h3 class="project__title"><a href="#contact">Want a site like this?</a></h3>
                <p class="project__meta">Send me your business name and I&rsquo;ll send back a free concept of your new homepage. If you want to keep it, I&rsquo;ll quote the price to own it, with no obligation.</p>
                <span class="project__more" aria-hidden="true">Get a free concept {icon('arrow-right')}</span>
              </div>
              <div class="ghost-site" aria-hidden="true">
                <div class="ghost-site__bar"><i></i><i></i><i></i><span>yourbusiness.com</span></div>
                <div class="ghost-site__body"><b></b><b></b><b class="short"></b><em></em><span class="hand">your site here</span></div>
              </div>
            </article>
          </div>
"""
    WORK_GRID = (f'''          <!-- To add a case study: copy one <article class="project"> block below, swap the images, text and link. -->
          <div class="projects">
            <article class="project reveal">
              <div class="project__thumb project__thumb--split" aria-hidden="true">
                <img class="project__shot" src="{I}christina-new-compare-720.webp" srcset="{I}christina-new-compare-720.webp 720w, {I}christina-new-compare.webp 1440w" sizes="(min-width: 1100px) 380px, (min-width: 700px) 46vw, 92vw" width="1440" height="704" alt="" loading="lazy" decoding="async">
                <img class="project__shot project__shot--before" src="{I}christina-old-compare-720.webp" srcset="{I}christina-old-compare-720.webp 720w, {I}christina-old-compare.webp 1440w" sizes="(min-width: 1100px) 380px, (min-width: 700px) 46vw, 92vw" width="1440" height="704" alt="" loading="lazy" decoding="async">
                <span class="project__divider"></span>
                <span class="project__tag project__tag--before">Before</span>
                <span class="project__tag project__tag--after">After</span>
              </div>
              <div class="project__body">
                <span class="label" data-project-label="christinas-salon">Concept redesign</span>
                <h3 class="project__title"><a href="work/christinas-salon.html">Christina&rsquo;s Hair Salon</a></h3>
                <p class="project__meta">Milpitas, CA &middot; Hair salon</p>
                <ul class="tags" role="list"><li>Redesign</li><li>Appointment form</li><li>Before/after slider</li></ul>
                <span class="project__more" aria-hidden="true">View case study {icon('arrow-right')}</span>
              </div>
            </article>

            <article class="project reveal" style="--d:80ms">
              <div class="project__thumb" aria-hidden="true">
                <img class="project__shot" src="{I}carrillo-desktop-960.webp" srcset="{I}carrillo-desktop-960.webp 960w, {I}carrillo-desktop.webp 1440w" sizes="(min-width: 1100px) 380px, (min-width: 700px) 46vw, 92vw" width="1440" height="900" alt="" loading="lazy" decoding="async">
              </div>
              <div class="project__body">
                <span class="label" data-project-label="j-carrillo-plumbing">Concept redesign</span>
                <h3 class="project__title"><a href="work/j-carrillo-plumbing.html">J. Carrillo Plumbing &amp; Drains</a></h3>
                <p class="project__meta">Hayward, CA &middot; Family-owned plumber</p>
                <ul class="tags" role="list"><li>Click to call</li><li>Callback form</li><li>Before/after slider</li></ul>
                <span class="project__more" aria-hidden="true">View case study {icon('arrow-right')}</span>
              </div>
            </article>

            <article class="project project--next reveal" style="--d:160ms">
              <div class="project__body">
                <span class="project__plus" aria-hidden="true">{icon('sparkle')}</span>
                <h3 class="project__title"><a href="#contact">Your business could be next</a></h3>
                <p class="project__meta">Send me your business name and I&rsquo;ll design a free concept, just like these.</p>
                <span class="project__more" aria-hidden="true">Get my free concept {icon('arrow-right')}</span>
              </div>
            </article>
          </div>
''' if SHOW_WORK else SHOWCASE)
    html = f'''{head(r, 'MDV Web Design | Bay Area Web Designer',
     'Modern, mobile-friendly websites for Bay Area businesses, based in Hayward. Free concept redesigns. Contact MDV Web Design for a quote.', '',
     preload='' if not SHOW_WORK else f'\n  <link rel="preload" as="image" href="{I}carrillo-desktop.webp" imagesrcset="{I}carrillo-desktop-960.webp 960w, {I}carrillo-desktop.webp 1440w, {I}carrillo-desktop-2x.webp 2880w" imagesizes="(min-width: 1100px) 900px, 84vw" fetchpriority="high">')}{LOADER_SCRIPT}
  <script type="application/ld+json">{json.dumps(SCHEMA, separators=(',', ':'))}</script>
  <script type="application/ld+json">{json.dumps(FAQ_SCHEMA, separators=(',', ':'))}</script>
</head>
<body>
{SKY_LOADER}
{header(r)}

    <main id="main">
      <!-- Hero -->
      <section class="hero" data-tone="light" aria-labelledby="hero-title">
        <div class="hero__copy">
          <p class="hand hero__hello">Hi, I&rsquo;m Mark!</p>
          <h1 class="hero__title display" id="hero-title">I make websites for <span class="swoosh">local businesses</span> in the Bay Area.</h1>
          <p class="hero__sub lead">Shops, salons, plumbers, restaurants. If your website is old, slow or hard to use on a phone, send me your business name. I&rsquo;ll design a new homepage for free, and you decide from there.</p>
          <div class="hero__ctas">
            <a class="btn btn--dark" href="#contact">Get my free concept {icon('arrow-right')}</a>
            <a class="btn btn--light" href="#work">See my work</a>
          </div>
          <p class="hand hero__area"><span>Hayward</span> &middot; <span>San Francisco</span> &middot; <span>Oakland</span> &middot; <span>San Leandro</span> &middot; <span>San Lorenzo</span> &middot; <span>Castro Valley</span> &middot; <span>Union City</span> &middot; <span>Fremont</span> &middot; <span>Newark</span> &middot; <span>Dublin</span> &middot; <span>Pleasanton</span> &middot; <span>Livermore</span> &middot; <span>Milpitas</span> &middot; <span>San Jose</span> &middot; <span>Santa Clara</span> &middot; <span>Sunnyvale</span></p>
        </div>

        <div class="hero__bay" aria-hidden="true">
          <svg viewBox="0 0 1200 90" preserveAspectRatio="none" focusable="false">
            <path class="hb-hills" d="M0 52 C90 30 170 24 250 38 C330 52 380 30 470 26 C560 22 640 44 720 40 C820 34 900 18 1000 24 C1080 29 1140 40 1200 36"/>
            <path class="hb-deck" d="M0 62 H200 C260 62 280 44 330 44 C380 44 400 62 460 62 H1200"/>
            <path class="hb-piers" d="M220 62v8M250 58v12M280 50v20M310 45v25M340 45v25M370 50v20M400 57v13M430 62v8M500 62v8M560 62v8M620 62v8M680 62v8M740 62v8M800 62v8M860 62v8M920 62v8M980 62v8M1040 62v8M1100 62v8M1160 62v8M40 62v8M100 62v8M160 62v8"/>
            <path class="hb-water" d="M60 80 H180 M260 84 H420 M520 79 H600 M700 85 H880 M960 80 H1080"/>
          </svg>
        </div>
      </section>

      <!-- Work -->
      <section class="section has-doodles" id="work" data-tone="light" aria-labelledby="work-title">
        {doodle('golden-gate')}{doodle('fog')}
        <div class="container">
          <div class="section-head section-head--split reveal">
            <div>
              <h2 class="h2" id="work-title">Recent work</h2>
            </div>
            <p class="lead">{'Concept redesigns for real local businesses. Built first, pitched second, so you can see the result before you spend a dollar.' if SHOW_WORK else 'A real site I designed and built, running live on a laptop and a phone. More industries are coming soon.'}</p>
          </div>

{WORK_GRID}        </div>
      </section>

      <!-- What you get -->
      <section class="section" id="benefits" data-tone="light" aria-labelledby="benefits-title" style="padding-top:0">
        <div class="container">
          <div class="section-head section-head--split reveal">
            <div>
              <h2 class="h2" id="benefits-title">Built to bring in customers</h2>
            </div>
          </div>
          <ul class="benefits" role="list">
{ben_html}
          </ul>
          <div class="street" aria-hidden="true">{''.join(doodle(n) for n in ['taco-truck', 'bakery', 'barbershop', 'coffee', 'auto-shop', 'transamerica', 'hair-salon', 'florist', 'boba', 'landscaping', 'plumber-van'])}</div>
        </div>
      </section>

      <!-- Process -->
      <section class="section tone-dark panel" id="process" data-tone="dark" aria-labelledby="process-title">
        <div class="container">
          <div class="section-head section-head--split reveal">
            <div>
              <h2 class="h2" id="process-title">The concept is free. Owning it is quoted.</h2>
            </div>
          </div>
          <ol class="steps" role="list">
{step_html}
          </ol>
          <div class="chapter-cta reveal">
            <p>Curious what step two looks like for your business?</p>
            <a class="btn btn--lime" href="#contact">Get my free concept {icon('arrow-right')}</a>
          </div>
        </div>
      </section>

      <!-- About -->
      <section class="section has-doodles" id="about" data-tone="light" aria-labelledby="about-title">
        {doodle('sailboat')}{doodle('redwood')}{doodle('painted-ladies')}
        <div class="container about">
          <figure class="polaroid reveal">
            <span class="polaroid__tape" aria-hidden="true"></span>
            <div class="polaroid__window">
              {mark_anim('', cls='polaroid__logo', lazy=True, big=True)}
              <img class="polaroid__pic" src="assets/img/mark.jpg" width="840" height="1050" alt="Mark, the web designer behind MDV Web Design" loading="lazy" decoding="async" onerror="this.remove()">
            </div>
            <figcaption class="hand">Mark &middot; MDV Web Design<small>Hayward, CA</small></figcaption>
          </figure>
          <div class="about__body reveal" style="--d:80ms">
            <h2 class="h2" id="about-title">A bit about me</h2>
            <p class="lead">I was born and raised in Hayward. All my life I&rsquo;ve walked into great local businesses whose websites don&rsquo;t do them justice, or who don&rsquo;t have one at all. I started MDV Web Design to put those businesses on the map, so the people who need them can actually find them.</p>
            <p class="lead">You deal with me directly, from the first concept to launch day and any changes after. No agency, no runaround.</p>
            <ul class="facts" role="list">
              <li>{icon('pin')} Based in Hayward</li>
              <li>{icon('store')} Trades, salons, restaurants, shops</li>
              <li>{icon('phone')} All around the Bay, 415, 510 and 408</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section class="section faq-section" id="faq" data-tone="light" aria-labelledby="faq-title">
        <div class="container faq">
          <div class="section-head reveal">
            <h2 class="h2" id="faq-title">Questions people ask</h2>
            <p class="lead">Have a question? These are the ones business owners ask me most, with honest answers.</p>
          </div>
          <div class="faq__list reveal">
            <details class="faq__item">
              <summary>How much does a website cost?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>Every business needs something a little different, so every project gets its own quote based on the pages and features you need. The concept is always free, so you see exactly what you would be getting before you spend anything.</p>
            </details>
            <details class="faq__item">
              <summary>Is the free concept really free?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>Yes. I design a new homepage for your business and send it to you. If you don&rsquo;t love it, you owe nothing and there are no hard feelings.</p>
            </details>
            <details class="faq__item">
              <summary>How long does it take?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>Most small business sites take about 2 to 4 weeks from the day you say yes to launch day. Having your photos and info ready speeds things up.</p>
            </details>
            <details class="faq__item">
              <summary>I already have a website. Can you redesign it?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>Absolutely. Most of my work is giving older sites a fresh look that works on phones. I can keep your domain, so customers still find you at the same address.</p>
            </details>
            <details class="faq__item">
              <summary>Do I need to write the text or take photos?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>No. I can write the words for you based on a quick chat, and use your own photos if you have them. Real photos of your work and your team always help the most.</p>
            </details>
            <details class="faq__item">
              <summary>Will I own my website?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>Yes. Once it&rsquo;s paid for, the site and the domain are yours. I&rsquo;m happy to stick around for updates, but you&rsquo;re never locked in.</p>
            </details>
            <details class="faq__item">
              <summary>Are there any ongoing costs?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>If you skip my monthly care plan, you pay the companies that keep your site online directly. Your domain name, like yourbusiness.com, renews every year and usually costs about $10 to $25 a year, depending on the name and the company. Some companies let you pay monthly instead. Hosting for a small site like this is often free, or a few dollars a month. None of that money goes to me. If you&rsquo;d rather not deal with it, my optional care plan covers hosting, monthly checkups and small updates for one monthly fee, and your domain always stays in your name.</p>
            </details>
            <details class="faq__item">
              <summary>Can you help people find me on Google?<span class="faq__icon" aria-hidden="true"></span></summary>
              <p>Every site I build is set up for Google from day one, with your services, hours and service area clearly listed. I can also help you set up or clean up your Google Business Profile.</p>
            </details>
          </div>
        </div>
      </section>

      <!-- Contact -->
      <section class="section tone-dark panel panel--flush-bottom" id="contact" data-tone="dark" aria-labelledby="contact-title">
        <div class="container contact">
          <div class="contact__intro reveal">
            <h2 class="contact__title" id="contact-title">Tell me about your business.</h2>
            <p class="lead">Send me your business name and what you&rsquo;d like your website to do. I&rsquo;ll take a look and get back to you.</p>
            <div class="contact__details">
              <a class="contact__email" href="mailto:markdv.webdesign@gmail.com">{icon('mail')} markdv.webdesign@gmail.com</a>
              <p class="contact__place">{icon('pin')} Hayward, CA &middot; Serving the whole Bay Area</p>
            </div>
            <p class="contact__note">The concept is always free. The price to own your site depends on its size and features, so every project gets its own quote. I&rsquo;ll reply within 1 to 4 business days.</p>
          </div>

          <div class="form-card reveal" style="--d:80ms">
            <form class="form" name="quote" method="POST" action="https://api.web3forms.com/submit" novalidate data-quote-form>
              <input type="hidden" name="access_key" value="468499aa-e51f-4e4e-a295-7cfdf873344c">
              <input type="hidden" name="subject" value="New free concept request from MDV Web Design site">
              <input type="hidden" name="from_name" value="MDV Web Design website">
              <input type="hidden" name="redirect" value="https://mdvwebdesign.com/thanks.html">
              <p class="hp" aria-hidden="true"><label>Leave this empty <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off"></label></p>
              <p class="form__hint">Fields marked <span class="req" aria-hidden="true">*</span> are required.</p>

              <div class="form__row">
                <div class="field">
                  <label for="f-name">Name <span class="req" aria-hidden="true">*</span></label>
                  <input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="e-name">
                  <p class="field__error" id="e-name" aria-live="polite"></p>
                </div>
                <div class="field">
                  <label for="f-business">Business name <span class="req" aria-hidden="true">*</span></label>
                  <input id="f-business" name="business" type="text" autocomplete="organization" required aria-describedby="e-business">
                  <p class="field__error" id="e-business" aria-live="polite"></p>
                </div>
              </div>
              <div class="form__row">
                <div class="field">
                  <label for="f-email">Email <span class="req" aria-hidden="true">*</span></label>
                  <input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required aria-describedby="e-email">
                  <p class="field__error" id="e-email" aria-live="polite"></p>
                </div>
                <div class="field">
                  <label for="f-phone">Phone <span class="opt">(optional)</span></label>
                  <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel">
                </div>
              </div>
              <div class="field">
                <label for="f-site">Current website <span class="opt">(optional)</span></label>
                <input id="f-site" name="website" type="text" autocomplete="url" inputmode="url" placeholder="yourbusiness.com" aria-describedby="e-site">
                <p class="field__error" id="e-site" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="f-message">Message <span class="req" aria-hidden="true">*</span></label>
                <textarea id="f-message" name="message" rows="5" required aria-describedby="e-message" placeholder="What does your business do, and what would you like your website to do better?"></textarea>
                <p class="field__error" id="e-message" aria-live="polite"></p>
              </div>
              <div class="field">
                <label for="f-inspo">Websites you like <span class="opt">(optional)</span></label>
                <textarea id="f-inspo" name="inspiration" rows="3" aria-describedby="h-inspo" placeholder="Paste links to any sites you love the look of, one per line"></textarea>
                <p class="field__hint" id="h-inspo">Any kind of business works. I&rsquo;ll use them as inspiration for your free concept.</p>
              </div>
              <p class="form__status" role="alert" data-form-status></p>
              <button class="btn btn--lime btn--block" type="submit" data-submit>
                <span data-submit-label>Get my free concept</span> {icon('arrow-right')}
              </button>
            </form>

            <div class="thanks" role="status" tabindex="-1" hidden data-thanks>
              {icon('check')}
              <h3>Got it.</h3>
              <p>Thanks! I&rsquo;ll get back to you within 1 to 4 business days.</p>
            </div>
          </div>
        </div>
      </section>
    </main>

{footer(r)}
{menu(r)}
{tail(r)}'''
    return html

# ---------------- Case studies ----------------
CASES = {
    'j-carrillo-plumbing': dict(
        key='carrillo', name='J. Carrillo Plumbing &amp; Drains', plain='J. Carrillo Plumbing & Drains', short='J. Carrillo Plumbing',
        city='Hayward, CA', type='Family-owned plumber, open 24 hours Monday to Saturday',
        title='J. Carrillo Plumbing Concept Redesign | MDV Web Design',
        desc='A concept redesign for J. Carrillo Plumbing & Drains in Hayward, CA: click-to-call, a callback form and a before/after slider. By MDV Web Design.',
        goal=['When a pipe bursts or a drain backs up, nobody wants to read. They want a phone number they can tap and proof that the plumber is local, licensed and fair.',
              'The site&rsquo;s job is to get that person to call right away, or leave a number for a callback, in the first few seconds.'],
        built=['Sticky click-to-call phone number that stays on screen',
               '&ldquo;Call me back&rdquo; form right in the hero',
               'Service list: drain cleaning, sewer line replacement, water heaters, faucets and sinks, leak repair, commercial',
               'Drag-to-compare before/after slider of a kitchen sink job',
               '&ldquo;Family owned since 2009&rdquo; story',
               'Trust points: licensed, and no extra charge for nights or weekends',
               'Yelp reviews section',
               'FAQ and contact section with directions'],
        colors=[('Navy', '#1F2F5C'), ('Blue', '#2569C9'), ('Red', '#C93A22'), ('Mist', '#EFF4FA')],
        fonts=[('Barlow Condensed', 'Headings', "'Barlow Condensed', sans-serif", 700, 'DRAINS CLEARED.'),
               ('Barlow', 'Body text', "'Barlow', sans-serif", 400, 'Family owned since 2009.')],
        font_url='https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700&family=Barlow:wght@400&display=swap',
        why='Navy and red read as trustworthy, solid and urgent, like a service truck pulling up. Tall condensed headings say &ldquo;we fix it today&rdquo; without shouting.',
        next='christinas-salon', next_name='Christina&rsquo;s Hair Salon',
        lap_alt='J. Carrillo Plumbing concept redesign homepage: navy hero with the headline Drains cleared, pipes fixed and a red call button',
        phone_alt='J. Carrillo Plumbing concept redesign on a phone with the call button at the top',
        full_alt='Full J. Carrillo Plumbing concept redesign page on desktop: services, before/after kitchen sink slider, family story, reviews, FAQ and quote form',
        mfull_alt='Full J. Carrillo Plumbing concept redesign page on a phone',
        dfull_h=6682, mfull_h=16010,
    ),
    'christinas-salon': dict(
        key='christina', name='Christina&rsquo;s Hair Salon', plain="Christina's Hair Salon", short="Christina's Hair Salon",
        city='Milpitas, CA', type='Filipino-operated hair salon for women, men and kids',
        title="Christina's Hair Salon Concept Redesign | MDV Web Design",
        desc="A concept redesign for Christina's Hair Salon in Milpitas, CA, with an old-site vs. new-site comparison. Services, hours and booking made obvious. By MDV Web Design.",
        goal=['Christina&rsquo;s sits inside the Seafood City shopping center and is known for rebonding and keratin. Customers need to know what she offers, when she&rsquo;s open and how to find the suite.',
              'The site&rsquo;s job is to make services, hours and location obvious, and make it easy to call or request an appointment.'],
        built=['Services menu for women, men and kids',
               'Rebonding and keratin specialty section',
               'Drag-to-compare before/after bob haircut slider',
               'Stylist cards',
               'Hours table with &ldquo;good to know&rdquo; details',
               'Google Maps directions',
               'Appointment request form',
               'Instagram links and a mobile call bar'],
        colors=[('Taupe', '#B3A584'), ('Warm brown', '#5B544B'), ('Sand', '#F1ECE2')],
        fonts=[('Anton', 'Display name', "'Anton', sans-serif", 400, "CHRISTINA'S"),
               ('Mr Dafoe', 'Script accent', "'Mr Dafoe', cursive", 400, 'Hair Salon'),
               ('Young Serif', 'Headings', "'Young Serif', serif", 400, 'Beauty and care'),
               ('Figtree', 'Body text', "'Figtree', sans-serif", 400, 'Walk-ins welcome.')],
        font_url='https://fonts.googleapis.com/css2?family=Anton&family=Figtree:wght@400&family=Mr+Dafoe&family=Young+Serif&display=swap',
        why='Taupe, warm brown and sand feel warm, personal and welcoming, like the salon itself. A bold name with a handwritten script keeps it friendly, not fussy.',
        next='j-carrillo-plumbing', next_name='J. Carrillo Plumbing &amp; Drains',
        lap_alt="Christina's Hair Salon concept redesign homepage: the salon name in bold taupe letters with a script accent, beside a photo of a stylist at work",
        phone_alt="Christina's Hair Salon concept redesign on a phone",
        full_alt="Full Christina's Hair Salon concept redesign page on desktop: services menu, keratin section, before/after haircut slider, stylists, hours and appointment form",
        mfull_alt="Full Christina's Hair Salon concept redesign page on a phone",
        dfull_h=6875, mfull_h=16149,
    ),
}

def page_case(slug):
    c = CASES[slug]; r = '../'; k = c['key']; P = f'{r}{I}{k}'
    extra = f'\n  <link rel="stylesheet" href="{c["font_url"]}" media="print" onload="this.media=\'all\'">'
    extra += f'\n  <link rel="preload" as="image" href="{P}-desktop.webp" imagesrcset="{P}-desktop-960.webp 960w, {P}-desktop.webp 1440w, {P}-desktop-2x.webp 2880w" imagesizes="(min-width: 1100px) 930px, 86vw" fetchpriority="high">'
    sw = '\n'.join(f'''            <li class="swatch"><span class="swatch__chip" style="background:{h}"></span><span class="swatch__name">{n}</span><span class="swatch__hex">{h}</span></li>''' for n, h in c['colors'])
    fonts = '\n'.join(f'''            <li><span class="fonts__sample" style="font-family:{fam};font-weight:{wt}" aria-hidden="true">{sample}</span><span><strong>{n}</strong> <span class="fonts__role">&middot; {role}</span></span></li>''' for n, role, fam, wt, sample in c['fonts'])
    built = '\n'.join(f'            <li>{icon("check")}<span>{b}</span></li>' for b in c['built'])
    goal = '\n'.join(f'            <p class="lead">{g}</p>' for g in c['goal'])
    old_new = ''
    if slug == 'christinas-salon':
        cmp = compare(f'{r}{I}christina-old-compare.webp', f'{r}{I}christina-old-compare-720.webp 720w, {r}{I}christina-old-compare.webp 1440w, {r}{I}christina-old-compare-2x.webp 1893w',
                      f'{r}{I}christina-new-compare.webp', f'{r}{I}christina-new-compare-720.webp 720w, {r}{I}christina-new-compare.webp 1440w, {r}{I}christina-new-compare-2x.webp 2880w',
                      1440, 704, "Before: Christina's Hair Salon's old website, a plain page of small text under a photo banner",
                      "After: the concept redesign with a bold salon name, a stylist photo and a call to book button",
                      "Compare Christina's Hair Salon's old website with the redesign", '(min-width: 1240px) 1200px, 92vw', 'compare-case')
        old_new = f'''
        <section class="case-block" aria-labelledby="h-compare" style="grid-template-columns:1fr">
          <div class="reveal">
            <h2 class="case-block__title" id="h-compare">Same salon. Different first impression.</h2>
          </div>
          <div class="reveal">
            <div class="browser">
              <div class="browser__bar" aria-hidden="true"><i></i><i></i><i></i><span>Old site vs. redesign</span></div>
              {cmp}
            </div>
            <p class="compare-caption">Drag the handle or use the arrow keys. Left: the current website. Right: my concept.</p>
          </div>
        </section>'''

    html = f'''{head(r, c['title'], c['desc'], f'work/{slug}.html', extra_fonts=extra)}
</head>
<body>
{header(r, home=False)}

    <main id="main">
      <section class="case-hero" data-tone="light" aria-labelledby="case-title">
        <div class="container">
          <a class="back-link" href="{r}index.html#work">{icon('arrow-left')} Back to work</a>
          <div><span class="label" data-project-label="{slug}">Concept redesign</span></div>
          <h1 class="case-hero__title" id="case-title">{c['name']}</h1>
          <ul class="case-hero__meta" role="list">
            <li>{icon('pin')} {c['city']}</li>
            <li>{icon('store')} {c['type']}</li>
          </ul>
        </div>
        <div class="case-stage">
          <div class="float">
{laptop(f'{P}-desktop.webp', f'{P}-desktop-960.webp 960w, {P}-desktop.webp 1440w, {P}-desktop-2x.webp 2880w', '(min-width: 1100px) 930px, 86vw', c['lap_alt'], eager=True)}
          </div>
          <div class="phone-wrap float float--slow">
{phone(f'{P}-mobile.webp', f'{P}-mobile-390.webp 390w, {P}-mobile.webp 780w, {P}-mobile-3x.webp 1170w', '(min-width: 768px) 240px, 30vw', c['phone_alt'], eager=True)}
          </div>
        </div>
      </section>

      <div class="section" style="padding-top:0;padding-bottom:0">
        <div class="container">
        <section class="case-block" aria-labelledby="h-goal">
          <h2 class="case-block__title reveal" id="h-goal">The goal</h2>
          <div class="reveal" style="display:grid;gap:16px">
{goal}
          </div>
        </section>
{old_new}
        <section class="case-block" aria-labelledby="h-built">
          <h2 class="case-block__title reveal" id="h-built">What I built</h2>
          <ul class="features reveal" role="list">
{built}
          </ul>
        </section>

        <section class="case-block" aria-labelledby="h-design">
          <h2 class="case-block__title reveal" id="h-design">Design choices</h2>
          <div class="reveal">
            <ul class="swatches" role="list" aria-label="Color palette">
{sw}
            </ul>
            <ul class="fonts" role="list" aria-label="Fonts">
{fonts}
            </ul>
            <p class="lead design-why">{c['why']}</p>
          </div>
        </section>

        <section class="case-block" aria-labelledby="h-shots">
          <h2 class="case-block__title reveal" id="h-shots">Screenshots</h2>
          <div class="shots reveal">
            <figure>
              <div class="browser">
                <div class="browser__bar" aria-hidden="true"><i></i><i></i><i></i><span>Desktop &middot; full page</span></div>
                <div class="shot-scroll" tabindex="0" role="region" aria-label="Full desktop page, scrollable">
                  <img src="{P}-desktop-full.webp" width="1440" height="{c['dfull_h']}" alt="{c['full_alt']}" loading="lazy" decoding="async">
                </div>
              </div>
              <figcaption>Scroll inside the frame to see the whole page.</figcaption>
            </figure>
            <figure class="shots__phone">
              <div class="phone"><span class="phone__btn phone__btn--action" aria-hidden="true"></span><span class="phone__btn phone__btn--vol" aria-hidden="true"></span><span class="phone__btn phone__btn--vol2" aria-hidden="true"></span><span class="phone__btn phone__btn--power" aria-hidden="true"></span><span class="phone__btn phone__btn--cam" aria-hidden="true"></span>
                <div class="phone__display shot-scroll" tabindex="0" role="region" aria-label="Full mobile page, scrollable">
                  <span class="phone__status" aria-hidden="true"><b>9:41</b><svg viewBox="0 0 68 12" focusable="false"><g fill="currentColor"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0.5" width="3" height="11.5" rx="1"/><path d="M31 3.2a9.5 9.5 0 0 1 12.6 0l-1.5 1.6a7.3 7.3 0 0 0-9.6 0zM33.4 5.8a6 6 0 0 1 7.8 0l-1.5 1.6a3.8 3.8 0 0 0-4.8 0zM37.3 11.6 35.6 9.9a2.5 2.5 0 0 1 3.4 0z"/><rect x="48" y="0.5" width="17" height="11" rx="3.2" fill="none" stroke="currentColor" stroke-opacity=".4"/><rect x="50" y="2.5" width="12.5" height="7" rx="1.8"/><rect x="66" y="4" width="1.6" height="4" rx=".8" fill-opacity=".45"/></g></svg></span>
                  <img src="{P}-mobile-full.webp" width="670" height="{c['mfull_h']}" alt="{c['mfull_alt']}" loading="lazy" decoding="async">
                </div>
              </div>
              <figcaption>Mobile, 390px wide.</figcaption>
            </figure>
          </div>
        </section>

        <p class="disclaimer" data-concept-only="{slug}">This is an unsolicited concept redesign created as a portfolio sample. MDV Web Design is not affiliated with {c['name']}, and this design is not their official website.</p>
        </div>
      </div>

      <section class="section" style="padding-top:0" aria-labelledby="cta-title">
        <div class="container">
          <div class="case-cta tone-dark panel" data-tone="dark">
            <h2 id="cta-title">Want this for your business?</h2>
            <a class="btn btn--lime" href="{r}index.html#contact">Get my free concept {icon('arrow-right')}</a>
          </div>
          <a class="next-project" href="{c['next']}.html">
            <small>Next project</small>
            <strong>{c['next_name']} {icon('arrow-right')}</strong>
          </a>
        </div>
      </section>
    </main>

{footer(r)}
{menu(r, home=False)}
{tail(r)}'''
    return html

def page_simple(kind):
    r = '/'  # served from site root; absolute paths keep 404 working at any depth
    if kind == 'thanks':
        t, d, h1, body, ic = ('Thanks | MDV Web Design', 'Thanks for reaching out to MDV Web Design.', 'Thanks!',
                              'I&rsquo;ll get back to you within 1 to 4 business days. If it&rsquo;s easier, you can also email me at <a href="mailto:markdv.webdesign@gmail.com">markdv.webdesign@gmail.com</a>.', 'check')
    else:
        t, d, h1, body, ic = ('Page not found | MDV Web Design', 'This page could not be found.', 'Lost?',
                              'That page doesn&rsquo;t exist, but your new website could. Head back home or send me a note.', 'search')
    html = f'''{head(r, t, d, 'thanks.html' if kind == 'thanks' else '404.html')}
  <meta name="robots" content="noindex">
</head>
<body>
{header(r, home=False)}

    <main id="main">
      <section class="simple" data-tone="light" aria-labelledby="simple-title">
        <div class="simple__inner">
          <span class="simple__mark">{icon(ic)}</span>
          <h1 class="simple__title" id="simple-title">{h1}</h1>
          <p class="lead">{body}</p>
          <div class="hero__ctas">
            <a class="btn btn--dark" href="{r}index.html">Back to home</a>
            <a class="btn btn--light" href="{r}index.html#{'work' if SHOW_WORK else 'process'}">{'See my work' if SHOW_WORK else 'How it works'}</a>
          </div>
        </div>
      </section>
    </main>

{footer(r)}
{menu(r, home=False)}
{tail(r)}'''
    return html

import os
os.makedirs(f'{OUT}/work', exist_ok=True)
open(f'{OUT}/index.html', 'w').write(page_index())
os.makedirs(f'{OUT}/work', exist_ok=True)
for s in CASES: open(f'{OUT}/work/{s}.html', 'w').write(page_case(s))
open(f'{OUT}/thanks.html', 'w').write(page_simple('thanks'))
open(f'{OUT}/404.html', 'w').write(page_simple('404'))
print('built')
