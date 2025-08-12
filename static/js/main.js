document.addEventListener('DOMContentLoaded', () => {
    /* Smart search */
    const searchInput = document.querySelector('#smartSearch');
    const resultsContainer = document.querySelector('#searchResults');

    if (searchInput) {
        let timeoutId;
        searchInput.addEventListener('keyup', (e) => {
            clearTimeout(timeoutId);
            const query = e.target.value;
            if (query.length < 2) {
                resultsContainer.innerHTML = '';
                return;
            }
            timeoutId = setTimeout(() => {
                fetch(`/search/?q=${encodeURIComponent(query)}`)
                    .then((res) => res.json())
                    .then((data) => {
                        resultsContainer.innerHTML = data.results.map(item =>
                            `<a href="${item.url}" class="list-group-item list-group-item-action">${item.name}</a>`
                        ).join('');
                    });
            }, 300);
        });
    }

    /* Toggle favorite */
    document.body.addEventListener('click', (e) => {
        if (e.target.closest('.toggle-favorite')) {
            const btn = e.target.closest('.toggle-favorite');
            const productId = btn.dataset.id;
            fetch('/favorite/toggle/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: new URLSearchParams({ product_id: productId })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'added') {
                        btn.querySelector('i').classList.remove('bi-heart');
                        btn.querySelector('i').classList.add('bi-heart-fill', 'text-danger');
                    } else {
                        btn.querySelector('i').classList.remove('bi-heart-fill', 'text-danger');
                        btn.querySelector('i').classList.add('bi-heart');
                    }
                });
        }
    });
});