import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { spawn, execFileSync } from 'node:child_process';
// usage: node render.mjs <in.studyflow.yaml> <out.studyflow.png> [scale]
const origin = 'http://127.0.0.1:4175';
const [input, outPath, scaleArg] = process.argv.slice(2);
const scale = Number(scaleArg ?? 4);
const cli = 'packages/cli/dist/studyflow.mjs';
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
// rasterize at `scale`
const p2 = await browser.newPage({ deviceScaleFactor: scale, viewport:{width:1600,height:1000} });
await p2.setContent(`<html><body style="margin:0;background:#fff">${svgText}</body></html>`);
await p2.waitForTimeout(500);
const el = p2.locator('svg').first();
const png = await el.screenshot({ type:'png', omitBackground:false });
writeFileSync('/tmp/render_raster.png', png);
execFileSync('node', [cli, 'convert', '--into', '/tmp/render_raster.png', input, outPath], { stdio: 'inherit' });
console.log('wrote', outPath);
await browser.close(); child?.kill(); process.exit(0);
