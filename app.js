'use strict';

(() => {
  const PAGE_SIZE = 60;
  const byId = id => document.getElementById(id);
  const state = { catalog: null, orderedAssets: [], category: '', query: '', source: '', license: '', format: '', page: 1, filtered: [] };
  const sources = new Map();
  const categories = new Map();
  let deliveryBase = '';
  const externalPaths = new Set();
  const elements = {
    grid: byId('asset-grid'), loading: byId('load-state'), count: byId('result-count'),
    search: byId('search'), source: byId('source-filter'), license: byId('license-filter'), format: byId('format-filter'),
    pagination: byId('pagination'), previous: byId('previous-page'), next: byId('next-page'),
    dialog: byId('asset-dialog')
  };

  const text = value => value == null ? '' : String(value);
  const normalize = value => text(value).normalize('NFKC').toLocaleLowerCase().replace(/[_-]+/g, ' ');
  const number = value => Number(value || 0).toLocaleString('zh-CN');
  const node = (tag, className, content) => {
    const result = document.createElement(tag);
    if (className) result.className = className;
    if (content != null) result.textContent = text(content);
    return result;
  };
  const safeRemote = value => {
    try {
      const url = new URL(text(value));
      return url.protocol === 'https:' || url.protocol === 'http:' ? url.href : '';
    } catch { return ''; }
  };
  const localAsset = value => {
    const path = text(value);
    if (!path.startsWith('assets/') || path.split('/').some(part => !part || part === '.' || part === '..') || /[\\\u0000-\u001f?#]/.test(path)) return '';
    return path.split('/').map(encodeURIComponent).join('/');
  };
  const configureDelivery = delivery => {
    deliveryBase = '';
    externalPaths.clear();
    const base = text(delivery?.base_url);
    const match = /^https:\/\/raw\.githubusercontent\.com\/([A-Za-z0-9][A-Za-z0-9-]*)\/([A-Za-z0-9_.-]+)\/[0-9a-f]{40}\/$/.exec(base);
    if (!match || ['.', '..'].includes(match[2]) || !Array.isArray(delivery.external_paths)) return;
    deliveryBase = base;
    delivery.external_paths.forEach(path => { if (typeof path === 'string' && localAsset(path)) externalPaths.add(path); });
  };
  const safeAsset = value => {
    const encoded = localAsset(value);
    return encoded && deliveryBase && externalPaths.has(value) ? deliveryBase + encoded : encoded;
  };
  const downloadStatus = node('p', 'copy-status');
  downloadStatus.id = 'download-status';
  downloadStatus.setAttribute('role', 'status');
  downloadStatus.hidden = true;
  byId('download-asset').parentElement.after(downloadStatus);

  async function downloadExternal(event) {
    const anchor = event.currentTarget;
    const href = anchor.getAttribute('href') || '';
    const filename = anchor.download;
    if (!deliveryBase || !href.startsWith(deliveryBase)) return;
    event.preventDefault();
    if (anchor.getAttribute('aria-busy') === 'true') return;
    anchor.setAttribute('aria-busy', 'true');
    downloadStatus.hidden = false;
    downloadStatus.textContent = '正在准备下载…';
    try {
      const response = await fetch(href, { mode: 'cors', credentials: 'omit', redirect: 'error' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const download = document.createElement('a');
      download.href = url;
      download.download = filename;
      download.hidden = true;
      document.body.append(download);
      download.click();
      download.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      downloadStatus.textContent = '下载已开始。';
    } catch {
      downloadStatus.replaceChildren(document.createTextNode('暂时无法下载。可打开原图后另存为：'), link('打开原图 ↗', href));
    } finally {
      anchor.removeAttribute('aria-busy');
    }
  }
  const originalFormat = asset => text(asset.path).split('.').pop().toUpperCase();
  const hasPptPng = asset => Boolean(safeAsset(asset.ppt_png_path));
  const hasNativeDimensions = asset => Number(asset.pixel_width) > 0 && Number(asset.pixel_height) > 0;
  const isNativeBitmap = asset => ['PNG', 'JPG', 'JPEG'].includes(originalFormat(asset));
  const isNativeOriginal = asset => isNativeBitmap(asset) && hasNativeDimensions(asset);
  const isHighresNative = asset => isNativeOriginal(asset) && Math.max(Number(asset.pixel_width), Number(asset.pixel_height)) >= 1600;
  const matchesFormat = asset => !state.format || (state.format === 'svg' && originalFormat(asset) === 'SVG') || (state.format === 'ppt-png' && hasPptPng(asset)) || (state.format === 'highres-native' && isHighresNative(asset)) || (state.format === 'bitmap-native' && isNativeOriginal(asset));
  const previewPath = asset => safeAsset(asset.preview_path) || (asset.requires_png_fallback ? safeAsset(asset.ppt_png_path) : '') || safeAsset(asset.path);
  function roundRobin(items, key) {
    const buckets = new Map();
    items.forEach(asset => {
      const group = key(asset);
      if (!buckets.has(group)) buckets.set(group, []);
      buckets.get(group).push(asset);
    });
    const values = [...buckets.values()];
    const longest = Math.max(0, ...values.map(bucket => bucket.length));
    const ordered = [];
    for (let index = 0; index < longest; index++) {
      values.forEach(bucket => { if (bucket[index]) ordered.push(bucket[index]); });
    }
    return ordered;
  }
  function link(label, href) {
    const url = safeRemote(href);
    if (!url) return node('span', '', label);
    const anchor = node('a', '', label);
    anchor.href = url;
    anchor.target = '_blank';
    anchor.rel = 'noopener noreferrer';
    return anchor;
  }
  function option(value, label) {
    const element = node('option', '', label);
    element.value = value;
    return element;
  }
  function sourceName(id) { return sources.get(id)?.name || id; }
  function categoryName(id) { return categories.get(id)?.name || id; }

  function initialize(catalog) {
    if (!catalog || !Array.isArray(catalog.assets) || !Array.isArray(catalog.sources) || !Array.isArray(catalog.categories)) throw new Error('目录格式不正确');
    state.catalog = catalog;
    configureDelivery(catalog.delivery);
    catalog.sources.forEach(source => sources.set(source.id, source));
    catalog.categories.forEach(category => categories.set(category.id, category));
    byId('asset-total').textContent = number(catalog.assets.length);
    byId('source-total').textContent = number(catalog.sources.length);
    byId('category-total').textContent = number(catalog.categories.length);
    const date = new Date(catalog.generated_at);
    byId('updated-at').textContent = Number.isNaN(date.getTime()) ? '' : `目录更新于 ${date.toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' })}`;
    catalog.sources.forEach(source => elements.source.append(option(source.id, `${source.name} (${number(source.count)})`)));
    [...new Set(catalog.assets.map(asset => asset.license))].sort().forEach(license => elements.license.append(option(license, license)));
    const tabs = byId('category-tabs');
    catalog.categories.forEach(category => {
      const button = node('button', 'category-tab', category.name);
      button.type = 'button';
      button.dataset.category = category.id;
      button.setAttribute('aria-pressed', 'false');
      button.append(node('span', 'category-count', number(category.count)));
      tabs.append(button);
    });
    catalog.assets.forEach(asset => {
      asset._search = normalize([asset.name, asset.author, asset.subcategory, asset.license, asset.collection, sourceName(asset.source), categoryName(asset.category), originalFormat(asset), hasPptPng(asset) ? 'ppt png 高清 演示' : '', isNativeOriginal(asset) ? '原始位图 原图 PowerPoint' : '', isHighresNative(asset) ? '高清' : isNativeOriginal(asset) ? '标准分辨率 小幅图示' : '', ...(Array.isArray(asset.tags) ? asset.tags : [])].join(' '));
    });
    // Lead with presentation-ready illustrations, then established biomedical art.
    const ppt = catalog.assets.filter(hasPptPng);
    const native = catalog.assets.filter(asset => isHighresNative(asset) && !hasPptPng(asset));
    const ready = [...native, ...ppt];
    const readySet = new Set(ready);
    const standard = catalog.assets.filter(asset => isNativeOriginal(asset) && !readySet.has(asset));
    const standardSet = new Set(standard);
    const featured = catalog.assets.filter(asset => !readySet.has(asset) && !standardSet.has(asset) && /servier|dbcls|swissbiopics/i.test(`${asset.author} ${asset.author_url} ${asset.source}`));
    const readyOrder = roundRobin(ready, asset => `${asset.category}:${asset.source}`);
    const standardOrder = roundRobin(standard, asset => `${asset.category}:${asset.source}`);
    const illustrationOrder = [];
    // Mix one standard-resolution original after two presentation-ready images.
    // This exposes the broader science collection without replacing HD with upscales.
    for (let index = 0; index < Math.max(Math.ceil(readyOrder.length / 2), standardOrder.length); index++) {
      illustrationOrder.push(...readyOrder.slice(index * 2, index * 2 + 2));
      if (standardOrder[index]) illustrationOrder.push(standardOrder[index]);
    }
    const prioritized = new Set([...ready, ...standard, ...featured]);
    state.orderedAssets = [
      ...illustrationOrder,
      ...roundRobin(featured, asset => asset.author),
      ...roundRobin(catalog.assets.filter(asset => !prioritized.has(asset)), asset => asset.source)
    ];
    elements.format.querySelector('[value="ppt-png"]').textContent = `PPT 高清 PNG (${number(ppt.length)})`;
    elements.format.querySelector('[value="highres-native"]').textContent = `高清原图 PNG/JPG (${number(catalog.assets.filter(isHighresNative).length)})`;
    elements.format.querySelector('[value="bitmap-native"]').textContent = `原始位图 PNG/JPG（全部） (${number(catalog.assets.filter(isNativeOriginal).length)})`;
    renderSources();
    restoreFilters();
    filterAssets();
  }

  function restoreFilters() {
    const params = new URLSearchParams(location.search);
    state.query = params.get('q') || '';
    state.category = categories.has(params.get('category')) ? params.get('category') : '';
    state.source = sources.has(params.get('source')) ? params.get('source') : '';
    const license = params.get('license') || '';
    state.license = [...elements.license.options].some(item => item.value === license) ? license : '';
    state.format = ['svg', 'ppt-png', 'highres-native', 'bitmap-native'].includes(params.get('format')) ? params.get('format') : '';
    elements.search.value = state.query;
    elements.source.value = state.source;
    elements.license.value = state.license;
    elements.format.value = state.format;
  }

  function filterAssets() {
    const terms = normalize(state.query).trim().split(/\s+/).filter(Boolean);
    state.filtered = state.orderedAssets.filter(asset =>
      (!state.category || asset.category === state.category) &&
      (!state.source || asset.source === state.source) &&
      (!state.license || asset.license === state.license) &&
      matchesFormat(asset) &&
      terms.every(term => asset._search.includes(term))
    );
    state.page = 1;
    document.querySelectorAll('.category-tab').forEach(button => {
      const active = button.dataset.category === state.category;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    const params = new URLSearchParams();
    if (state.query) params.set('q', state.query);
    if (state.category) params.set('category', state.category);
    if (state.source) params.set('source', state.source);
    if (state.license) params.set('license', state.license);
    if (state.format) params.set('format', state.format);
    try { history.replaceState(null, '', `${location.pathname}${params.size ? '?' + params : ''}${location.hash}`); } catch { /* File previews can deny history updates. */ }
    renderAssets();
  }

  function renderAssets() {
    const total = state.filtered.length;
    const pageCount = Math.max(1, Math.ceil(total / PAGE_SIZE));
    elements.count.textContent = `找到 ${number(total)} 张素材${total !== state.catalog.assets.length ? ` · 全库 ${number(state.catalog.assets.length)} 张` : ''}`;
    elements.grid.replaceChildren();
    elements.loading.hidden = total > 0;
    if (!total) {
      elements.loading.replaceChildren(node('span', 'error-symbol', '⌕'), node('p', '', '暂时没有匹配的素材。试试英文名称、近义词，或减少筛选条件。'));
      const reset = node('button', 'secondary-button', '清除筛选');
      reset.type = 'button';
      reset.addEventListener('click', resetFilters);
      elements.loading.append(reset);
    }
    const fragment = document.createDocumentFragment();
    state.filtered.slice((state.page - 1) * PAGE_SIZE, state.page * PAGE_SIZE).forEach(asset => {
      const card = node('button', 'asset-card');
      card.type = 'button';
      card.dataset.assetId = text(asset.id);
      card.setAttribute('aria-label', `${asset.name}，${sourceName(asset.source)}，查看详情`);
      const preview = node('span', 'card-preview');
      const image = document.createElement('img');
      image.src = previewPath(asset);
      image.alt = text(asset.name).replace(/_/g, ' ');
      image.loading = 'lazy';
      image.decoding = 'async';
      image.addEventListener('error', () => { image.hidden = true; preview.append(node('span', 'muted', '预览不可用')); }, { once: true });
      preview.append(image);
      const info = node('span', 'card-info');
      info.append(node('span', 'card-title', text(asset.name).replace(/_/g, ' ')), node('span', 'card-source', sourceName(asset.source)));
      const bottom = node('span', 'card-bottom');
      const type = node('span', hasPptPng(asset) || isHighresNative(asset) ? 'card-type card-type-ppt' : 'card-type', hasPptPng(asset) ? `PNG + ${originalFormat(asset)}` : isHighresNative(asset) ? `高清 ${originalFormat(asset)}` : isNativeOriginal(asset) ? `${originalFormat(asset)} 原图` : originalFormat(asset));
      if (isNativeOriginal(asset)) type.title = `${number(asset.pixel_width)} × ${number(asset.pixel_height)} px`;
      bottom.append(node('span', 'card-license', asset.license), type);
      info.append(bottom);
      card.append(preview, info);
      card.addEventListener('click', () => showDetail(asset));
      fragment.append(card);
    });
    elements.grid.append(fragment);
    elements.pagination.hidden = total <= PAGE_SIZE;
    elements.previous.disabled = state.page <= 1;
    elements.next.disabled = state.page >= pageCount;
    byId('page-status').textContent = `${state.page} / ${number(pageCount)}`;
  }

  function renderSources() {
    const fragment = document.createDocumentFragment();
    state.catalog.sources.forEach(source => {
      const card = node('article', 'source-card');
      const heading = node('div', 'source-card-heading');
      const title = node('h3');
      title.append(link(source.name, source.homepage || source.repository));
      heading.append(title);
      if (source.kind === 'specialist' || source.kind === 'supporting') {
        heading.append(node('span', `source-kind source-kind-${source.kind}`, source.kind === 'specialist' ? '科研专题库' : '通用绘图符号'));
      }
      card.append(heading, node('p', '', source.description));
      const bottom = node('div', 'source-card-bottom');
      bottom.append(node('span', '', `${number(source.count)} 张素材 · ${source.license || '逐图授权'}`));
      const browse = node('button', 'text-button', '浏览此来源 →');
      browse.type = 'button';
      browse.addEventListener('click', () => {
        state.source = source.id;
        state.category = '';
        state.query = '';
        state.license = '';
        state.format = '';
        elements.source.value = state.source;
        elements.search.value = '';
        elements.license.value = '';
        elements.format.value = '';
        filterAssets();
        byId('gallery').scrollIntoView({ block: 'start' });
      });
      bottom.append(browse);
      card.append(bottom);
      fragment.append(card);
    });
    byId('source-grid').replaceChildren(fragment);
  }

  function showDetail(asset) {
    const source = sources.get(asset.source) || {};
    byId('detail-title').textContent = text(asset.name).replace(/_/g, ' ');
    byId('detail-category').textContent = categoryName(asset.category);
    byId('detail-subcategory').textContent = asset.subcategory || '';
    byId('detail-image').src = previewPath(asset);
    byId('detail-image').alt = text(asset.name);
    byId('detail-author').replaceChildren(link(asset.author || '详见来源', asset.author_url));
    byId('detail-source').replaceChildren(link(source.name || asset.source, source.homepage || source.repository));
    byId('detail-license').replaceChildren(link(asset.license || '详见来源', asset.license_url));
    const pngAvailable = hasPptPng(asset);
    byId('detail-original-row').hidden = !isNativeBitmap(asset) || !hasNativeDimensions(asset);
    byId('detail-original-size').textContent = hasNativeDimensions(asset) ? `${number(asset.pixel_width)} × ${number(asset.pixel_height)} px · ${originalFormat(asset)}` : '';
    byId('detail-png-row').hidden = !pngAvailable;
    const dimensions = Number(asset.ppt_png_width) > 0 && Number(asset.ppt_png_height) > 0;
    byId('detail-png-size').textContent = pngAvailable && dimensions ? `${number(asset.ppt_png_width)} × ${number(asset.ppt_png_height)} px` : '详见下载文件';
    const previewNote = byId('preview-note');
    previewNote.hidden = !asset.requires_png_fallback;
    previewNote.textContent = asset.requires_png_fallback ? '这张 SVG 含复杂文字排版，部分演示软件可能无法完整显示。请在 PowerPoint 中使用配套高清 PNG，以保留文字和标注。' : '';
    byId('detail-format-note').textContent = isNativeBitmap(asset)
      ? `PNG/JPG 原图可直接插入 PowerPoint。它是位图图片，不能拆分为 SVG 矢量路径。${isHighresNative(asset) ? '放大后的细节取决于原始像素。' : '适合小幅图示，建议按原始尺寸使用，避免过度放大。'}`
      : '高清 PNG 可直接插入 PowerPoint；SVG 可保持矢量缩放，是否能拆分编辑取决于图形与软件版本。';
    const license = text(asset.license).toUpperCase();
    byId('license-note').textContent = license.includes('SA')
      ? '需署名：保留作者、来源和许可证链接；修改时注明修改。改编素材还需遵守相同方式共享（ShareAlike）要求。'
      : license.includes('CC0') || license.includes('CC-0') || license.includes('PUBLIC DOMAIN')
        ? '该记录标记为公共领域或 CC0；通常无需署名，仍建议在科研作品中保留来源。具体范围以链接中的原始条款为准。'
        : license.includes('MIT') || license.includes('APACHE') || license.includes('BSD')
          ? '请保留相应版权声明和许可证文本，并遵守原始许可证的其他条件。署名文本不能代替需要保留的许可文件。'
          : '需按该素材的具体许可证使用。CC BY 通常要求保留作者、来源和许可证链接，并注明是否修改；请阅读原始条款。';
    byId('attribution').value = asset.attribution || `${asset.name} — ${asset.author || source.name || asset.source}. ${asset.source_url || source.homepage || ''}. ${asset.license || ''} ${asset.license_url || ''}`;
    byId('copy-status').textContent = '';
    downloadStatus.hidden = true;
    downloadStatus.replaceChildren();
    const download = byId('download-asset');
    download.href = safeAsset(asset.path);
    download.download = text(asset.path).split('/').pop();
    download.textContent = `下载 ${originalFormat(asset)} 原图 ↓`;
    const pngDownload = byId('download-ppt-png');
    pngDownload.hidden = !pngAvailable;
    if (pngAvailable) {
      pngDownload.href = safeAsset(asset.ppt_png_path);
      pngDownload.download = text(asset.ppt_png_path).split('/').pop();
    } else {
      pngDownload.removeAttribute('href');
      pngDownload.removeAttribute('download');
    }
    const original = byId('original-source');
    const upstream = safeRemote(asset.source_url || source.repository || source.homepage);
    original.hidden = !upstream;
    if (upstream) original.href = upstream;
    elements.dialog.showModal();
  }

  function resetFilters() {
    if (!state.catalog) return;
    Object.assign(state, { query: '', source: '', license: '', category: '', format: '' });
    elements.search.value = '';
    elements.source.value = '';
    elements.license.value = '';
    elements.format.value = '';
    filterAssets();
  }
  function changePage(direction) {
    state.page += direction;
    renderAssets();
    byId('category-tabs').scrollIntoView({ block: 'start' });
    elements.count.focus({ preventScroll: true });
  }

  let debounce;
  elements.search.addEventListener('input', () => {
    clearTimeout(debounce);
    debounce = setTimeout(() => { if (state.catalog) { state.query = elements.search.value; filterAssets(); } }, 140);
  });
  byId('filter-form').addEventListener('submit', event => { event.preventDefault(); clearTimeout(debounce); if (state.catalog) { state.query = elements.search.value; filterAssets(); } });
  elements.source.addEventListener('change', () => { if (state.catalog) { state.source = elements.source.value; filterAssets(); } });
  elements.license.addEventListener('change', () => { if (state.catalog) { state.license = elements.license.value; filterAssets(); } });
  elements.format.addEventListener('change', () => { if (state.catalog) { state.format = elements.format.value; filterAssets(); } });
  byId('category-tabs').addEventListener('click', event => { const button = event.target.closest('[data-category]'); if (button && state.catalog) { state.category = button.dataset.category; filterAssets(); } });
  byId('reset-filters').addEventListener('click', resetFilters);
  elements.previous.addEventListener('click', () => changePage(-1));
  elements.next.addEventListener('click', () => changePage(1));
  byId('close-dialog').addEventListener('click', () => elements.dialog.close());
  byId('download-asset').addEventListener('click', downloadExternal);
  byId('download-ppt-png').addEventListener('click', downloadExternal);
  elements.dialog.addEventListener('click', event => { if (event.target === elements.dialog) { const rect = elements.dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) elements.dialog.close(); } });
  document.addEventListener('keydown', event => { if (event.key === '/' && !event.ctrlKey && !event.metaKey && !event.altKey && !elements.dialog.open && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) { event.preventDefault(); elements.search.focus(); } });
  byId('copy-attribution').addEventListener('click', async () => {
    const attribution = byId('attribution');
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(attribution.value);
      byId('copy-status').textContent = '署名文本已复制。';
    } catch {
      attribution.focus();
      attribution.select();
      byId('copy-status').textContent = '浏览器未开放剪贴板权限，已选中文本；请按 Ctrl/Cmd + C 复制。';
    }
  });
  elements.count.tabIndex = -1;
  fetch('data/catalog.json').then(response => { if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); }).then(initialize).catch(error => {
    elements.count.textContent = '素材目录加载失败';
    elements.loading.hidden = false;
    elements.loading.replaceChildren(node('span', 'error-symbol', '!'), node('p', '', '暂时无法读取素材目录。请通过 HTTP 服务或 GitHub Pages 打开本站，再刷新重试。'));
    const anchor = node('a', '', '查看项目说明 →');
    anchor.href = 'README.md';
    elements.loading.append(anchor);
    console.error('Catalog loading failed:', error);
  });
})();
