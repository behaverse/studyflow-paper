import { chromium } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
// usage: node views.mjs <in.studyflow.yaml> <outDir>
// Captures the reference modeler's own renderings of the study's Gantt, Checklist and Provenance views, each
// cropped to its content (no dialog chrome), at 6x: view-gantt.png (the chart), view-checklist-<n>.png (one
// per element carrying a checklist) and view-provenance.png (the log, or the dialog's own empty-state line
// when the file carries no run records). compose_views.py lays out whatever is written here.
const origin = 'http://127.0.0.1:4175';
const [input, outDir] = process.argv.slice(2);
async function up(){ try { return (await fetch(origin+'/app')).ok } catch { return false } }
let child;
if (!(await up())) {
  child = spawn('npm',['run','dev','-w','@behaverse/studyflow-modeler','--','--host','127.0.0.1','--port','4175'],{stdio:'ignore'});
  const t=Date.now()+120000; while(Date.now()<t && !(await up())) await new Promise(r=>setTimeout(r,500));
}
const browser = await chromium.launch().catch(() => chromium.launch({ channel: 'chrome' }));
const page = await browser.newPage({ viewport:{width:1000, height:1400}, deviceScaleFactor: 6 });
page.on('pageerror', e => console.log('[pageerror]', e.message));
await page.addInitScript(() => { for (const k of ['showOpenFilePicker','showSaveFilePicker']) Object.defineProperty(window,k,{configurable:true,value:undefined}); });
await page.goto(origin+'/app');
await page.getByTestId('modeler-ready').waitFor({state:'attached',timeout:60000});
await page.getByTestId('open-file-input').setInputFiles({name:'figure.studyflow.yaml',mimeType:'text/yaml',buffer:readFileSync(input)});
await page.locator('.sf-shape').first().waitFor({timeout:30000});
await page.waitForTimeout(1500);
// A kept notice (reader warnings) would sit over the toolbar and swallow the clicks below.
for (const b of await page.getByRole('button', { name: 'Dismiss' }).all()) await b.click().catch(() => {});

async function open(command, width) {
  await page.setViewportSize({ width, height: 1400 });
  await page.getByRole('button',{name:'Open command palette'}).click();
  await page.getByRole('dialog').getByText(command,{exact:true}).click();
  await page.waitForTimeout(2000);
}
async function close() { await page.keyboard.press('Escape'); await page.waitForTimeout(500); }

// The Gantt chart is a little wider than the dialog's default width: let the dialog grow to it.
await open('View as Gantt...', 1000);
await page.evaluate(() => {
  const svg = document.querySelector('[role=dialog] svg[role=img]');
  const w = svg.getBoundingClientRect().width + 56;
  for (let el = svg.parentElement; el && el !== document.body; el = el.parentElement) {
    if (getComputedStyle(el).maxWidth !== 'none') { el.style.maxWidth = 'none'; el.style.width = `${w}px`; }
  }
});
await page.waitForTimeout(500);
await page.locator('[role=dialog] svg[role=img]').first().screenshot({ path: `${outDir}/view-gantt.png` });
await close();

// One card per element carrying a checklist, at the narrow width the composite gives them.
await open('View as Checklist...', 640);
const cards = page.locator('[role=dialog] li:has(h4)');
const n = await cards.count();
for (let i = 0; i < n; i++) await cards.nth(i).screenshot({ path: `${outDir}/view-checklist-${i + 1}.png` });
console.log('checklist cards', n);
await close();

// The log only exists once the file carries run records; the deposited plan has none and the dialog shows its
// empty-state line instead. Capture whichever is there, and leave the panel out if neither is.
await open('View Provenance...', 1000);
const log = page.getByTestId('provenance-log');
const shown = (await log.count()) ? log : page.locator('[role=dialog] p').last();
await shown.screenshot({ path: `${outDir}/view-provenance.png`, timeout: 10000 })
  .catch((e) => console.log('provenance: no panel —', e.message.split('\n')[0]));
await close();
await browser.close(); child?.kill(); process.exit(0);
