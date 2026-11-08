// v4: every page must fit the screen (no scrolling) at common laptop sizes; real Kanda names; map + trace.
const { chromium } = require('playwright');
const path = require('path');
const DEVA = ['बालकाण्ड', 'अयोध्याकाण्ड', 'अरण्यकाण्ड', 'किष्किन्धाकाण्ड', 'सुन्दरकाण्ड', 'युद्धकाण्ड', 'उत्तरकाण्ड'];
(async () => {
  const [file, shots] = ['file://' + path.resolve(process.argv[2]), process.argv[3]];
  const browser = await chromium.launch();
  const errors = [];
  for (const [w, hgt] of [[1440, 900], [1280, 800], [1360, 545], [1100, 520]]) {
    const page = await browser.newPage({ viewport: { width: w, height: hgt }, deviceScaleFactor: 1 });
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(file);
    await page.waitForSelector('.book');
    let i = 0, kanda = 0, overflow = [];
    while (true) {
      if (await page.$('.error')) { errors.push('error page at ' + i); break; }
      const fits = await page.evaluate(() => { const s = document.querySelector('.scroll'); return s.scrollHeight <= s.clientHeight + 1 && document.documentElement.scrollHeight <= innerHeight + 1; });
      const cls = await page.$eval('.book', b => b.className);
      if (!fits) overflow.push(i + ':' + cls.replace('book ', ''));
      if (/page-kanda/.test(cls)) {
        const d = (await page.innerText('.deva-title')).trim();
        if (d !== DEVA[kanda]) errors.push(`kanda ${kanda + 1}: "${d}"`);
        kanda++;
      }
      if (w === 1440) await page.screenshot({ path: `${shots}/p${String(i).padStart(2, '0')}_${cls.replace('book page-', '')}.png` });
      const next = await page.$('.nav .arrow:last-child:not([disabled])');
      if (!next) break;
      await page.keyboard.press('ArrowRight'); i++;
      if (i > 60) { errors.push('runaway'); break; }
    }
    if (kanda !== 7) errors.push(`saw ${kanda} Kanda pages at ${w}x${hgt}`);
    if (overflow.length) errors.push(`${w}x${hgt} pages needing scroll: ${overflow.join(', ')}`);
    console.log(`${w}x${hgt}: ${i + 1} pages`);
    if (w === 1440) {
      await page.click('.segs li >> nth=1 >> button');            // Path of Rama
      await page.waitForSelector('.map .land');
      const legs = await page.$$eval('.map .leg', l => l.length);
      if (legs < 10) errors.push('map legs: ' + legs);
      await page.click('.stops li >> nth=6 >> button');           // Kishkindha
      if (!/Kishkindha/.test(await page.innerText('.stop-detail'))) errors.push('stop select failed');
      await page.screenshot({ path: `${shots}/path_selected.png` });
      await page.click('.trace'); await page.waitForTimeout(2000);
      await page.screenshot({ path: `${shots}/path_tracing.png` });
      await page.click('.trace');                                  // stop
    }
    await page.close();
  }
  const m = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await m.goto(file); await m.waitForSelector('.book'); await m.keyboard.press('ArrowRight'); await m.keyboard.press('ArrowRight'); await m.keyboard.press('ArrowRight');
  if (await m.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)) errors.push('horizontal overflow on phone');
  await m.screenshot({ path: `${shots}/mobile.png`, fullPage: true });
  await browser.close();
  console.log(errors.length ? 'ERRORS:\n' + errors.join('\n') : 'STORYBOOK OK');
  process.exit(errors.length ? 1 : 0);
})();
