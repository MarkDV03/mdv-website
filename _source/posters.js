// Still images shown in the laptop and phone while Christina's live preview loads.
// Run after refreshing live/christinas-salon:  node _source/posters.js  (needs a server on :8765 serving the repo root)
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [name, w, h, phone] of [['desktop', 1440, 900, false], ['phone', 390, 844, true]]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.goto('http://localhost:8765/live/christinas-salon/', { waitUntil: 'networkidle' });
    await p.addStyleTag({ content: 'html{scrollbar-width:none}html::-webkit-scrollbar{display:none}[data-reveal],.reveal{opacity:1!important;transform:none!important;transition:none!important}' + (phone ? '.topbar,.announce,.alert,.top-bar,.hours-bar{display:none!important}' : '') });
    await p.waitForTimeout(2500);
    await p.screenshot({ path: `_source/poster-${name}.png` });
    await p.close();
  }
  await b.close();
})();
