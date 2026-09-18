import { chromium } from '@playwright/test';
import { readFileSync, writeFileSync } from 'node:fs';
import { spawn } from 'node:child_process';
import { crc32 } from 'node:zlib';
// usage (from the modeler checkout): node modeler.mjs <in.studyflow.yaml> <out.png>
// The annotated modeler screenshot of fig-s2-modeler: the Behaverse palette flyout and the inspector's
// Execution tab for a selected Behaverse task, both generated from the skills' schemas.
const origin = 'http://127.0.0.1:4175';
const [input, outPath] = process.argv.slice(2);
async function up(){ try { return (await fetch(origin+'/app')).ok } catch { return false } }
let child;
if (!(await up())) {
  child = spawn('npm',['run','dev','-w','@behaverse/studyflow-modeler','--','--host','127.0.0.1','--port','4175'],{stdio:'ignore'});
  const t=Date.now()+120000; while(Date.now()<t && !(await up())) await new Promise(r=>setTimeout(r,500));
}
const browser = await chromium.launch().catch(() => chromium.launch({ channel: 'chrome' }));
const page = await browser.newPage({ viewport:{width:1440,height:900}, deviceScaleFactor: 2 });
await page.addInitScript(() => { for (const k of ['showOpenFilePicker','showSaveFilePicker']) Object.defineProperty(window,k,{configurable:true,value:undefined}); });
await page.goto(origin+'/app');
await page.getByTestId('modeler-ready').waitFor({state:'attached',timeout:60000});
await page.getByTestId('open-file-input').setInputFiles({name:'study.studyflow.yaml',mimeType:'text/yaml',buffer:readFileSync(input)});
await page.locator('.sf-shape').first().waitFor({timeout:30000});
await page.waitForTimeout(800);
await page.locator('[data-element-id="Task_WorkingMemory"]').first().click();
await page.getByTestId('inspector-shell').getByText('Execution', { exact: true }).click();
await page.getByTestId('palette-root').getByRole('button', { name: /^Behaverse elements/ }).hover();
await page.waitForTimeout(600);
// Lettered callouts beside the three regions the caption names.
await page.evaluate(() => {
  const box = (sel) => document.querySelector(sel)?.getBoundingClientRect();
  // The smallest box holding the text: the flyout's heading, the inspector's last section.
  const byText = (re) => [...document.querySelectorAll('body *')].filter((el) => re.test(el.textContent ?? ''))
    .sort((x, y) => x.getBoundingClientRect().width * x.getBoundingClientRect().height - y.getBoundingClientRect().width * y.getBoundingClientRect().height)[0]?.getBoundingClientRect();
  const heading = byText(/^\s*Behaverse\s*$/i);
  const outputs = byText(/^\s*Outputs\s*$/);
  const regions = [
    ['a', 'Palette, from the schemas', heading && { right: heading.right + 150, top: heading.top - 12 }, 'right'],
    ['b', 'Inspector, from the schemas', outputs && { left: outputs.left, top: outputs.bottom + 28 }, 'at'],
    ['c', 'Canvas', box('[data-element-id="Task_Interference"]'), 'above'],
  ];
  for (const [letter, text, r, side] of regions) {
    if (!r) continue;
    const tag = document.createElement('div');
    tag.style.cssText = 'position:fixed;z-index:99999;display:flex;align-items:center;gap:6px;font:600 15px "IBM Plex Sans",sans-serif;color:#1c1917;background:#fef3c7;border:1.5px solid #1c1917;border-radius:999px;padding:3px 10px 3px 3px;box-shadow:0 1px 3px rgba(0,0,0,.2)';
    tag.innerHTML = `<span style="display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#1c1917;color:#fff">${letter}</span>${text}`;
    const at = side === 'right' ? { left: r.right + 10, top: r.top + 8 } : side === 'at' ? { left: r.left, top: r.top } : { left: r.left, top: r.top - 40 };
    tag.style.left = `${at.left}px`; tag.style.top = `${at.top}px`;
    document.body.append(tag);
  }
});
const shot = await page.screenshot();
// pHYs, so the screenshot prints 180 mm wide.
const phys = Buffer.alloc(21), ppm = Math.round(shot.readUInt32BE(16) / 0.180);
phys.writeUInt32BE(9, 0); phys.write('pHYs', 4, 'latin1'); phys.writeUInt32BE(ppm, 8); phys.writeUInt32BE(ppm, 12); phys[16] = 1;
phys.writeUInt32BE(crc32(phys.subarray(4, 17)), 17);
writeFileSync(outPath, Buffer.concat([shot.subarray(0, 33), phys, shot.subarray(33)]));
console.log('wrote', outPath);
await browser.close(); child?.kill(); process.exit(0);
