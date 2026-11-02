'use strict';

(() => {
  const PAGE_SIZE = 60;
  const byId = id => document.getElementById(id);
  const state = { catalog: null, orderedAssets: [], category: '', query: '', source: '', license: '', page: 1, filtered: [] };
  const sources = new Map();
  const categories = new Map();
  const elements = {
    grid: byId('asset-grid'), loading: byId('load-state'), count: byId('result-count'),
    search: byId('search'), source: byId('source-filter'), license: byId('license-filter'),
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
  const safeAsset = value => {
    const path = text(value);
    if (!path.startsWith('assets/') || path.split('/').some(part => part === '..') || /[\\\u0000-\u001f?#]/.test(path)) return '';
    return path.split('/').map(encodeURIComponent).join('/');
  };
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
      asset._search = normalize([asset.name, asset.author, asset.subcategory, asset.license, sourceName(asset.source), categoryName(asset.category), ...(Array.isArray(asset.tags) ? asset.tags : [])].join(' '));
    });
    // Round-robin sources so the opening page represents the collection's breadth.
    const buckets = new Map(catalog.sources.map(source => [source.id, []]));
    catalog.assets.forEach(asset => {
      if (!buckets.has(asset.source)) buckets.set(asset.source, []);
      buckets.get(asset.source).push(asset);
    });
    const sourceBuckets = [...buckets.values()];
    const longest = Math.max(0, ...sourceBuckets.map(bucket => bucket.length));
    for (let index = 0; index < longest; index++) {
      sourceBuckets.forEach(bucket => { if (bucket[index]) state.orderedAssets.push(bucket[index]); });
    }
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
    elements.search.value = state.query;
    elements.source.value = state.source;
    elements.license.value = state.license;
  }

  function filterAssets() {
    const terms = normalize(state.query).trim().split(/\s+/).filter(Boolean);
    state.filtered = state.orderedAssets.filter(asset =>
      (!state.category || asset.category === state.category) &&
      (!state.source || asset.source === state.source) &&
      (!state.license || asset.license === state.license) &&
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
      card.setAttribute('aria-label', `${asset.name}，${sourceName(asset.source)}，查看详情`);
      const preview = node('span', 'card-preview');
      const image = document.createElement('img');
      image.src = safeAsset(asset.path);
      image.alt = text(asset.name).replace(/_/g, ' ');
      image.loading = 'lazy';
      image.decoding = 'async';
      image.addEventListener('error', () => { image.hidden = true; preview.append(node('span', 'muted', '预览不可用')); }, { once: true });
      preview.append(image);
      const info = node('span', 'card-info');
      info.append(node('span', 'card-title', text(asset.name).replace(/_/g, ' ')), node('span', 'card-source', sourceName(asset.source)));
      const bottom = node('span', 'card-bottom');
      bottom.append(node('span', 'card-license', asset.license), node('span', 'card-type', text(asset.path).split('.').pop().toUpperCase()));
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
      const title = node('h3');
      title.append(link(source.name, source.homepage || source.repository));
      card.append(title, node('p', '', source.description));
      const bottom = node('div', 'source-card-bottom');
      bottom.append(node('span', '', `${number(source.count)} 张素材 · ${source.license || '逐图授权'}`));
      const browse = node('button', 'text-button', '浏览此来源 →');
      browse.type = 'button';
      browse.addEventListener('click', () => {
        state.source = source.id;
        state.category = '';
        state.query = '';
        state.license = '';
        elements.source.value = state.source;
        elements.search.value = '';
        elements.license.value = '';
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
    byId('detail-image').src = safeAsset(asset.path);
    byId('detail-image').alt = text(asset.name);
    byId('detail-author').replaceChildren(link(asset.author || '详见来源', asset.author_url));
    byId('detail-source').replaceChildren(link(source.name || asset.source, source.homepage || source.repository));
    byId('detail-license').replaceChildren(link(asset.license || '详见来源', asset.license_url));
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
    const download = byId('download-asset');
    download.href = safeAsset(asset.path);
    download.download = text(asset.path).split('/').pop();
    const original = byId('original-source');
    const upstream = safeRemote(asset.source_url || source.repository || source.homepage);
    original.hidden = !upstream;
    if (upstream) original.href = upstream;
    elements.dialog.showModal();
  }

  function resetFilters() {
    if (!state.catalog) return;
    Object.assign(state, { query: '', source: '', license: '', category: '' });
    elements.search.value = '';
    elements.source.value = '';
    elements.license.value = '';
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
  byId('category-tabs').addEventListener('click', event => { const button = event.target.closest('[data-category]'); if (button && state.catalog) { state.category = button.dataset.category; filterAssets(); } });
  byId('reset-filters').addEventListener('click', resetFilters);
  elements.previous.addEventListener('click', () => changePage(-1));
  elements.next.addEventListener('click', () => changePage(1));
  byId('close-dialog').addEventListener('click', () => elements.dialog.close());
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
