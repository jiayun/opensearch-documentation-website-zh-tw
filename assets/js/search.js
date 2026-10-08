/* Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations. */
(function () {
  'use strict';
  const defaultBase = '/opensearch-documentation-website-zh-tw/3.9';
  const base = typeof document === 'undefined' ? defaultBase : (document.querySelector('meta[name="docs-baseurl"]')?.content || defaultBase);
  let modulePromise;
  function loadPagefind() {
    if (!modulePromise) modulePromise = import(`${base}/pagefind/pagefind.js`).then(async engine => {
      await engine.options({ baseUrl: base + '/' });
      return engine;
    }).catch(error => { modulePromise = undefined; throw error; });
    return modulePromise;
  }
  function safeResultURL(value, origin = 'https://jiayun.github.io') {
    try {
      const url = new URL(value, origin + base + '/');
      return url.origin === origin && url.pathname.startsWith(base + '/') ? url.pathname + url.search + url.hash : null;
    } catch { return null; }
  }
  function createController({ load = loadPagefind, results, error, loading }) {
    let sequence = 0;
    return {
      cancel() { sequence++; loading?.(false); },
      async search(query, options = {}, limit = 20) {
        const current = ++sequence;
        query = query.trim();
        if (!query) { loading?.(false); results?.([], 0, query); return; }
        loading?.(true);
        try {
          const engine = await load();
          const response = await engine.search(query, options);
          const items = await Promise.all(response.results.slice(0, limit).map(item => item.data()));
          if (current === sequence) results?.(items, response.results.length, query);
        } catch (failure) {
          if (current === sequence) error?.(failure);
        } finally { if (current === sequence) loading?.(false); }
      }
    };
  }
  const api = { createController, safeResultURL };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document === 'undefined') return;

  function snippet(value) {
    const fragment = document.createDocumentFragment();
    const parsed = new DOMParser().parseFromString(String(value || ''), 'text/html');
    function append(source, target) {
      for (const node of source.childNodes) {
        if (node.nodeType === 3) target.appendChild(document.createTextNode(node.textContent));
        else if (node.nodeType === 1) {
          if (node.tagName === 'MARK') { const mark = document.createElement('mark'); append(node, mark); target.appendChild(mark); }
          else append(node, target);
        }
      }
    }
    append(parsed.body, fragment);
    return fragment;
  }
  function message(container, text) {
    const node = document.createElement('p'); node.className = 'search-page--results--no-results'; node.textContent = text; container.replaceChildren(node);
  }
  function render(container, items, dropdown) {
    const nodes = [];
    for (const item of items) {
      const href = safeResultURL(item.url, location.origin);
      if (!href) continue;
      const row = document.createElement(dropdown ? 'div' : 'article');
      row.className = dropdown ? 'top-banner-search--field-with-results--field--wrapper--search-component--search-results--result' : 'search-page--results--result';
      const anchor = document.createElement('a'); anchor.href = href; anchor.textContent = item.meta?.title || '文件';
      if (dropdown) row.appendChild(anchor);
      else { const heading = document.createElement('h3'); heading.appendChild(anchor); row.appendChild(heading); }
      const summary = document.createElement(dropdown ? 'span' : 'p'); summary.appendChild(snippet(item.excerpt)); row.appendChild(summary);
      nodes.push(row);
    }
    container.replaceChildren(...nodes);
    if (!nodes.length) message(container, '找不到符合的文件，請嘗試其他字詞。');
  }
  document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('search-input');
    const box = document.getElementById('search-results');
    const output = box?.querySelector('.top-banner-search--field-with-results--field--wrapper--search-component--search-results-wrapper');
    const spinner = document.querySelector('.top-banner-search--field-with-results--field--wrapper--search-component--search-spinner');
    if (input && box && output) {
      let composing = false, timer, selected = -1;
      const close = () => { clearTimeout(timer); controller.cancel(); document.documentElement.classList.remove('search-active'); input.setAttribute('aria-expanded', 'false'); selected = -1; };
      const open = () => { document.documentElement.classList.add('search-active'); input.setAttribute('aria-expanded', 'true'); };
      const controller = createController({
        results(items, total, query) { selected = -1; if (!query) { output.replaceChildren(); close(); return; } render(output, items, true); open(); },
        error() { message(output, '搜尋暫時無法使用，請稍後再試。'); open(); },
        loading(active) { spinner?.classList.toggle('spinning', active); }
      });
      input.setAttribute('aria-controls', 'search-results'); input.setAttribute('aria-expanded', 'false');
      const schedule = () => { clearTimeout(timer); controller.cancel(); if (!input.value.trim()) { close(); output.replaceChildren(); return; } timer = setTimeout(() => controller.search(input.value, {}, 5), 250); };
      input.addEventListener('compositionstart', () => { composing = true; clearTimeout(timer); controller.cancel(); });
      input.addEventListener('compositionend', () => { composing = false; schedule(); });
      input.addEventListener('input', event => { if (!composing && !event.isComposing) schedule(); });
      input.addEventListener('keydown', event => {
        if (composing || event.isComposing || event.keyCode === 229) return;
        const rows = [...output.querySelectorAll('a[href]')];
        if (event.key === 'Escape') { event.preventDefault(); close(); }
        else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
          event.preventDefault(); if (!rows.length) return;
          selected = (selected + (event.key === 'ArrowDown' ? 1 : -1) + rows.length) % rows.length;
          rows.forEach((anchor, index) => anchor.parentElement.classList.toggle('highlighted', index === selected));
          rows[selected].scrollIntoView({ block: 'nearest' });
        } else if (event.key === 'Enter') {
          event.preventDefault();
          location.href = rows[selected]?.href || `${base}/search.html?q=${encodeURIComponent(input.value.trim())}`;
        }
      });
      document.addEventListener('pointerdown', event => { if (!box.contains(event.target) && event.target !== input) close(); });
      input.addEventListener('focus', () => { if (output.childNodes.length && input.value.trim()) open(); });
    }

    const pageInput = document.getElementById('searchPageInput');
    const pageOutput = document.getElementById('searchPageResultsContainer');
    const heading = document.getElementById('searchPageResultsHeader');
    const section = document.getElementById('searchSection');
    if (pageInput && pageOutput && heading && section) {
      let pageLimit = 50;
      const more = document.getElementById('searchMore');
      const controller = createController({
        results(items, total, query) { heading.textContent = query ? `「${query}」的搜尋結果（共 ${total} 筆）` : '請輸入搜尋字詞。'; if (query) render(pageOutput, items, false); else pageOutput.replaceChildren(); if (more) more.hidden = !query || items.length >= total; },
        error() { heading.textContent = '搜尋暫時無法使用'; message(pageOutput, '請稍後再試。'); },
        loading(active) { pageOutput.setAttribute('aria-busy', String(active)); if (active) heading.textContent = '搜尋中…'; }
      });
      function readURL() {
        const params = new URLSearchParams(location.search); pageInput.value = params.get('q') || ''; section.value = params.get('section') || '';
        const filters = section.value ? { filters: { section: section.value } } : {};
        controller.search(pageInput.value, filters, pageLimit);
      }
      function submit() {
        pageLimit = 50;
        const url = new URL(location.href); const query = pageInput.value.trim();
        if (query) url.searchParams.set('q', query); else url.searchParams.delete('q');
        if (section.value) url.searchParams.set('section', section.value); else url.searchParams.delete('section');
        if (url.href !== location.href) history.pushState({}, '', url);
        readURL();
      }
      pageInput.addEventListener('keydown', event => { if (event.key === 'Enter' && !event.isComposing && event.keyCode !== 229) { event.preventDefault(); submit(); } });
      document.getElementById('searchSubmit')?.addEventListener('click', submit);
      more?.addEventListener('click', () => { pageLimit += 50; readURL(); });
      section.addEventListener('change', submit);
      window.addEventListener('popstate', () => { pageLimit = 50; readURL(); });
      loadPagefind().then(engine => engine.filters()).then(filters => {
        for (const name of Object.keys(filters.section || {}).sort()) { const option = document.createElement('option'); option.value = name; option.textContent = name; section.appendChild(option); }
        readURL();
      }).catch(() => { readURL(); });
    }
  });
}());
