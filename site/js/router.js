/* Entry point: load the three small data files, then route on the hash.

   Routes
     #/                      home
     #/route                 the build-out route, as a route rather than an axis
     #/search/<query>        results
     #/<repo/path.md>        a document; `!anchor` after it scrolls to a heading

   The router owns the hash, which is why `render.js` turns in-document `#section`
   links into scroll handlers instead of leaving them to the browser. */

import { initI18n, applyStatic, setLang, getLang, t } from "./i18n.js";
import { buildNav, restoreFacet } from "./nav.js";
import { renderDoc, renderHome, renderRoute, renderNotFound, runMermaid, configureMermaid,
         retheme } from "./render.js";
import { renderSearch } from "./search.js";

const THEME_KEY = "ssc.theme";
const THEMES = ["auto", "light", "dark"];
const state = { index: null, titles: null, mirrorOf: new Map(), mirrorCount: 0 };

/* ── theme ────────────────────────────────────────────────────────────────── */

function readTheme() {
  try { return localStorage.getItem(THEME_KEY) ?? "auto"; } catch { return "auto"; }
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.getElementById("theme-toggle").textContent =
    theme === "light" ? "☀" : theme === "dark" ? "☾" : "◐";
  try { localStorage.setItem(THEME_KEY, theme); } catch { /* fine */ }
  configureMermaid();
  retheme();
  runMermaid();
}

/* ── routing ──────────────────────────────────────────────────────────────── */

function parse() {
  const raw = location.hash.replace(/^#\/?/, "");
  if (!raw) return { view: "home" };
  if (raw === "route") return { view: "route" };
  if (raw.startsWith("search/")) {
    return { view: "search", query: decodeURIComponent(raw.slice("search/".length)) };
  }
  const [path, anchor] = decodeURIComponent(raw).split("!");
  return { view: "doc", path, anchor };
}

async function route() {
  const target = parse();
  closeDrawer();

  const input = document.getElementById("search-input");
  if (target.view !== "search" && input.value) input.value = "";

  if (target.view === "home") { renderHome(state); buildNav(state, null); }
  else if (target.view === "route") { renderRoute(state); buildNav(state, null); }
  else if (target.view === "search") {
    input.value = target.query;
    buildNav(state, null);
    await renderSearch(target.query, state);
  } else if (!state.index.files[target.path]) {
    renderNotFound(target.path);
    buildNav(state, null);
  } else {
    // Landing on a document that names its own language is a language choice; follow
    // it. Mirrors always say "zh"; a walkthrough script says which of the two it is.
    const rec = state.index.files[target.path];
    if (rec.language && rec.language !== getLang()) setLang(rec.language);
    buildNav(state, target.path);
    await renderDoc(target.path, state, target.anchor);
  }
  document.getElementById("main").focus({ preventScroll: true });
}

/* ── chrome ───────────────────────────────────────────────────────────────── */

function closeDrawer() {
  document.body.classList.remove("drawer-open");
  document.getElementById("drawer-scrim").hidden = true;
  document.getElementById("drawer-toggle").setAttribute("aria-expanded", "false");
}

function wire() {
  document.getElementById("theme-toggle").addEventListener("click", () => {
    applyTheme(THEMES[(THEMES.indexOf(readTheme()) + 1) % THEMES.length]);
  });

  document.getElementById("lang-toggle").addEventListener("click", () => {
    const next = getLang() === "zh" ? "en" : "zh";
    setLang(next);
    const target = parse();
    // Follow the reader across to the other language of the document they are on.
    if (target.view === "doc") {
      const rec = state.index.files[target.path];
      const across = next === "zh" ? state.mirrorOf.get(target.path)
                                   : (rec?.derived ? rec.mirrors : null);
      if (across) { location.hash = `#/${across}`; return; }
    }
    route();
  });

  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (input.value.trim()) location.hash = `#/search/${encodeURIComponent(input.value.trim())}`;
  });

  let timer = null;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    const value = input.value.trim();
    timer = setTimeout(() => {
      if (value.length >= 2) location.hash = `#/search/${encodeURIComponent(value)}`;
      else if (!value && location.hash.startsWith("#/search/")) location.hash = "#/";
    }, 220);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "/" && document.activeElement !== input) {
      event.preventDefault();
      input.focus();
    }
    if (event.key === "Escape") { input.blur(); closeDrawer(); }
  });

  const toggle = document.getElementById("drawer-toggle");
  const scrim = document.getElementById("drawer-scrim");
  toggle.addEventListener("click", () => {
    const open = document.body.classList.toggle("drawer-open");
    scrim.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
  });
  scrim.addEventListener("click", closeDrawer);

  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    if (readTheme() === "auto") { configureMermaid(); retheme(); runMermaid(); }
  });

  addEventListener("hashchange", route);
}

/* ── boot ─────────────────────────────────────────────────────────────────── */

async function boot() {
  const [index, titles, strings] = await Promise.all([
    fetch("/doc/docs/index.json").then((r) => r.json()),
    fetch("titles.json").then((r) => r.json()),
    fetch("strings.json").then((r) => r.json()),
  ]);

  state.index = index;
  state.titles = titles.titles;
  for (const [path, rec] of Object.entries(index.files)) {
    if (rec.derived && rec.mirrors) {
      state.mirrorOf.set(rec.mirrors, path);
      state.mirrorCount += 1;
    }
  }

  initI18n(strings);
  restoreFacet();
  applyStatic();
  applyTheme(readTheme());
  wire();
  await route();
}

boot().catch((err) => {
  document.getElementById("main").innerHTML =
    `<article class="doc"><h1>Failed to start</h1><p class="empty">${err}</p>
     <p class="empty">Run <code>python3 docs/build-index.py</code> and
     <code>python3 site/build-corpus.py</code>, then reload.</p></article>`;
});
