/* Run: node tests/site_delivery.spec.cjs
 * Builds an isolated committed fixture and mocks GitHub raw responses with CORS.
 * No network requests or changes to repository artwork are needed.
 */
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const { spawnSync } = require('node:child_process');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '..');
const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'gallery-delivery-'));
const fixture = path.join(temporary, 'repository');
const dist = path.join(fixture, 'dist');
const limit = 256 * 1024;
const largePath = 'assets/fixture/large (original).svg';
const smallPath = 'assets/fixture/small.svg';
const boundaryPath = 'assets/fixture/boundary.svg';
const pngPath = 'assets/ppt-png/fixture/large.png';
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const encodePath = value => value.split('/').map(encodeURIComponent).join('/');
const encodeDocPath = value => encodePath(value).replace(/[!'()*]/g, char => '%' + char.charCodeAt(0).toString(16).toUpperCase());
const types = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png' };

function write(relative, bytes) {
  const filename = path.join(fixture, relative);
  fs.mkdirSync(path.dirname(filename), { recursive: true });
  fs.writeFileSync(filename, bytes);
}
function git(...args) {
  const result = spawnSync('git', ['-C', fixture, ...args], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout.trim();
}
function pythonCall(functionName, args) {
  const code = `import runpy, sys; m=runpy.run_path(sys.argv[1]); print(m[sys.argv[2]](*sys.argv[3:]))`;
  return spawnSync('python', ['-c', code, path.join(root, 'scripts/build_site.py'), functionName, ...args], { encoding: 'utf8' });
}
function svg(size) {
  const prefix = '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48"><rect width="48" height="48" fill="#137c72"/><!--';
  const suffix = '--></svg>';
  return Buffer.from(prefix + 'x'.repeat(size - prefix.length - suffix.length) + suffix);
}

let server;
let browser;
(async () => {
  try {
    fs.mkdirSync(fixture);
    for (const name of ['index.html', 'app.js', 'styles.css', '.nojekyll', 'LICENSE']) write(name, fs.readFileSync(path.join(root, name)));
    write(largePath, svg(limit + 1));
    write(smallPath, svg(180));
    write(boundaryPath, svg(limit));
    // PNG decoders preserve the original 1×1 pixel and ignore trailing padding.
    const png = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jCLkAAAAASUVORK5CYII=', 'base64');
    write(pngPath, Buffer.concat([png, Buffer.alloc(limit + 1 - png.length)]));
    write('assets/fixture/metadata.xml', 'x'.repeat(limit + 1));
    write('licenses/fixture.txt', 'License evidence must remain local.');
    write('downloads/ppt-illustrations.pptx', Buffer.from('PK fixture presentation bytes'));
    const largeLink = encodePath(largePath);
    write('README.md', `[large](${largeLink})\n[small](${smallPath})\n`);
    write('docs/GUIDE.md', `[large](../${largeLink}?raw=true)\n<img src="../${largePath}">\n[small](../${smallPath})\n`);
    const assets = [[largePath, 'large'], [smallPath, 'small'], [boundaryPath, 'boundary']].map(([assetPath, id]) => ({
      id, path: assetPath, name: id, category: 'biomedical', subcategory: 'fixture', source: 'fixture', format: 'svg',
      author: 'Fixture author', author_url: 'https://example.org/', license: 'CC-BY-4.0', license_url: 'https://creativecommons.org/licenses/by/4.0/',
      source_url: 'https://example.org/illustration', attribution: `${id} — Fixture author. CC-BY-4.0.`, tags: [],
      bytes: fs.statSync(path.join(fixture, assetPath)).size, sha256: hash(fs.readFileSync(path.join(fixture, assetPath))),
      ...(id === 'large' ? { ppt_png_path: pngPath, ppt_png_width: 1, ppt_png_height: 1 } : {})
    }));
    const catalog = {
      generated_at: '2026-11-04T00:00:00Z', assets,
      sources: [{ id: 'fixture', name: 'Fixture', count: assets.length, kind: 'specialist', homepage: 'https://example.org/', license: 'CC-BY-4.0' }],
      categories: [{ id: 'biomedical', name: '生物医学', count: assets.length }]
    };
    write('data/catalog.json', JSON.stringify(catalog, null, 2));
    git('init', '--quiet');
    git('add', '.');
    git('-c', 'user.name=Delivery Fixture', '-c', 'user.email=fixture@example.org', 'commit', '--quiet', '-m', 'Committed delivery fixture');
    git('remote', 'add', 'origin', 'https://fixture-user:fixture-password@github.com/fixture-owner/fixture-repo.git');
    const commit = git('rev-parse', 'HEAD');
    const base = `https://raw.githubusercontent.com/fixture-owner/fixture-repo/${commit}/`;
    const before = new Map(['data/catalog.json', largePath, pngPath, 'README.md', 'docs/GUIDE.md'].map(relative => [relative, hash(fs.readFileSync(path.join(fixture, relative)))]));
    const build = pythonCall('build_site', [fixture, dist]);
    assert.equal(build.status, 0, build.stderr);
    assert.ok(!build.stdout.includes('fixture-password'), 'Build output never exposes remote credentials');
    const built = JSON.parse(fs.readFileSync(path.join(dist, 'data/catalog.json'), 'utf8'));
    assert.deepEqual(built.delivery, { base_url: base, external_paths: [largePath, pngPath] });
    assert.deepEqual(built.assets, catalog.assets, 'Delivery does not alter artwork metadata');
    for (const relative of [largePath, pngPath]) assert.equal(fs.existsSync(path.join(dist, relative)), false, 'Large image is omitted only from the artifact');
    for (const relative of [smallPath, boundaryPath, 'assets/fixture/metadata.xml', 'licenses/fixture.txt', 'downloads/ppt-illustrations.pptx']) {
      assert.deepEqual(fs.readFileSync(path.join(dist, relative)), fs.readFileSync(path.join(fixture, relative)), `${relative} stays local and byte-identical`);
    }
    for (const [relative, sha] of before) assert.equal(hash(fs.readFileSync(path.join(fixture, relative))), sha, 'Original files and source catalog remain unchanged');
    const guide = fs.readFileSync(path.join(dist, 'docs/GUIDE.md'), 'utf8');
    assert.ok(guide.includes(`[large](${base}${encodeDocPath(largePath)}?raw=true)`));
    assert.ok(guide.includes(`<img src="${base}${encodeDocPath(largePath)}">`));
    assert.ok(guide.includes(`[small](../${smallPath})`));
    assert.ok(fs.readFileSync(path.join(dist, 'README.md'), 'utf8').includes(`[large](${base}${encodeDocPath(largePath)})`));
    write('assets/fixture/uncommitted.svg', svg(200));
    const uncommitted = pythonCall('build_site', [fixture, dist]);
    assert.notEqual(uncommitted.status, 0, 'Uncommitted images cannot produce URLs pinned to a commit without those files');
    assert.match(uncommitted.stderr, /Commit image additions/);
    fs.unlinkSync(path.join(fixture, 'assets/fixture/uncommitted.svg'));
    assert.deepEqual(JSON.parse(fs.readFileSync(path.join(dist, 'data/catalog.json'), 'utf8')), built, 'Failed rebuild keeps the previous valid artifact');

    for (const remote of ['git@github.com:fixture-owner/fixture-repo.git', 'ssh://git@github.com/fixture-owner/fixture-repo.git']) {
      git('remote', 'set-url', 'origin', remote);
      const result = pythonCall('github_delivery_base', [fixture]);
      assert.equal(result.status, 0, result.stderr);
      assert.equal(result.stdout.trim(), base);
    }
    git('remote', 'set-url', 'origin', 'https://github.com.evil.invalid/fixture-owner/fixture-repo.git');
    assert.notEqual(pythonCall('github_delivery_base', [fixture]).status, 0, 'Non-GitHub origin is rejected');

    server = http.createServer((request, response) => {
      try {
        const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
        const filename = path.resolve(dist, '.' + (pathname === '/' ? '/index.html' : pathname));
        if (!filename.startsWith(dist + path.sep) || !fs.statSync(filename).isFile()) throw new Error('Invalid file');
        response.writeHead(200, { 'Content-Type': types[path.extname(filename)] || 'application/octet-stream' });
        fs.createReadStream(filename).pipe(response);
      } catch { response.writeHead(404); response.end('Not found'); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const site = `http://127.0.0.1:${server.address().port}/`;
    browser = await chromium.launch({ headless: true, ...(fs.existsSync('/usr/bin/chromium') ? { executablePath: '/usr/bin/chromium' } : {}), args: ['--no-sandbox'] });
    const context = await browser.newContext({ acceptDownloads: true });
    const page = await context.newPage();
    const errors = [];
    const rawRequests = [];
    let failDownload = false;
    let servedCatalog = built;
    page.on('pageerror', error => errors.push(error.message));
    await page.route('**/data/catalog.json', route => route.fulfill({ json: servedCatalog }));
    await page.route('https://raw.githubusercontent.com/**', route => {
      const request = route.request();
      assert.ok(request.url().startsWith(base), 'Only the pinned own-repository base is requested');
      const relative = decodeURIComponent(request.url().slice(base.length));
      assert.ok(built.delivery.external_paths.includes(relative), 'Only explicit external paths are requested');
      rawRequests.push({ relative, type: request.resourceType() });
      if (failDownload && request.resourceType() === 'fetch') return route.fulfill({ status: 503, headers: { 'Access-Control-Allow-Origin': '*' }, body: 'Unavailable' });
      return route.fulfill({ headers: { 'Content-Type': types[path.extname(relative)], 'Access-Control-Allow-Origin': '*' }, body: fs.readFileSync(path.join(fixture, relative)) });
    });
    await page.goto(site);
    await page.waitForSelector('.asset-card');
    const large = page.locator('[data-asset-id="large"]');
    assert.equal(await large.locator('img').getAttribute('src'), base + largeLink, 'Large preview uses the pinned URL');
    await large.locator('img').evaluate(image => image.decode());
    assert.equal(await page.locator('[data-asset-id="small"] img').getAttribute('src'), smallPath, 'Unlisted assets remain local');
    assert.equal(await page.locator('[data-asset-id="boundary"] img').getAttribute('src'), boundaryPath, 'Exactly 256 KiB remains local');
    await large.click();
    for (const [selector, relative] of [['#download-asset', largePath], ['#download-ppt-png', pngPath]]) {
      const ready = page.waitForEvent('download');
      await page.locator(selector).click();
      const downloaded = await ready;
      assert.equal(downloaded.suggestedFilename(), path.basename(relative), 'Cross-origin download preserves its original filename');
      assert.deepEqual(fs.readFileSync(await downloaded.path()), fs.readFileSync(path.join(fixture, relative)), 'Cross-origin Blob download preserves original bytes');
      assert.ok(rawRequests.some(item => item.relative === relative && item.type === 'fetch'), 'Download fetched through CORS');
    }
    const unchangedUrl = page.url();
    failDownload = true;
    await page.locator('#download-asset').click();
    await page.waitForFunction(() => document.getElementById('download-status').textContent.includes('暂时无法下载'));
    assert.equal(page.url(), unchangedUrl, 'Failed downloads keep the gallery open');
    assert.equal(await page.locator('#download-status a').getAttribute('href'), base + largeLink);
    assert.equal(await page.locator('#download-status a').getAttribute('target'), '_blank', 'Fallback requires an explicit click in another tab');
    failDownload = false;
    await page.keyboard.press('Escape');
    await page.locator('[data-asset-id="small"]').click();
    const localReady = page.waitForEvent('download');
    await page.locator('#download-asset').click();
    assert.deepEqual(fs.readFileSync(await (await localReady).path()), fs.readFileSync(path.join(fixture, smallPath)), 'Local downloads remain byte-identical');

    const invalidBases = [
      'https://evil.invalid/fixture-owner/fixture-repo/' + commit + '/',
      'https://raw.githubusercontent.com.evil.invalid/fixture-owner/fixture-repo/' + commit + '/',
      'https://user:password@raw.githubusercontent.com/fixture-owner/fixture-repo/' + commit + '/',
      'https://raw.githubusercontent.com/fixture-owner/fixture-repo/main/',
      'https://raw.githubusercontent.com/fixture-owner/../' + commit + '/'
    ];
    for (const invalid of invalidBases) {
      servedCatalog = { ...built, delivery: { ...built.delivery, base_url: invalid } };
      await page.goto(site);
      await page.waitForSelector('.asset-card');
      assert.equal(await page.locator('[data-asset-id="large"] img').getAttribute('src'), largeLink, 'Invalid delivery bases cannot select remote URLs');
    }
    servedCatalog = { ...built, delivery: { ...built.delivery, external_paths: [...built.delivery.external_paths, 'assets/../outside.svg'] }, assets: [{ ...built.assets[0], id: 'unsafe', path: 'assets/../outside.svg', ppt_png_path: null }] };
    await page.goto(site);
    await page.waitForSelector('.asset-card');
    assert.equal(await page.locator('.asset-card img').getAttribute('src'), '', 'Traversal remains blocked even when explicitly listed');
    assert.deepEqual(errors, [], 'No JavaScript page errors');
    console.log('PASS: isolated build preserves source bytes, pins credential-free GitHub URLs, omits only large images, retains metadata/PPTX, rewrites copied docs, validates delivery, downloads original SVG/PNG bytes through CORS, and offers a safe failure link.');
  } finally {
    if (browser) await browser.close();
    if (server) await new Promise(resolve => server.close(resolve));
    fs.rmSync(temporary, { recursive: true, force: true });
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
