// Frame-accurate renderer: loads a composition, calls window.seek(t) per frame,
// screenshots it and pipes PNGs into ffmpeg.
// Usage:
//   node render.mjs <comp.html> <out.mp4> --w 1080 --h 1920 --fps 60 --dur 18.5
//   node render.mjs <comp.html> <outdir> --stills 0.5,2.6,4.1     (PNG stills)
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { mkdirSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const comp = resolve(args[0]);
const out = resolve(args[1]);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const W = +opt('w', 1080), H = +opt('h', 1920), FPS = +opt('fps', 60);
const DUR = +opt('dur', 0);
const stills = opt('stills', null);
const from = +opt('from', 0), to = +opt('to', 0);

const browser = await chromium.launch({
  channel: 'msedge',
  args: ['--allow-file-access-from-files', '--disable-web-security', '--force-color-profile=srgb', '--hide-scrollbars'],
});
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
page.on('console', m => { if (m.type() === 'error' || m.text().startsWith('[comp]')) console.log('[page]', m.text()); });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.goto(pathToFileURL(comp).href);
await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
const total = DUR || await page.evaluate(() => window.DURATION);

async function shot() { return page.screenshot({ type: 'jpeg', quality: 95 }); }

if (stills) {
  if (!existsSync(out)) mkdirSync(out, { recursive: true });
  for (const s of stills.split(',').map(Number)) {
    await page.evaluate(t => { window.seek(t - 1 / 60); window.seek(t); }, s);
    await page.screenshot({ path: join(out, `still_${s.toFixed(2)}.png`) });
    console.log('still', s);
  }
  await browser.close();
  process.exit(0);
}

const n0 = Math.round(from * FPS);
const n1 = to ? Math.round(to * FPS) : Math.round(total * FPS);
const ff = spawn('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error',
  '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
  '-vf', 'scale=in_range=pc:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
  '-x264-params', 'colorprim=bt709:transfer=bt709:colormatrix=bt709:range=tv',
  '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });

const t0 = Date.now();
if (n0 > 0) await page.evaluate(t => window.seek(t), (n0 - 1) / FPS);
for (let f = n0; f < n1; f++) {
  await page.evaluate(t => new Promise(res => { window.seek(t); requestAnimationFrame(() => requestAnimationFrame(res)); }), f / FPS);
  const buf = await shot();
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (f % 60 === 0) {
    const el = (Date.now() - t0) / 1000, done = f - n0 + 1;
    console.log(`frame ${f}/${n1}  ${(done / el).toFixed(1)} fps  eta ${((n1 - f) / (done / el)).toFixed(0)}s`);
  }
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log('done', out, ((Date.now() - t0) / 1000).toFixed(1) + 's');
