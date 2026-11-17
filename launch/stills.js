// node stills.js out_dir t1 t2 ...  -> one JPEG per timestamp (for checking frames)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [out, ...ts] = process.argv.slice(2);
  const lang = process.env.LANG_V || 'es';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  p.on('console', m => { if (m.type() === 'error') console.log('CONSOLE', m.text()); });
  await p.goto('file://' + path.resolve(__dirname, 'fullsite-launch.html') + '?render&lang=' + lang);
  await p.evaluate(() => window.ready);
  for (const t of ts) {
    await p.evaluate(t => seek(+t), t);
    await p.screenshot({ path: `${out}/f_${t}.jpg`, quality: 80, type: 'jpeg' });
  }
  await b.close();
})();
