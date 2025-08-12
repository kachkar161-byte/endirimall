(function(){
  const input = document.getElementById('searchInput');
  const resultsBox = document.getElementById('searchResults');
  const pathParts = window.location.pathname.split('/');
  let lang = pathParts[1];
  if (!['az','en','ru'].includes(lang)) lang = '';
  const prefix = lang ? `/${lang}` : '';

  function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  if (!input || !resultsBox) return;

  let timer = null;

  function clearResults() {
    resultsBox.innerHTML = '';
    resultsBox.style.display = 'none';
  }

  function renderResults(items) {
    if (!items || items.length === 0) {
      clearResults();
      return;
    }
    const html = items.map(item => `
      <a class="list-group-item list-group-item-action d-flex align-items-center" href="${item.url}">
        ${item.image ? `<img src="${item.image}" alt="" class="me-2 rounded" style="width:40px;height:40px;object-fit:cover;">` : ''}
        <div class="flex-fill">
          <div class="fw-semibold text-truncate">${item.name}</div>
          <div class="small text-muted text-truncate">${item.store}${item.category ? ' · ' + item.category : ''}</div>
        </div>
        <span class="badge text-bg-success ms-2">-${item.discount}%</span>
      </a>
    `).join('');
    resultsBox.innerHTML = `<div class="list-group">${html}</div>`;
    resultsBox.style.display = 'block';
  }

  async function search(q) {
    try {
      const url = `${prefix}/deals/search/?q=${encodeURIComponent(q)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Network error');
      const data = await res.json();
      renderResults(data.results);
    } catch (e) {
      clearResults();
    }
  }

  input.addEventListener('input', () => {
    const q = input.value.trim();
    if (timer) clearTimeout(timer);
    if (!q) { clearResults(); return; }
    timer = setTimeout(() => search(q), 250);
  });

  document.addEventListener('click', (e) => {
    if (!resultsBox.contains(e.target) && e.target !== input) {
      clearResults();
    }
  });

  window.toggleFav = async function(event, productId) {
    event.preventDefault();
    const form = event.target.closest('form');
    const csrf = getCookie('csrftoken');
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf },
      });
      if (!res.ok) throw new Error('Failed');
      const data = await res.json();
      const badge = document.querySelector('.badge.text-bg-primary');
      if (badge) { badge.innerHTML = `<i class="bi bi-heart-fill"></i> ${data.favorite_count}`; }
      const btnIcon = form.querySelector('i');
      if (btnIcon) { btnIcon.className = data.status === 'added' ? 'bi bi-heart-fill' : 'bi bi-heart'; }
    } catch (e) {}
  }

  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.favorite-toggle');
    if (!btn) return;
    e.preventDefault();
    const productId = btn.getAttribute('data-product-id');
    const csrf = getCookie('csrftoken');
    try {
      const res = await fetch(`${prefix}/deals/fav/${productId}/toggle/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrf },
      });
      const data = await res.json();
      const icon = btn.querySelector('i');
      if (icon) icon.className = data.status === 'added' ? 'bi bi-heart-fill text-danger' : 'bi bi-heart';
      const badge = document.querySelector('.badge.text-bg-primary');
      if (badge) { badge.innerHTML = `<i class="bi bi-heart-fill"></i> ${data.favorite_count}`; }
    } catch (e) {
      // If user is not authenticated, redirect to login with language prefix
      window.location.href = `${prefix}/accounts/login/`;
    }
  });
})();