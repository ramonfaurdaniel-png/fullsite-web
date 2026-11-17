// Renders fullsite-launch.html -> 1080p60 MP4 with the soundtrack.
// usage: node render.js <lang es|en> [out.mp4]
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs'), os = require('os'), { execFileSync } = require('child_process');
const LANG = process.argv[2] || 'es', OUT = process.argv[3] || `fullsite-launch-${LANG}.mp4`;
const FPS = 60, DUR = 51, WORKERS = 4, N = Math.round(DUR * FPS);
const dir = path.join(os.tmpdir(), 'fs-frames-' + LANG);
fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const t0 = Date.now(); let done = 0;
  await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', e => console.log('ERR', e.message));
    await p.goto('file://' + path.resolve(__dirname, 'fullsite-launch.html') + '?render&lang=' + LANG);
    await p.evaluate(() => window.ready);
    for (let i = w; i < N; i += WORKERS) {
      await p.evaluate(t => seek(t), i / FPS);
      await p.screenshot({ path: path.join(dir, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 93 });
      if (++done % 300 === 0) console.log(`${LANG} ${done}/${N} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
  await b.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%05d.jpg'),
    '-i', path.resolve(__dirname, 'assets/soundtrack.wav'),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '21', '-maxrate', '22M', '-bufsize', '44M', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', path.resolve(__dirname, OUT)], { stdio: 'inherit' });
  console.log('done', OUT, ((Date.now() - t0) / 1000).toFixed(0) + 's');
})();
