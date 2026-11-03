/* Run: node tests/gallery.spec.cjs
 * Requires Playwright with Chromium, or system Chromium at /usr/bin/chromium.
 * Runs an ephemeral loopback HTTP server; no external requests are needed.
 */
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const crypto = require('node:crypto');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const catalog = JSON.parse(fs.readFileSync(path.join(root, 'data/catalog.json'), 'utf8'));
const types = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml' };

const server = http.createServer((request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    const filename = path.resolve(root, '.' + (pathname === '/' ? '/index.html' : pathname));
    if (!filename.startsWith(root + path.sep)) throw new Error('Invalid path');
    if (!fs.statSync(filename).isFile()) throw new Error('Not a file');
    response.writeHead(200, { 'Content-Type': types[path.extname(filename)] || 'application/octet-stream' });
    fs.createReadStream(filename).pipe(response);
  } catch {
    response.writeHead(404);
    response.end('Not found');
  }
});

(async () => {
  let browser;
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const url = `http://127.0.0.1:${server.address().port}/`;
    browser = await chromium.launch({ headless: true, ...(fs.existsSync('/usr/bin/chromium') ? { executablePath: '/usr/bin/chromium' } : {}), args: ['--no-sandbox'] });
    const context = await browser.newContext({ viewport: { width: 1365, height: 1000 }, acceptDownloads: true });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const started = performance.now();
    await page.goto(url);
    await page.waitForSelector('.asset-card');
    const loadTime = performance.now() - started;
    assert.equal(await page.locator('.asset-card').count(), Math.min(60, catalog.assets.length));
    assert.match(await page.locator('#asset-total').textContent(), new RegExp(catalog.assets.length.toLocaleString('zh-CN')));
    assert.equal(await page.locator('.source-card').count(), catalog.sources.length);
    assert.equal(await page.locator('.source-kind-specialist').count(), catalog.sources.filter(source => source.kind === 'specialist').length);
    assert.equal(await page.locator('.source-kind-supporting').count(), catalog.sources.filter(source => source.kind === 'supporting').length);
    console.log(`Initial catalog rendered in ${Math.round(loadTime)} ms (${catalog.assets.length} assets; ${fs.statSync(path.join(root, 'data/catalog.json')).size} JSON bytes).`);

    for (const query of ['细胞', '显微镜', '电阻', '岩性', '地震']) {
      await page.locator('#search').fill(query);
      await page.waitForTimeout(240);
      const count = await page.locator('.asset-card').count();
      assert.ok(count > 0, `Chinese search should match ${query}`);
      console.log(`Chinese search ${query}: ${await page.locator('#result-count').textContent()}`);
    }
    await page.locator('#reset-filters').click();

    const tested = [];
    for (const source of catalog.sources) {
      await page.locator('#source-filter').selectOption(source.id);
      await page.waitForTimeout(80);
      assert.ok(await page.locator('.asset-card').count() > 0, `${source.id} has results`);
      const images = page.locator('.asset-card img');
      for (let index = 0; index < Math.min(2, await images.count()); index++) {
        await images.nth(index).scrollIntoViewIfNeeded();
        await images.nth(index).evaluate(image => image.decode());
        assert.ok(await images.nth(index).evaluate(image => image.naturalWidth > 0), `${source.id} image ${index} decodes`);
        if (['geologic-patterns', 'gissymbology', 'electrical-symbol-library', 'electricalsymbols'].includes(source.id)) {
          const visible = await images.nth(index).evaluate(image => {
            const canvas = document.createElement('canvas');
            canvas.width = canvas.height = 128;
            const context = canvas.getContext('2d');
            context.drawImage(image, 0, 0, 128, 128);
            const pixels = context.getImageData(0, 0, 128, 128).data;
            for (let p = 0; p < pixels.length; p += 4) {
              if (pixels[p + 3] > 20 && Math.min(pixels[p], pixels[p + 1], pixels[p + 2]) < 240) return true;
            }
            return false;
          });
          assert.ok(visible, `${source.id} preview contains visible nonwhite geometry`);
        }
      }
      tested.push(source.id);
    }
    console.log(`Original SVG rendering verified for ${tested.length} sources: ${tested.join(', ')}.`);
    await page.locator('#reset-filters').click();

    const license = catalog.assets[0].license;
    await page.locator('#license-filter').selectOption(license);
    assert.ok((await page.locator('.card-license').allTextContents()).every(value => value === license));
    await page.locator('#reset-filters').click();
    await page.locator('[data-category="chemistry"]').click();
    const chemistry = catalog.assets.filter(asset => asset.category === 'chemistry');
    assert.equal(await page.locator('.asset-card').count(), Math.min(60, chemistry.length));
    await page.locator('#reset-filters').click();
    await page.locator('#next-page').click();
    assert.match(await page.locator('#page-status').textContent(), /^2 \/ /);
    await page.locator('#previous-page').click();

    await page.locator('.asset-card').first().click();
    await page.waitForSelector('dialog[open]');
    const attribution = await page.locator('#attribution').inputValue();
    const asset = catalog.assets.find(item => item.attribution === attribution);
    assert.ok(asset, 'Displayed attribution comes from the original catalog record');
    assert.equal(await page.locator('#detail-license').textContent(), asset.license);
    const downloadReady = page.waitForEvent('download');
    await page.locator('#download-asset').click();
    const download = await downloadReady;
    const bytes = fs.readFileSync(await download.path());
    assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), asset.sha256, 'Downloaded file preserves original hash');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('dialog[open]').count(), 0);

    await page.locator('#reset-filters').click();
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: '/tmp/science-gallery-real.png', fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: '/tmp/science-gallery-real-mobile.png', fullPage: true });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, 'Mobile layout does not overflow');
    assert.deepEqual(errors, [], 'No JavaScript page errors');
    console.log('PASS: Chinese keyword search, per-source SVG rendering, license/category filters, pagination, original-file download SHA-256, attribution, Escape, responsive layout, zero page errors.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
