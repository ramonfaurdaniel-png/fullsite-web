// Renders fullsite-launch.html to frames in parallel, then muxes MP4 with the soundtrack.
// node render.js [fps=30] [out=fullsite-launch.mp4]
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const FPS = +(process.argv[2] || 30), OUT = process.argv[3] || 'fullsite-launch.mp4', DUR = 51, WORKERS = 4;
const N = Math.round(DUR * FPS);
const dir = path.join(require('os').tmpdir(), 'fs-frames');
fs.mkdirSync(dir, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const t0 = Date.now(); let done = 0;
  await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
    const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
    p.on('pageerror', e => console.log('ERR', e.message));
    await p.goto('file://' + path.resolve(__dirname, 'fullsite-launch.html') + '?render');
    await p.evaluate(() => window.ready);
    for (let i = w; i < N; i += WORKERS) {
      await p.evaluate(t => seek(t), i / FPS);
      await p.screenshot({ path: path.join(dir, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 94 });
      if (++done % 150 === 0) console.log(`${done}/${N} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
  }));
  await b.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f%05d.jpg'),
    '-i', path.resolve(__dirname, 'assets/soundtrack.wav'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', path.resolve(__dirname, OUT)], { stdio: 'inherit' });
  console.log('done', OUT, ((Date.now() - t0) / 1000).toFixed(0) + 's');
})();
