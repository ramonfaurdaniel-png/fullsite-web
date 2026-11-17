// Renders UI cards (HTML) to transparent 1920x1080 PNGs, plus a solid mask of each card's shape
// (used to blur the footage behind it = real frosted glass).
// usage: node cards_render.js cards.json out_dir
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [spec, out] = process.argv.slice(2);
  const cards = JSON.parse(fs.readFileSync(spec, 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  for (const c of cards) {
    await page.setContent(c.html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: `${out}/${c.name}.png`, omitBackground: true });
    await page.evaluate(() => document.body.classList.add('mask'));
    await page.screenshot({ path: `${out}/${c.name}_m.png`, omitBackground: true });
  }
  await browser.close();
})();
