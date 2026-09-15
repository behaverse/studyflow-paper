import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { spawn, execFileSync } from 'node:child_process';
// usage: node views.mjs <in.studyflow.yaml> <outDir>
const origin = 'http://127.0.0.1:4175';
const [input, outDir] = process.argv.slice(2);
const cli = 'packages/cli/dist/studyflow.mjs';
async function up(){ try { return (await fetch(origin+'/app')).ok } catch { return false } }
let child;
if (!(await up())) {
  child = spawn('npm',['run','dev','-w','@behaverse/studyflow-modeler','--','--host','127.0.0.1','--port','4175'],{stdio:'ignore'});
  const t=Date.now()+120000; while(Date.now()<t && !(await up())) await new Promise(r=>setTimeout(r,500));
}
// Playwright's own Chromium when installed, else this machine's Chrome.
const browser = await chromium.launch().catch(() => chromium.launch({ channel: 'chrome' }));
const ctx = await browser.newContext({acceptDownloads:true, viewport:{width:1400,height:1000}, deviceScaleFactor: 3});
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

for (const [label, id, title] of [['gantt','View as Gantt...','Gantt View'],['checklist','View as Checklist...','Checklist View'],['provenance','View Provenance...','Provenance']]) {
  await page.getByRole('button',{name:'Open command palette'}).click();
  await page.keyboard.type(label);
  await page.waitForTimeout(300);
  await page.screenshot({path: `${outDir}/debug-${label}.png`});
  const items = await page.getByRole('dialog').innerText().catch(()=> 'no dialog');
  console.log('palette:', items.slice(0,300).replace(/\n/g,' | '));
  await page.keyboard.press('Enter');
  await page.waitForTimeout(1500);
  await page.waitForTimeout(1500);
  if (await page.getByText('Reset Zoom', {exact:true}).isVisible().catch(()=>false)) { await page.keyboard.press('Escape'); await page.waitForTimeout(800); }
  const box = await page.evaluate((title) => {
    const el = [...document.querySelectorAll('h1,h2,h3,div,span')].find(e => e.childElementCount === 0 && e.textContent.trim().startsWith(title));
    let n = el, best = null;
    while (n && n !== document.body) { const r = n.getBoundingClientRect(); if (r.width < innerWidth * 0.95 && r.height < innerHeight * 0.95 && r.width > 200) best = {x:r.x,y:r.y,width:r.width,height:r.height}; n = n.parentElement; }
    return best;
  }, title);
  console.log(label, JSON.stringify(box));
  await page.screenshot({ path: `${outDir}/view-${label}.png`, clip: box ?? undefined });
  console.log('dialogs:', await page.locator('[role=dialog]').count(), 'testids:', (await page.locator('[data-testid]').evaluateAll(els => els.map(e=>e.getAttribute('data-testid')).filter(t=>/dialog|gantt|check|prov/i.test(t)))).join(','));
  console.log('shot', label);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);
}
await browser.close(); child?.kill(); process.exit(0);
