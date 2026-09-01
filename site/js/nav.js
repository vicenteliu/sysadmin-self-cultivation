/* The sidebar: the retrieval index, sliced four ways.

   The nav lists canonical (English) documents only — the 32 Chinese mirrors are not
   separate entries, they are the same document in another language. In Chinese, an
   entry that HAS a mirror links to it and shows its Chinese title; one that does not
   is tagged `EN`, because 32 of 204 canonical documents have a mirror — a fact a
   reader should see rather than discover. */

import { t, label, getLang } from "./i18n.js";

const AXIS_ORDER = ["start-here", "foundations", "the-stack", "platforms",
                    "cross-cutting", "build-out", "walkthrough", "toolbox", "meta"];
const KIND_ORDER = ["index", "note", "companion", "support-note", "lab", "route-step",
                    "walkthrough", "tool", "ansible-role", "skill-map", "agent-skill", "interview",
                    "adr", "roadmap", "questions", "glossary"];
const FACETS = [["axis", "byAxis"], ["platforms", "byPlatform"],
                ["themes", "byTheme"], ["kind", "byKind"]];

let facet = "axis";
const STORE_KEY = "ssc.facet";

export function currentFacet() { return facet; }

/** Canonical documents only, in a stable order: a folder's README, then everything else.

    A walkthrough is two canonical scripts, one per language, and neither is a mirror of
    the other — so the nav shows the one written in the language you are reading in.
    Without this an English reader gets a Chinese title in the list and no way to tell
    why. It is the same hiding the nav already does for the 32 mirrors, applied to a
    sibling instead of a derivative. */
export function canonicalDocs(state) {
  return Object.entries(state.index.files)
    .filter(([path, rec]) => !rec.derived && path.endsWith(".md") && inThisLanguage(rec))
    .sort(([a], [b]) => sortKey(a).localeCompare(sortKey(b)));
}

/** True unless the document names a language, and it is not the one on screen. */
export function inThisLanguage(rec) {
  return !rec.counterpart || (rec.language ?? "en") === getLang();
}

function sortKey(path) {
  const dir = path.includes("/") ? path.slice(0, path.lastIndexOf("/")) : "";
  const file = path.slice(path.lastIndexOf("/") + 1);
  return `${dir}/${file === "README.md" ? "0" : "1"}${file}`;
}

/** Every group for the current facet, as [value, paths[]] in a deliberate order. */
export function groups(state) {
  const docs = canonicalDocs(state);
  const bucket = new Map();

  for (const [path, rec] of docs) {
    const values = facet === "axis" ? [rec.axis || "meta"]
                 : facet === "kind" ? [rec.kind || "note"]
                 : (rec[facet] || []);
    for (const value of values) {
      if (!value) continue;
      if (!bucket.has(value)) bucket.set(value, []);
      bucket.get(value).push(path);
    }
  }

  const order = facet === "axis" ? AXIS_ORDER : facet === "kind" ? KIND_ORDER : null;
  const keys = [...bucket.keys()].sort((a, b) => {
    if (order) {
      const ia = order.indexOf(a), ib = order.indexOf(b);
      if (ia !== ib) return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
    }
    return a.localeCompare(b);
  });
  return keys.map((k) => [k, bucket.get(k)]);
}

/** In Chinese, prefer the mirror. Returns { href, title, mirrored }. */
export function entryFor(state, path) {
  const mirror = state.mirrorOf.get(path);
  if (getLang() === "zh" && mirror) {
    return { href: `#/${mirror}`, title: state.titles[mirror] || path, mirrored: true };
  }
  return { href: `#/${path}`, title: state.titles[path] || path, mirrored: !!mirror };
}

export function buildNav(state, activePath) {
  const picker = document.getElementById("facet-picker");
  picker.replaceChildren(...FACETS.map(([key, stringKey]) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.role = "tab";
    btn.textContent = t(stringKey);
    btn.setAttribute("aria-selected", String(facet === key));
    btn.addEventListener("click", () => {
      facet = key;
      try { localStorage.setItem(STORE_KEY, key); } catch { /* fine */ }
      buildNav(state, activePath);
    });
    return btn;
  }));

  const tree = document.getElementById("nav-tree");
  const facetName = facet === "platforms" ? "platform" : facet === "themes" ? "theme" : facet;
  const openGroups = new Set();

  tree.replaceChildren(...groups(state).map(([value, paths]) => {
    const details = document.createElement("details");
    details.className = "nav-group";
    const holdsActive = activePath && paths.some((p) =>
      p === activePath || state.mirrorOf.get(p) === activePath);
    details.open = holdsActive || (facet === "axis" && value === "start-here");
    if (details.open) openGroups.add(value);

    const summary = document.createElement("summary");
    summary.append(labelFor(facetName, value));
    const count = document.createElement("span");
    count.className = "n";
    count.textContent = paths.length;
    summary.append(count);
    details.append(summary);

    for (const path of paths) {
      const { href, title, mirrored } = entryFor(state, path);
      const a = document.createElement("a");
      a.href = href;
      a.textContent = title;
      const summary = state.index.files[path]?.summary;
      a.title = summary ? `${path}\n\n${summary}` : path;
      if (getLang() === "zh" && !mirrored) {
        const tag = document.createElement("span");
        tag.className = "n only-en";
        tag.textContent = "EN";
        a.append(tag);
      }
      if (path === activePath || state.mirrorOf.get(path) === activePath) {
        a.setAttribute("aria-current", "page");
      }
      details.append(a);
    }
    return details;
  }));

  const total = canonicalDocs(state).length;
  document.getElementById("nav-count").textContent =
    `${total} ${t("documents")} · ${state.mirrorCount} 🌐`;
  return openGroups;
}

function labelFor(facetName, value) {
  const span = document.createElement("span");
  span.textContent = (facetName === "axis" || facetName === "kind")
    ? label(facetName, value) : value;
  return span;
}

export function restoreFacet() {
  try {
    const saved = localStorage.getItem(STORE_KEY);
    if (saved && FACETS.some(([k]) => k === saved)) facet = saved;
  } catch { /* fine */ }
}
