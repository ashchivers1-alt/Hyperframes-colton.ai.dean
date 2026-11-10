// snapshot a built comp at given times: node snap.mjs <compdir> <out-prefix> t1 t2 ...
import { chromium } from '/Users/ashleychivers/Documents/Claude Video Studio/node_modules/playwright/index.mjs';
const [dir, out, ...ts] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/Users/ashleychivers/.cache/hyperframes/chrome/chrome-headless-shell/mac_arm-152.0.7977.30/chrome-headless-shell-mac-arm64/chrome-headless-shell' });
console.log('launched');
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
p.on('console', m => console.log('console:', m.text())); p.on('pageerror', e => console.log('err:', e.message));
await p.goto('file://' + dir + '/index.html', { waitUntil: 'load', timeout: 20000 }); console.log('loaded');
await p.evaluate(() => { document.body.style.background = '#3a4048'; });
for (const t of ts) { await p.evaluate(t => window.__timelines.main.seek(+t, false), t); await p.screenshot({ path: `${out}-${t}.png`, timeout: 30000 }); console.log('shot', t); }
await b.close();
