/* Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations. */
document.addEventListener('DOMContentLoaded', async () => {
  const nav = document.getElementById('site-nav');
  if (!nav?.dataset.navigationSrc) return;
  try {
    const response = await fetch(nav.dataset.navigationSrc);
    if (!response.ok) throw new Error('Navigation unavailable');
    const markup = await response.text();
    // This is a same-origin, build-generated asset containing the original navigation tree.
    nav.innerHTML = markup;
    const current = location.pathname.replace(/index\.html$/, '').replace(/\/$/, '');
    for (const anchor of nav.querySelectorAll('a.nav-list-link[href], a.nav-category[href]')) {
      const path = new URL(anchor.href).pathname.replace(/index\.html$/, '').replace(/\/$/, '');
      if (path !== current) continue;
      anchor.setAttribute('aria-current', 'page');
      anchor.classList.add('active');
      let item = anchor.closest('li');
      while (item && nav.contains(item)) {
        item.classList.add('active');
        const expander = item.querySelector(':scope > .nav-list-expander');
        expander?.setAttribute('aria-expanded', 'true');
        item = item.parentElement?.closest('li');
      }
    }
    // The theme uses delegated expansion events on the existing nav element.
    nav.addEventListener('click', event => {
      const expander = event.target.closest('.nav-list-expander');
      if (!expander) return;
      requestAnimationFrame(() => expander.setAttribute('aria-expanded', String(expander.parentElement.classList.contains('active'))));
    });
    document.dispatchEvent(new CustomEvent('docs-navigation-ready'));
  } catch {
    const loading = nav.querySelector('[data-nav-loading]');
    if (loading) {
      loading.textContent = '文件導覽暫時無法載入。';
      const retry = document.createElement('button'); retry.type = 'button'; retry.textContent = '重新載入'; retry.addEventListener('click', () => location.reload()); loading.appendChild(retry);
      const fallback = document.createElement('a'); fallback.href = nav.dataset.navigationSrc; fallback.textContent = '開啟完整導覽'; loading.appendChild(fallback);
    }
  }
});
