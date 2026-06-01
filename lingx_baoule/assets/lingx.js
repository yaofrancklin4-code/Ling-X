
// ── LingX Engine (client-side NLP pour le baoulé/français) ──

const STOPWORDS_FR = new Set([
  'le','la','les','un','une','des','de','du','et','en','au','aux',
  'est','sont','a','il','elle','ils','elles','je','tu','nous','vous',
  'ce','se','sa','son','ses','si','ou','mais','donc','or','ni','car',
  'que','qui','dont','où','par','pour','sur','sous','avec','dans','sans',
  'plus','très','bien','tout','cette','ces','mon','ton','leur','leurs',
  'être','avoir','faire','dire','aller','voir','pouvoir','vouloir',
  'l'','d'','n'','s'','j'','c'',
]);

function tokenize(text) {
  return text.toLowerCase()
    .replace(/[.,!?;:«»"'(){}\[\]]/g, ' ')
    .split(/\s+/)
    .filter(t => t.length > 1);
}

function countSyllables(word) {
  const vowels = word.match(/[aeiouyéèêëàâîïôùûü]/gi);
  return vowels ? vowels.length : 1;
}

function readabilityScore(text) {
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const tokens    = tokenize(text).filter(t => !STOPWORDS_FR.has(t));
  if (!sentences.length || !tokens.length) return 0;
  const avgWords     = tokens.length / sentences.length;
  const avgSyllables = tokens.reduce((s, t) => s + countSyllables(t), 0) / tokens.length;
  // Flesch-Kincaid adapté (approximation)
  const score = 206.835 - 1.015 * avgWords - 84.6 * avgSyllables;
  return Math.max(0, Math.min(100, Math.round(score)));
}

function tfidf(term, doc, allDocs) {
  const tokens = tokenize(doc);
  const tf = tokens.filter(t => t === term).length / tokens.length;
  const docsWithTerm = allDocs.filter(d => tokenize(d).includes(term)).length;
  const idf = Math.log((allDocs.length + 1) / (docsWithTerm + 1)) + 1;
  return +(tf * idf).toFixed(4);
}

function topKeywords(text, n = 8) {
  const tokens  = tokenize(text);
  const content = tokens.filter(t => !STOPWORDS_FR.has(t) && t.length > 3);
  const freq    = {};
  content.forEach(t => freq[t] = (freq[t] || 0) + 1);
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([w, c]) => ({ word: w, count: c }));
}

function analyseText(text) {
  const tokens    = tokenize(text);
  const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
  const words     = tokens.filter(t => !STOPWORDS_FR.has(t) && t.length > 1);
  const types     = new Set(words);
  const ttr       = words.length ? +(types.size / words.length).toFixed(3) : 0;
  const readab    = readabilityScore(text);
  const keywords  = topKeywords(text);
  return {
    tokens, sentences, words,
    nTokens:    tokens.length,
    nSentences: sentences.length,
    nTypes:     types.size,
    ttr,
    readab,
    keywords,
    avgWordLen: +(tokens.reduce((s, t) => s + t.length, 0) / (tokens.length || 1)).toFixed(1),
  };
}

// ── UI ──
const corpusData = window.CORPUS || [];

function renderResults(stats) {
  const box = document.getElementById('lingx-results');
  if (!box) return;
  box.style.display = 'block';

  const kwHtml = stats.keywords.map(k =>
    `<span class="token-chip">${k.word} <b>(${k.count})</b></span>`
  ).join('');

  const tokHtml = stats.tokens.slice(0, 60).map(t =>
    `<span class="token-chip ${STOPWORDS_FR.has(t) ? 'stopword' : ''}">${t}</span>`
  ).join('');

  box.innerHTML = `
    <div class="result-grid">
      <div class="result-pill"><div class="rp-label">Tokens</div><div class="rp-val">${stats.nTokens}</div></div>
      <div class="result-pill"><div class="rp-label">Phrases</div><div class="rp-val">${stats.nSentences}</div></div>
      <div class="result-pill"><div class="rp-label">Types uniques</div><div class="rp-val">${stats.nTypes}</div></div>
      <div class="result-pill"><div class="rp-label">TTR (richesse)</div><div class="rp-val">${stats.ttr}</div></div>
      <div class="result-pill"><div class="rp-label">Lisibilité</div><div class="rp-val">${stats.readab}/100</div></div>
      <div class="result-pill"><div class="rp-label">Long. moy. mot</div><div class="rp-val">${stats.avgWordLen}</div></div>
    </div>
    <h4 style="color:var(--primary);margin:.8rem 0 .4rem;font-family:var(--font-serif)">Mots-clés détectés</h4>
    <div class="tokens-box">${kwHtml}</div>
    <h4 style="color:var(--primary);margin:.8rem 0 .4rem;font-family:var(--font-serif)">Tokens (60 premiers — gris = mot vide)</h4>
    <div class="tokens-box">${tokHtml}</div>
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  const analyseBtn = document.getElementById('btn-analyse');
  const clearBtn   = document.getElementById('btn-clear');
  const textarea   = document.getElementById('lingx-input');
  const results    = document.getElementById('lingx-results');

  // Corpus items
  const corpusItems = document.querySelectorAll('.corpus-item');
  corpusItems.forEach(item => {
    item.addEventListener('click', () => {
      corpusItems.forEach(i => i.classList.remove('selected'));
      item.classList.add('selected');
      if (textarea) textarea.value = item.dataset.texte || '';
    });
  });

  if (analyseBtn) {
    analyseBtn.addEventListener('click', () => {
      const text = textarea?.value.trim();
      if (!text) { alert('Veuillez entrer ou sélectionner un texte.'); return; }
      const stats = analyseText(text);
      renderResults(stats);
    });
  }
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (textarea) textarea.value = '';
      if (results)  { results.style.display = 'none'; results.innerHTML = ''; }
      corpusItems.forEach(i => i.classList.remove('selected'));
    });
  }
});
