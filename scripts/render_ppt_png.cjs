#!/usr/bin/env node
/* Faithful, offline SVG -> PNG rendering for PowerPoint.
 * Originals are never rewritten. Requires the repository's pinned Playwright.
 * Default: node scripts/render_ppt_png.cjs
 * Input: data/ppt-selection.json { long_edge: 2400, asset_ids: ["..."] }
 * Smoke: node scripts/render_ppt_png.cjs --ids ID1,ID2 --output-root /tmp/ppt-smoke
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const zlib = require('node:zlib');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const RENDER_VERSION = 'svg-ppt-png-v1';
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const readJSON = filename => JSON.parse(fs.readFileSync(filename, 'utf8'));

function argumentsFrom(argv) {
  const options = { selection: path.join(ROOT, 'data/ppt-selection.json'), catalog: path.join(ROOT, 'data/catalog.json'), outputRoot: ROOT, workers: 2, timeout: 60000, force: false };
  for (let n = 0; n < argv.length; n++) {
    const key = argv[n];
    if (key === '--force') { options.force = true; continue; }
    if (key === '--help') {
      console.log('Usage: node scripts/render_ppt_png.cjs [--selection FILE] [--ids ID,ID] [--long-edge 2400] [--workers 2] [--timeout 60000] [--output-root DIR] [--manifest FILE] [--force]');
      process.exit(0);
    }
    if (!['--selection', '--catalog', '--ids', '--long-edge', '--workers', '--timeout', '--output-root', '--manifest'].includes(key) || !argv[n + 1]) throw new Error(`Unknown or incomplete argument: ${key}`);
    const value = argv[++n];
    if (key === '--ids') options.ids = value.split(',').map(id => id.trim()).filter(Boolean);
    else if (key === '--long-edge') options.longEdge = Number(value);
    else if (key === '--workers') options.workers = Number(value);
    else if (key === '--timeout') options.timeout = Number(value);
    else if (key === '--output-root') options.outputRoot = path.resolve(value);
    else options[key.slice(2)] = path.resolve(value);
  }
  options.manifest ||= path.join(options.outputRoot, 'data/ppt-renders.json');
  if (!Number.isInteger(options.workers) || options.workers < 1 || options.workers > 3) throw new Error('--workers must be 1, 2 or 3');
  if (!Number.isInteger(options.timeout) || options.timeout < 5000 || options.timeout > 180000) throw new Error('--timeout must be between 5000 and 180000 ms');
  return options;
}

function atomicJSON(filename, value) {
  fs.mkdirSync(path.dirname(filename), { recursive: true });
  const temporary = `${filename}.tmp`;
  fs.writeFileSync(temporary, JSON.stringify(value, null, 2) + '\n');
  fs.renameSync(temporary, filename);
}

function pngDimensions(bytes) {
  if (bytes.length < 24 || !bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) throw new Error('Renderer output is not a PNG');
  return { width: bytes.readUInt32BE(16), height: bytes.readUInt32BE(20) };
}

// Recompress the original PNG scanlines without changing any pixel or metadata.
// Chromium favors encoding speed; level-9 IDAT is usually smaller for flat art.
const CRC_TABLE = Array.from({ length: 256 }, (_, value) => {
  for (let bit = 0; bit < 8; bit++) value = (value & 1) ? 0xedb88320 ^ (value >>> 1) : value >>> 1;
  return value >>> 0;
});
function pngChunk(type, data) {
  const typed = Buffer.concat([Buffer.from(type, 'ascii'), data]);
  let crc = 0xffffffff;
  for (const byte of typed) crc = CRC_TABLE[(crc ^ byte) & 255] ^ (crc >>> 8);
  const result = Buffer.alloc(data.length + 12);
  result.writeUInt32BE(data.length, 0); typed.copy(result, 4); result.writeUInt32BE((crc ^ 0xffffffff) >>> 0, result.length - 4);
  return result;
}
function losslessCompressPNG(bytes) {
  pngDimensions(bytes);
  const chunks = [], idat = [];
  for (let offset = 8; offset < bytes.length;) {
    const length = bytes.readUInt32BE(offset), end = offset + length + 12;
    if (end > bytes.length) throw new Error('Truncated PNG chunk');
    const type = bytes.toString('ascii', offset + 4, offset + 8);
    chunks.push({ type, raw: bytes.subarray(offset, end) });
    if (type === 'IDAT') idat.push(bytes.subarray(offset + 8, offset + 8 + length));
    offset = end;
  }
  const scanlines = zlib.inflateSync(Buffer.concat(idat));
  const compressed = zlib.deflateSync(scanlines, { level: 9 });
  const parts = [bytes.subarray(0, 8)]; let inserted = false;
  for (const chunk of chunks) {
    if (chunk.type === 'IDAT') {
      if (!inserted) { parts.push(pngChunk('IDAT', compressed)); inserted = true; }
    } else parts.push(chunk.raw);
  }
  const result = Buffer.concat(parts);
  return result.length < bytes.length ? result : bytes;
}

async function main() {
  const options = argumentsFrom(process.argv.slice(2));
  const selection = fs.existsSync(options.selection) ? readJSON(options.selection) : {};
  const longEdge = options.longEdge || selection.long_edge || 2400;
  if (!Number.isInteger(longEdge) || longEdge < 256 || longEdge > 4096) throw new Error('long_edge must be an integer from 256 to 4096');
  const ids = [...new Set(options.ids || selection.asset_ids || [])];
  if (!ids.length) throw new Error('No selection: provide data/ppt-selection.json or --ids ID,ID');
  const catalog = readJSON(options.catalog), byID = new Map(catalog.assets.map(asset => [asset.id, asset]));
  const assets = ids.map(id => {
    const asset = byID.get(id);
    if (!asset) throw new Error(`Selected asset missing from catalog: ${id}`);
    if (!/^[a-zA-Z0-9_-]+$/.test(id) || !/^[a-zA-Z0-9_-]+$/.test(asset.category) || !/^[a-zA-Z0-9_-]+$/.test(asset.source)) throw new Error(`Unsafe asset identifier: ${id}`);
    const file = fs.realpathSync(path.resolve(ROOT, asset.path));
    if (!file.startsWith(path.join(ROOT, 'assets') + path.sep) || path.extname(file).toLowerCase() !== '.svg') throw new Error(`Selected source is not a local SVG: ${id}`);
    if (sha256(fs.readFileSync(file)) !== asset.sha256) throw new Error(`Source hash differs from catalog: ${id}`);
    return { ...asset, originalFile: file };
  });
  const allowed = new Map(assets.map(asset => [asset.id, asset]));
  const existing = fs.existsSync(options.manifest) ? readJSON(options.manifest) : {};
  const records = existing.renders || existing;
  const saveRecords = () => atomicJSON(options.manifest, { long_edge: longEdge, renders: Object.fromEntries(Object.entries(records).sort(([a], [b]) => a.localeCompare(b))) });
  const failures = [], blocked = new WeakMap(); let rendered = 0, reused = 0, cursor = 0;
  const server = http.createServer((request, response) => {
    try {
      const match = /^\/svg\/([a-zA-Z0-9_-]+)$/.exec(new URL(request.url, 'http://127.0.0.1').pathname);
      const asset = match && allowed.get(match[1]);
      if (!asset || !['GET', 'HEAD'].includes(request.method)) { response.writeHead(404); response.end(); return; }
      response.writeHead(200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-store',
        'Content-Security-Policy': "default-src 'none'; script-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; sandbox",
        'X-Content-Type-Options': 'nosniff'
      });
      if (request.method === 'HEAD') response.end(); else fs.createReadStream(asset.originalFile).pipe(response);
    } catch { response.writeHead(500); response.end(); }
  });
  let browser;
  try {
    await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
    const origin = `http://127.0.0.1:${server.address().port}`;
    browser = await chromium.launch({ headless: true, ...(fs.existsSync('/usr/bin/chromium') ? { executablePath: '/usr/bin/chromium' } : {}), args: ['--no-sandbox', '--disable-background-networking'] });
    async function worker() {
      const context = await browser.newContext({ viewport: { width: 1280, height: 1280 }, deviceScaleFactor: 1, javaScriptEnabled: false, serviceWorkers: 'block', colorScheme: 'light', reducedMotion: 'reduce', locale: 'en-US', timezoneId: 'UTC' });
      await context.route('**/*', route => {
        const url = route.request().url(), page = route.request().frame().page();
        if (url.startsWith(`${origin}/svg/`) || url.startsWith('data:')) return route.continue();
        if (!blocked.has(page)) blocked.set(page, []);
        blocked.get(page).push(url);
        return route.abort('blockedbyclient');
      });
      try {
        while (cursor < assets.length) {
          const asset = assets[cursor++], previous = records[asset.id];
          const relative = path.posix.join('assets', 'ppt-png', asset.category, asset.source, `${asset.id}.png`);
          const output = path.join(options.outputRoot, ...relative.split('/'));
          if (!options.force && previous?.source_sha256 === asset.sha256 && previous?.render_version === RENDER_VERSION && previous?.long_edge === longEdge && previous?.png_path === relative && fs.existsSync(output)) {
            const bytes = fs.readFileSync(output), size = pngDimensions(bytes);
            if (sha256(bytes) === previous.sha256 && bytes.length === previous.bytes && size.width === previous.width && size.height === previous.height) {
              reused++; console.log(`CACHED ${asset.id} ${size.width}x${size.height}`); continue;
            }
          }
          let page, timer;
          try {
            page = await context.newPage(); page.setDefaultTimeout(options.timeout);
            const render = async () => {
              await page.goto(`${origin}/svg/${asset.id}`, { waitUntil: 'load', timeout: options.timeout });
              const natural = await page.evaluate(() => {
                const svg = document.documentElement;
                if (svg.localName !== 'svg') throw new Error('Source did not load as SVG');
                const vb = svg.viewBox?.baseVal;
                if (vb && vb.width > 0 && vb.height > 0) return { width: vb.width, height: vb.height, viewBox: true };
                const w = svg.width?.baseVal, h = svg.height?.baseVal;
                if (!w || !h || w.unitType === 2 || h.unitType === 2 || w.value <= 0 || h.value <= 0) throw new Error('SVG has no usable viewBox or fixed intrinsic dimensions');
                return { width: w.value, height: h.value, viewBox: false };
              });
              const ratio = natural.width / natural.height;
              if (!Number.isFinite(ratio) || ratio < 1 / 40 || ratio > 40) throw new Error(`Extreme or invalid aspect ratio ${ratio}`);
              const width = Math.max(1, Math.round(longEdge * natural.width / Math.max(natural.width, natural.height)));
              const height = Math.max(1, Math.round(longEdge * natural.height / Math.max(natural.width, natural.height)));
              await page.setViewportSize({ width, height });
              await page.evaluate(({ natural, width, height }) => {
                const svg = document.documentElement;
                if (!natural.viewBox) svg.setAttribute('viewBox', `0 0 ${natural.width} ${natural.height}`);
                svg.setAttribute('width', String(width)); svg.setAttribute('height', String(height));
                svg.style.setProperty('width', `${width}px`, 'important'); svg.style.setProperty('height', `${height}px`, 'important');
                svg.style.setProperty('display', 'block'); svg.style.setProperty('margin', '0');
              }, { natural, width, height });
              await page.evaluate(async () => { if (document.fonts) await document.fonts.ready; });
              // Source JavaScript is disabled, so page-scheduled RAF callbacks do not
              // run. A short host-side paint allowance also covers foreignObject text.
              await page.waitForTimeout(100);
              const bytes = losslessCompressPNG(await page.screenshot({ type: 'png', omitBackground: true, animations: 'disabled', clip: { x: 0, y: 0, width, height }, timeout: options.timeout }));
              if (blocked.get(page)?.length) throw new Error(`External or unsupported resources were blocked: ${blocked.get(page).length}`);
              const actual = pngDimensions(bytes);
              if (actual.width !== width || actual.height !== height) throw new Error('PNG dimensions differ from requested viewport');
              fs.mkdirSync(path.dirname(output), { recursive: true });
              fs.writeFileSync(`${output}.tmp`, bytes); fs.renameSync(`${output}.tmp`, output);
              records[asset.id] = { png_path: relative, width, height, sha256: sha256(bytes), bytes: bytes.length, source_sha256: asset.sha256, long_edge: longEdge, render_version: RENDER_VERSION };
              saveRecords();
              rendered++;
              console.log(`RENDERED ${asset.id} ${width}x${height} ${bytes.length} bytes${bytes.length > 6 * 1024 * 1024 ? ' (over 6 MiB; original resolution retained)' : ''}`);
            };
            await Promise.race([render(), new Promise((_, reject) => { timer = setTimeout(() => reject(new Error(`Render exceeded ${options.timeout} ms`)), options.timeout); })]);
          } catch (error) {
            const failure = { id: asset.id, path: asset.path, source_sha256: asset.sha256, reason: error.message };
            failures.push(failure); console.error(`FAILED ${asset.id}: ${error.message}`);
          } finally { clearTimeout(timer); if (page) await page.close().catch(() => {}); }
        }
      } finally { await context.close(); }
    }
    await Promise.all(Array.from({ length: options.workers }, () => worker()));
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
  atomicJSON(path.join(path.dirname(options.manifest), 'ppt-render-failures.json'), failures);
  console.log(`PNG rendering: ${rendered} generated, ${reused} verified cached, ${failures.length} failed, ${assets.length} selected. Originals unchanged.`);
  if (failures.length) process.exitCode = 1;
}

main().catch(error => { console.error(error.stack || error.message); process.exitCode = 1; });
