/* Full-text search over the corpus.

   The corpus is 1.2 MB and is fetched the first time someone searches, not on load —
   the alternative was a metadata-only search, which for 200,000 words of prose would
   have found almost nothing you actually go looking for.

   Chinese is matched by substring and English by prefix, because "network" should find
   "networking" and 网络 has no word boundary to anchor to. */

import { t } from "./i18n.js";

let corpus = null;
let loading = null;

const CJK = /[㐀-鿿぀-ヿ가-힯]/;

async function load() {
  if (corpus) return corpus;
  if (!loading) {
    loading = fetch("corpus.json")
      .then((r) => r.json())
      .then((data) => { corpus = data.docs; return corpus; });
  }
  return loading;
}

function terms(query) {
  return query.toLowerCase().split(/[\s,;/]+/).filter((s) => s.length > 0).slice(0, 8);
}

function matcher(term) {
  const escaped = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(CJK.test(term) ? escaped : `\\b${escaped}`, "giu");
}

function tally(text, regex) {
  regex.lastIndex = 0;
  const found = text.match(regex);
  return found ? found.length : 0;
}

export async function search(query, state) {
  const docs = await load();
  const words = terms(query);
  if (!words.length) return [];

  const scored = [];
  for (const [path, doc] of Object.entries(docs)) {
    let score = 0;
    let hitAll = true;
    for (const word of words) {
      const re = matcher(word);
      const inTitle = tally(doc.t, re);
      const inHeadings = doc.h.reduce((sum, h) => sum + tally(h, re), 0);
      const inBody = tally(doc.b, re);
      if (!(inTitle + inHeadings + inBody)) { hitAll = false; break; }
      score += inTitle * 8 + inHeadings * 3 + Math.min(inBody, 12);
    }
    if (!hitAll) continue;
    // A mirror scoring the same as its source is noise; nudge canonical documents up.
    if (state.index.files[path]?.derived) score *= 0.85;
    scored.push({ path, score, doc });
  }

  scored.sort((a, b) => b.score - a.score || a.path.localeCompare(b.path));
  return scored.slice(0, 40).map((hit) => ({
    ...hit,
    summary: state.index.files[hit.path]?.summary ?? "",
    snippet: snippet(hit.doc.b, words),
  }));
}

function snippet(body, words) {
  const first = matcher(words[0]);
  const found = first.exec(body);
  const at = found ? Math.max(0, found.index - 90) : 0;
  let text = body.slice(at, at + 260);
  if (at > 0) text = `…${text}`;
  if (at + 260 < body.length) text = `${text}…`;
  return text;
}

export function highlight(text, query) {
  const fragment = document.createDocumentFragment();
  const words = terms(query);
  const combined = new RegExp(
    words.map((w) => {
      const e = w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      return CJK.test(w) ? e : `\\b${e}`;
    }).join("|"), "giu");

  let cursor = 0;
  for (const match of text.matchAll(combined)) {
    fragment.append(text.slice(cursor, match.index));
    const mark = document.createElement("mark");
    mark.textContent = match[0];
    fragment.append(mark);
    cursor = match.index + match[0].length;
  }
  fragment.append(text.slice(cursor));
  return fragment;
}

export async function renderSearch(query, state) {
  const main = document.getElementById("main");
  document.getElementById("toc").replaceChildren();

  if (!corpus) {
    main.innerHTML = `<article class="doc"><p class="empty">${t("loadingCorpus")}</p></article>`;
  }
  const hits = await search(query, state);

  const article = document.createElement("article");
  article.className = "doc";
  const heading = document.createElement("h1");
  heading.textContent = `${t("searchResultsFor")} “${query}”`;
  const count = document.createElement("p");
  count.className = "empty";
  count.textContent = hits.length ? `${hits.length} ${t("results")}` : t("noResults");
  article.append(heading, count);

  for (const hit of hits) {
    const a = document.createElement("a");
    a.className = "result";
    a.href = `#/${hit.path}`;

    const title = document.createElement("span");
    title.className = "result-title";
    title.append(highlight(hit.doc.t, query));

    const path = document.createElement("span");
    path.className = "result-path";
    path.textContent = hit.path;

    const body = document.createElement("p");
    body.className = "result-snippet";
    body.append(highlight(hit.snippet, query));

    a.append(title, path);
    // The snippet says why this matched; the summary says what it is. A reader scanning
    // forty results needs the second at least as much as the first.
    if (hit.summary) {
      const claim = document.createElement("p");
      claim.className = "result-summary";
      claim.textContent = hit.summary;
      a.append(claim);
    }
    a.append(body);
    article.append(a);
  }
  main.replaceChildren(article);
}
