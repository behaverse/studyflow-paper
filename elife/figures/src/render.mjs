import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { spawn, execFileSync } from 'node:child_process';
import { crc32 } from 'node:zlib';
// usage: node render.mjs <in.studyflow.yaml | panel.svg> <out.png> [scale]
// A .studyflow.yaml is drawn by the modeler and its source embedded in the PNG; a hand-drawn .svg panel is
// only rasterized, at the same scale and print size.
const origin = 'http://127.0.0.1:4175';
const [input, outPath, scaleArg] = process.argv.slice(2);
const scale = Number(scaleArg ?? 4);
const cli = 'packages/cli/dist/studyflow.mjs';
const MM_PER_UNIT = Number(process.env.MM_PER_UNIT ?? 0.2);
function withPrintSize(png) {
  // Every figure prints at one scale, 1 diagram unit = MM_PER_UNIT mm (11-12 unit labels at 6.2-6.8 pt): a pHYs
  // chunk after IHDR gives the raster that physical size. A figure too big for a page at that scale sets its own.
  const phys = Buffer.alloc(21);
  phys.writeUInt32BE(9, 0); phys.write('pHYs', 4, 'latin1');
  const ppm = Math.round(scale / MM_PER_UNIT * 1000);
  phys.writeUInt32BE(ppm, 8); phys.writeUInt32BE(ppm, 12); phys[16] = 1;
  phys.writeUInt32BE(crc32(phys.subarray(4, 17)), 17);
  return Buffer.concat([png.subarray(0, 33), phys, png.subarray(33)]);
}
async function rasterize(browser, svgText) {
  const p2 = await browser.newPage({ deviceScaleFactor: scale, viewport:{width:1600,height:1000} });
  await p2.setContent(`<html><body style="margin:0;background:#fff">${svgText}</body></html>`);
  await p2.waitForTimeout(500);
  return p2.locator('svg').first().screenshot({ type:'png', omitBackground:false });
}
if (input.endsWith('.svg')) {
  const browser = await chromium.launch().catch(() => chromium.launch({ channel: 'chrome' }));
  writeFileSync(outPath, withPrintSize(await rasterize(browser, readFileSync(input, 'utf8'))));
  console.log('wrote', outPath);
  await browser.close(); process.exit(0);
}
async function up(){ try { return (await fetch(origin+'/app')).ok } catch { return false } }
let child;
if (!(await up())) {
  child = spawn('npm',['run','dev','-w','@behaverse/studyflow-modeler','--','--host','127.0.0.1','--port','4175'],{stdio:'ignore'});
  const t=Date.now()+120000; while(Date.now()<t && !(await up())) await new Promise(r=>setTimeout(r,500));
}
// Playwright's own Chromium when installed, else this machine's Chrome.
const browser = await chromium.launch().catch(() => chromium.launch({ channel: 'chrome' }));
const ctx = await browser.newContext({acceptDownloads:true, viewport:{width:1600,height:1000}});
const page = await ctx.newPage();
page.on('console', m => { if (['error','warning'].includes(m.type())) console.log('[console.'+m.type()+']', m.text().slice(0,200)); });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.route(/api\.iconify\.design\/([^/]+)\/([^/.]+)\.svg/, async (route) => {
  const m = route.request().url().match(/api\.iconify\.design\/([^/]+)\/([^/.]+)\.svg/);
  try {
    const set = JSON.parse(readFileSync(`node_modules/@iconify/json/json/${m[1]}.json`,'utf8'));
    let name = m[2]; while (set.aliases?.[name] && !set.icons[name]) name = set.aliases[name].parent;
    const ic = set.icons[name]; if (!ic) throw new Error('no icon '+m[1]+':'+m[2]);
    const w = ic.width ?? set.width ?? 24, h = ic.height ?? set.height ?? 24;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${ic.left??0} ${ic.top??0} ${w} ${h}">${ic.body}</svg>`;
    await route.fulfill({status:200, contentType:'image/svg+xml', headers:{'access-control-allow-origin':'*'}, body: svg});
  } catch (e) { console.log('[icon]', e.message); await route.fulfill({status:404, headers:{'access-control-allow-origin':'*'}, body:''}); }
});
await page.addInitScript(() => { for (const k of ['showOpenFilePicker','showSaveFilePicker']) Object.defineProperty(window,k,{configurable:true,value:undefined}); });
await page.goto(origin+'/app');
await page.getByTestId('modeler-ready').waitFor({state:'attached',timeout:60000});
await page.getByTestId('open-file-input').setInputFiles({name:'figure.studyflow.yaml',mimeType:'text/yaml',buffer:readFileSync(input)});
await page.locator('.sf-shape').first().waitFor({timeout:30000});
await page.waitForTimeout(1500);
// A kept notice (reader warnings) would sit over the toolbar and swallow the clicks below.
for (const b of await page.getByRole('button', { name: 'Dismiss' }).all()) await b.click().catch(() => {});
async function exportAs(format){
  await page.getByRole('button',{name:'Open command palette'}).click();
  await page.getByRole('dialog').getByText('Save As...',{exact:true}).click();
  await page.getByTestId('save-dialog').waitFor();
  await page.getByTestId('export-format').selectOption(format);
  const dl = page.waitForEvent('download',{timeout:60000});
  await page.getByTestId('save-submit').click();
  return readFileSync(await (await dl).path());
}
const svg = exportAs('svg').then(b=>b.toString('utf8'));
const svgText = await svg;
const svgPath = '/tmp/render_export.svg'; // the PNG is the deposited figure; the SVG is only its raster source
writeFileSync(svgPath, svgText);
writeFileSync('/tmp/render_raster.png', withPrintSize(await rasterize(browser, svgText)));
execFileSync('node', [cli, 'convert', '--into', '/tmp/render_raster.png', input, outPath], { stdio: 'inherit' });
console.log('wrote', outPath);
await browser.close(); child?.kill(); process.exit(0);
