
// Navigation mobile
const toggle = document.querySelector('.menu-toggle');
const nav    = document.querySelector('nav');
if (toggle) toggle.addEventListener('click', () => nav.classList.toggle('open'));

// Recherche dictionnaire
const searchInput = document.getElementById('dict-search');
const filterBtns  = document.querySelectorAll('.filter-btn');
const tableRows   = document.querySelectorAll('.dict-row');

function filterTable() {
  const q   = searchInput ? searchInput.value.toLowerCase() : '';
  const cat = document.querySelector('.filter-btn.active')?.dataset.cat || 'all';
  tableRows.forEach(row => {
    const text = row.textContent.toLowerCase();
    const rowCat = row.dataset.cat || '';
    const matchQ   = text.includes(q);
    const matchCat = cat === 'all' || rowCat === cat;
    row.style.display = (matchQ && matchCat) ? '' : 'none';
  });
}

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    filterTable();
  });
});
if (searchInput) searchInput.addEventListener('input', filterTable);
