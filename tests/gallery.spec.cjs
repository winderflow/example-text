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
const isNativeBitmap = asset => /\.(png|jpe?g)$/i.test(asset.path) && Number(asset.pixel_width) > 0 && Number(asset.pixel_height) > 0;
const isNativeHighres = asset => isNativeBitmap(asset) && Math.max(Number(asset.pixel_width), Number(asset.pixel_height)) >= 1600;
const types = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg' };

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
    console.log(`Asset preview rendering verified for ${tested.length} sources: ${tested.join(', ')}.`);
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

    const lgplAssets = catalog.assets.filter(item => item.license === 'LGPL-2.1-or-later');
    if (lgplAssets.length) {
      const item = lgplAssets[0];
      const params = new URLSearchParams({ q: item.name, source: item.source, license: item.license });
      await page.goto(url + '?' + params);
      const exact = page.locator(`[data-asset-id="${item.id}"]`);
      await exact.waitFor();
      await exact.click();
      await page.waitForSelector('dialog[open]');
      assert.equal(await page.locator('#detail-license').textContent(), item.license);
      const note = await page.locator('#license-note').textContent();
      assert.match(note, /LGPL/);
      assert.match(note, /SVG 源文件/);
      assert.match(note, /原版权声明/);
      assert.match(note, /2\.1/);
      assert.doesNotMatch(note, /CC BY 通常/, 'LGPL assets must show their own source and license requirements');
      assert.equal(await page.locator('#attribution').inputValue(), item.attribution);
      assert.equal(decodeURIComponent(new URL(await page.locator('#download-asset').getAttribute('href'), url).pathname).slice(1), item.path);
      const svgReady = page.waitForEvent('download');
      await page.locator('#download-asset').click();
      const svgDownload = await svgReady;
      const originalSvg = fs.readFileSync(await svgDownload.path());
      assert.equal(crypto.createHash('sha256').update(originalSvg).digest('hex'), item.sha256, 'LGPL SVG download retains its original copyright metadata and bytes');
      assert.deepEqual(originalSvg, fs.readFileSync(path.join(root, item.path)));
      await page.keyboard.press('Escape');
      await page.locator('#reset-filters').click();
      console.log(`LGPL source-file notice, attribution and original SVG download/hash verified (${lgplAssets.length} assets).`);
    }

    const pptAssets = catalog.assets.filter(item => item.ppt_png_path);
    await page.locator('#format-filter').selectOption('svg');
    assert.ok((await page.locator('.card-type').allTextContents()).every(value => value.includes('SVG')), 'SVG format filter only shows SVG originals');
    await page.locator('#reset-filters').click();
    await page.locator('#format-filter').selectOption('ppt-png');
    assert.match(new URL(page.url()).searchParams.get('format'), /^ppt-png$/);
    assert.equal(await page.locator('.asset-card').count(), Math.min(60, pptAssets.length));
    assert.ok((await page.locator('.card-type').allTextContents()).every(value => value.includes('PNG')), 'PPT filter requires actual PNG derivatives');
    if (pptAssets.length) {
      const samples = [pptAssets.find(item => !item.requires_png_fallback) || pptAssets[0]];
      const fallback = pptAssets.find(item => item.requires_png_fallback);
      if (fallback && fallback.id !== samples[0].id) samples.push(fallback);
      for (const item of samples) {
        const params = new URLSearchParams({ q: item.name, source: item.source, format: 'ppt-png' });
        await page.goto(url + '?' + params);
        // Asset ids avoid confusing similarly named variants when present on the first page.
        const exact = page.locator(`[data-asset-id="${item.id}"]`);
        await exact.waitFor();
        const preview = item.preview_path || (item.requires_png_fallback ? item.ppt_png_path : item.path);
        assert.equal(decodeURIComponent(new URL(await exact.locator('img').getAttribute('src'), url).pathname).slice(1), preview);
        await exact.locator('img').evaluate(image => image.decode());
        await exact.click();
        await page.waitForSelector('dialog[open]');
        assert.equal(decodeURIComponent(new URL(await page.locator('#download-asset').getAttribute('href'), url).pathname).slice(1), item.path, 'Original SVG link remains unchanged');
        assert.ok(await page.locator('#download-ppt-png').isVisible());
        assert.match(await page.locator('#detail-png-size').textContent(), new RegExp(Number(item.ppt_png_width).toLocaleString('zh-CN')));
        assert.equal(await page.locator('#preview-note').isVisible(), Boolean(item.requires_png_fallback));
        const pngReady = page.waitForEvent('download');
        await page.locator('#download-ppt-png').click();
        const pngDownload = await pngReady;
        const downloaded = fs.readFileSync(await pngDownload.path());
        const original = fs.readFileSync(path.join(root, item.ppt_png_path));
        assert.deepEqual(downloaded, original, 'PPT PNG download matches local derivative byte-for-byte');
        assert.equal(downloaded.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
        assert.equal(downloaded.readUInt32BE(16), item.ppt_png_width);
        assert.equal(downloaded.readUInt32BE(20), item.ppt_png_height);
        await page.keyboard.press('Escape');
      }
      console.log(`PPT PNG filter, original SVG links, PNG downloads/dimensions and foreignObject fallback verified (${pptAssets.length} derivatives).`);
    } else {
      console.log('PPT PNG filter correctly returns no results; derivative-specific checks not run (no derivatives in catalog).');
    }

    await page.locator('#reset-filters').click();
    const nativeAssets = catalog.assets.filter(isNativeHighres);
    await page.locator('#format-filter').selectOption('highres-native');
    assert.equal(new URL(page.url()).searchParams.get('format'), 'highres-native');
    assert.equal(await page.locator('.asset-card').count(), Math.min(60, nativeAssets.length));
    assert.ok((await page.locator('.card-type').allTextContents()).every(value => /^高清 (PNG|JPE?G)$/.test(value)), 'Native high-resolution filter requires actual PNG/JPEG originals');
    for (const id of await page.locator('.asset-card').evaluateAll(cards => cards.map(card => card.dataset.assetId))) {
      assert.ok(nativeAssets.some(item => item.id === id), 'HD results retain the 1600-pixel minimum long edge');
    }
    if (nativeAssets.length) {
      const samples = [...new Map([nativeAssets.find(item => /\.jpe?g$/i.test(item.path)), nativeAssets.find(item => /\.png$/i.test(item.path))].filter(Boolean).map(item => [item.id, item])).values()];
      for (const item of samples) {
        const params = new URLSearchParams({ q: item.name, source: item.source, format: 'highres-native' });
        await page.goto(url + '?' + params);
        const exact = page.locator(`[data-asset-id="${item.id}"]`);
        await exact.waitFor();
        await exact.locator('img').evaluate(image => image.decode());
        const size = await exact.locator('img').evaluate(image => [image.naturalWidth, image.naturalHeight].sort((a, b) => a - b));
        assert.deepEqual(size, [Number(item.pixel_width), Number(item.pixel_height)].sort((a, b) => a - b), 'Original image dimensions match recorded pixels');
        await exact.click();
        await page.waitForSelector('dialog[open]');
        assert.ok(await page.locator('#detail-original-row').isVisible());
        assert.match(await page.locator('#detail-original-size').textContent(), new RegExp(Number(item.pixel_width).toLocaleString('zh-CN')));
        assert.match(await page.locator('#download-asset').textContent(), /下载 (PNG|JPE?G) 原图/);
        assert.match(await page.locator('#detail-format-note').textContent(), /位图/);
        const ready = page.waitForEvent('download');
        await page.locator('#download-asset').click();
        const original = await ready;
        const downloaded = fs.readFileSync(await original.path());
        assert.equal(crypto.createHash('sha256').update(downloaded).digest('hex'), item.sha256, 'PNG/JPEG download preserves original file hash');
        await page.keyboard.press('Escape');
      }
      console.log(`Native high-resolution filter, image dimensions and PNG/JPEG original download SHA-256 verified (${nativeAssets.length} originals).`);
    } else {
      console.log('Native high-resolution filter correctly returns no results; bitmap-specific checks not run (no native originals in catalog).');
    }

    await page.locator('#reset-filters').click();
    const bitmapAssets = catalog.assets.filter(isNativeBitmap);
    const standardAssets = bitmapAssets.filter(item => !isNativeHighres(item));
    await page.locator('#format-filter').selectOption('bitmap-native');
    assert.equal(new URL(page.url()).searchParams.get('format'), 'bitmap-native');
    assert.match(await page.locator('#format-filter option[value="bitmap-native"]').textContent(), new RegExp(bitmapAssets.length.toLocaleString('zh-CN')));
    assert.equal(await page.locator('.asset-card').count(), Math.min(60, bitmapAssets.length));
    for (const card of await page.locator('.asset-card').all()) {
      const id = await card.getAttribute('data-asset-id');
      const item = bitmapAssets.find(asset => asset.id === id);
      assert.ok(item, 'All-original bitmap filter excludes SVGs and synthetic format variants');
      const badge = await card.locator('.card-type').textContent();
      if (!isNativeHighres(item)) {
        assert.doesNotMatch(badge, /高清/, 'Standard-resolution originals are never labeled HD');
        assert.match(badge, /^(PNG|JPE?G) 原图$/);
      }
    }
    if (standardAssets.length) {
      const samples = [...new Map([
        standardAssets.find(item => /\.jpe?g$/i.test(item.path)),
        standardAssets.find(item => /\.png$/i.test(item.path))
      ].filter(Boolean).map(item => [item.id, item])).values()];
      for (const item of samples) {
        const params = new URLSearchParams({ q: item.name, source: item.source, format: 'bitmap-native' });
        await page.goto(url + '?' + params);
        const exact = page.locator(`[data-asset-id="${item.id}"]`);
        await exact.waitFor();
        assert.doesNotMatch(await exact.locator('.card-type').textContent(), /高清/);
        await exact.locator('img').evaluate(image => image.decode());
        const actualSize = await exact.locator('img').evaluate(image => [image.naturalWidth, image.naturalHeight].sort((a, b) => a - b));
        assert.deepEqual(actualSize, [Number(item.pixel_width), Number(item.pixel_height)].sort((a, b) => a - b), 'Standard-original preview preserves native resolution');
        await exact.click();
        await page.waitForSelector('dialog[open]');
        assert.ok(await page.locator('#detail-original-row').isVisible());
        assert.match(await page.locator('#detail-original-size').textContent(), new RegExp(Number(item.pixel_width).toLocaleString('zh-CN')));
        assert.match(await page.locator('#detail-format-note').textContent(), /适合小幅图示/);
        assert.match(await page.locator('#detail-format-note').textContent(), /避免过度放大/);
        const ready = page.waitForEvent('download');
        await page.locator('#download-asset').click();
        const original = await ready;
        const downloaded = fs.readFileSync(await original.path());
        assert.equal(crypto.createHash('sha256').update(downloaded).digest('hex'), item.sha256, 'Standard-resolution original download preserves source bytes');
        await page.keyboard.press('Escape');
      }
      console.log(`All-native bitmap filter and honest standard-resolution labels/dimensions/downloads verified (${bitmapAssets.length} originals; ${standardAssets.length} standard-resolution).`);
    } else {
      console.log(`All-native bitmap filter verified (${bitmapAssets.length} originals); standard-resolution-specific checks not run (no standard originals yet).`);
    }

    await page.locator('#reset-filters').click();
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: '/tmp/science-gallery-real.png', fullPage: true });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: '/tmp/science-gallery-real-mobile.png', fullPage: true });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, 'Mobile layout does not overflow');
    assert.deepEqual(errors, [], 'No JavaScript page errors');
    console.log('PASS: Chinese keyword search, per-source previews, license/category/format filters, pagination, original-file download SHA-256, attribution, honest native image resolution, optional PPT PNGs, Escape, responsive layout, zero page errors.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
