/* Markdown → page. Also the home and route views.

   Three things happen here that a plain Markdown renderer does not do:

   1. **Links are rewritten.** A document links to its neighbours the way GitHub needs
      (`../the-stack/README.md`, `toolbox/generate/`). Those are resolved against the
      document's own path and turned into routes. A bare directory becomes its README —
      which is what 29 of the repo's `../../foundations/`-style links mean. Anything the
      viewer cannot serve (a `.sh`, a `.json`) goes to GitHub instead of 404-ing.
   2. **In-page anchors do not touch the hash.** The router owns the hash; a `#section`
      link scrolls instead of navigating.
   3. **Mermaid inherits the brass skin**, so a runtime-rendered diagram and an exported
      hero SVG are the same drawing in two media, not two visual languages. */

import { t, label, getLang, setLang } from "./i18n.js";

// The one piece of deployment knowledge the viewer holds. It is used only for files
// the allowlist does not serve; every Markdown link stays inside the viewer.
const REPO_URL = "https://github.com/vicenteliu/sysadmin-self-cultivation";
const BRANCH = "main";

const FRONT_MATTER = /^---\n[\s\S]*?\n---\n/;
const EXT = /\.[a-z0-9]+$/i;

/* ── mermaid ──────────────────────────────────────────────────────────────── */

const MERMAID_LIGHT = {
  background: "#faf8f4", mainBkg: "#f0ece4", primaryColor: "#f0ece4",
  primaryTextColor: "#26262b", primaryBorderColor: "#c9c2b4", nodeBorder: "#c9c2b4",
  secondaryColor: "#e7e2d8", tertiaryColor: "#faf8f4", lineColor: "#5d5a52",
  textColor: "#26262b", titleColor: "#26262b", edgeLabelBackground: "#faf8f4",
  clusterBkg: "rgba(168,118,62,0.06)", clusterBorder: "#c9c2b4",
  labelBoxBkgColor: "#f0ece4", labelBoxBorderColor: "#c9c2b4",
  actorBkg: "#f0ece4", actorBorder: "#c9c2b4", actorTextColor: "#26262b",
  signalColor: "#5d5a52", signalTextColor: "#26262b", noteBkgColor: "rgba(168,118,62,0.10)",
  noteBorderColor: "#a8763e", noteTextColor: "#26262b",
};
const MERMAID_DARK = {
  background: "#1a1a17", mainBkg: "#25241f", primaryColor: "#25241f",
  primaryTextColor: "#faf8f4", primaryBorderColor: "rgba(201,194,180,0.35)",
  nodeBorder: "rgba(201,194,180,0.35)", secondaryColor: "#302e28", tertiaryColor: "#1a1a17",
  lineColor: "#b8b2a6", textColor: "#faf8f4", titleColor: "#faf8f4",
  edgeLabelBackground: "#1a1a17", clusterBkg: "rgba(201,154,91,0.08)",
  clusterBorder: "rgba(201,194,180,0.30)", labelBoxBkgColor: "#25241f",
  labelBoxBorderColor: "rgba(201,194,180,0.35)", actorBkg: "#25241f",
  actorBorder: "rgba(201,194,180,0.35)", actorTextColor: "#faf8f4",
  signalColor: "#b8b2a6", signalTextColor: "#faf8f4",
  noteBkgColor: "rgba(201,154,91,0.14)", noteBorderColor: "#c99a5b", noteTextColor: "#faf8f4",
};

export function isDark() {
  const chosen = document.documentElement.dataset.theme;
  if (chosen === "dark") return true;
  if (chosen === "light") return false;
  return matchMedia("(prefers-color-scheme: dark)").matches;
}

export function configureMermaid() {
  globalThis.mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: "base",
    themeVariables: isDark() ? MERMAID_DARK : MERMAID_LIGHT,
    fontFamily: "'Geist', system-ui, -apple-system, sans-serif",
    // Mermaid sizes a cluster label as if it were one line, so a wrapped subgraph title
    // lands on top of the first node inside it. The repo's longest is 74 characters;
    // widening the wrap point keeps every one of them to two lines, and the bottom
    // margin covers the second.
    // `useMaxWidth: false` keeps a wide diagram at its natural size and lets the
    // container scroll, rather than shrinking a five-node flow until its labels are
    // unreadable. `.doc .mermaid svg { max-width: none }` is the other half of that.
    flowchart: { curve: "basis", useMaxWidth: false, padding: 14, wrappingWidth: 260,
                 subGraphTitleMargin: { top: 6, bottom: 34 } },
    mindmap: { useMaxWidth: false, padding: 12 },
    sequence: { useMaxWidth: false },
    gantt: { useMaxWidth: false },
  });
}

/** Render every mermaid block in the page. Safe to call again after a theme change. */
/** Point every theme-aware figure at the variant matching the current theme. */
export function retheme() {
  const key = isDark() ? "dark" : "light";
  for (const img of document.querySelectorAll("img[data-light][data-dark]")) {
    const wanted = img.dataset[key];
    if (img.getAttribute("src") !== wanted) img.setAttribute("src", wanted);
  }
}

export async function runMermaid() {
  const blocks = [...document.querySelectorAll(".mermaid")];
  if (!blocks.length) return;
  configureMermaid();
  for (const [i, el] of blocks.entries()) {
    const source = el.dataset.src;
    try {
      const { svg } = await globalThis.mermaid.render(`mmd-${Date.now()}-${i}`, source);
      el.innerHTML = svg;
      fit(el);
      delete el.dataset.failed;
    } catch (err) {
      // A broken diagram must not take the page with it: show the source and say so.
      el.dataset.failed = "1";
      el.textContent = `mermaid failed to render — ${err?.message ?? err}\n\n${source}`;
    }
  }
}

/** Shrink a diagram to the column if that stays legible; otherwise leave it at its
    natural size and let the container scroll. Below about 62% the labels — 9px mono
    sublabels in places — stop being readable, and a scrollbar is the better bargain. */
const LEGIBLE_FLOOR = 0.62;

function fit(el) {
  const svg = el.querySelector("svg");
  if (!svg) return;
  const natural = svg.getBoundingClientRect().width;
  const room = el.clientWidth - 32;                 // the container's own padding
  if (natural > room && room / natural >= LEGIBLE_FLOOR) {
    svg.style.width = "100%";
    svg.style.height = "auto";
  }
}

/* ── links ────────────────────────────────────────────────────────────────── */

function resolve(from, href) {
  const base = from.includes("/") ? from.slice(0, from.lastIndexOf("/") + 1) : "";
  const parts = (base + href).split("/");
  const out = [];
  for (const part of parts) {
    if (part === "." || part === "") continue;
    if (part === "..") out.pop();
    else out.push(part);
  }
  return out.join("/") + (href.endsWith("/") ? "/" : "");
}

function rewriteLinks(root, docPath, state) {
  for (const a of root.querySelectorAll("a[href]")) {
    const href = a.getAttribute("href");

    if (/^([a-z]+:|\/\/)/i.test(href)) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      continue;
    }
    if (href.startsWith("#")) {
      a.dataset.anchor = href.slice(1);
      a.removeAttribute("href");
      a.style.cursor = "pointer";
      a.tabIndex = 0;
      continue;
    }

    const [rawPath, hash] = href.split("#");
    let target = resolve(docPath, rawPath || "");

    if (target.endsWith("/") || !EXT.test(target)) {          // a directory link
      const readme = target.replace(/\/$/, "") + "/README.md";
      target = state.index.files[readme] ? readme : target;
    }
    if (target.endsWith(".md") && state.index.files[target]) {
      a.setAttribute("href", `#/${target}${hash ? `!${hash}` : ""}`);
      continue;
    }
    // Not something the viewer serves — a script, a JSON, a directory with no README.
    a.setAttribute("href", `${REPO_URL}/blob/${BRANCH}/${target.replace(/\/$/, "")}`);
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.title = t("openOnGitHub");
  }

  const assetUrl = (value) => {
    if (!value) return value;
    if (/^([a-z]+:|\/\/|data:)/i.test(value)) return value;
    if (value.startsWith("/")) return value;            // already resolved by this pass
    const target = resolve(docPath, value);
    // Site-owned assets (the hero diagrams) come from the site root, not from /doc/.
    return target.startsWith("site/") ? `/${target.slice(5)}` : `/doc/${target}`;
  };

  // A <picture> switches on `prefers-color-scheme`, which is the OS setting — but this
  // page also has a manual theme toggle. Collapse each one to a single <img> carrying
  // both resolved sources so `retheme()` can follow the toggle instead of the OS.
  for (const picture of root.querySelectorAll("picture")) {
    const dark = picture.querySelector('source[media*="dark"]')?.getAttribute("srcset");
    const img = picture.querySelector("img");
    if (!dark || !img) continue;
    img.dataset.light = assetUrl(img.getAttribute("src"));
    img.dataset.dark = assetUrl(dark);
    img.setAttribute("src", img.dataset.light);
    picture.replaceWith(img);
  }

  for (const img of root.querySelectorAll("img[src]")) {
    img.setAttribute("src", assetUrl(img.getAttribute("src")));
  }
}

/* ── document ─────────────────────────────────────────────────────────────── */

export async function renderDoc(path, state, anchor) {
  const main = document.getElementById("main");
  main.innerHTML = `<p class="empty">${t("loading")}</p>`;

  const response = await fetch(`/doc/${path}`);
  if (!response.ok) return renderNotFound(path);
  const markdown = (await response.text()).replace(FRONT_MATTER, "");

  const article = document.createElement("article");
  article.className = "doc";
  article.append(metaBar(path, state));

  const body = document.createElement("div");
  body.innerHTML = globalThis.marked.parse(markdown);
  promoteMermaid(body);
  rewriteLinks(body, path, state);
  numberHeadings(body);
  article.append(body);

  main.replaceChildren(article);
  buildToc(body);
  retheme();
  await runMermaid();

  if (anchor) scrollToAnchor(anchor);
  else main.scrollIntoView({ block: "start" });
  body.addEventListener("click", (event) => {
    const a = event.target.closest("[data-anchor]");
    if (a) { event.preventDefault(); scrollToAnchor(a.dataset.anchor); }
  });
}

function promoteMermaid(root) {
  for (const code of root.querySelectorAll("code.language-mermaid")) {
    const holder = document.createElement("div");
    holder.className = "mermaid";
    holder.dataset.src = code.textContent;
    code.closest("pre").replaceWith(holder);
  }
}

function slug(text) {
  return text.toLowerCase().trim()
    .replace(/[^\p{L}\p{N}\s-]/gu, "").replace(/\s+/g, "-").replace(/-+/g, "-");
}

function numberHeadings(root) {
  const seen = new Map();
  for (const h of root.querySelectorAll("h2, h3")) {
    let id = slug(h.textContent) || "section";
    const n = (seen.get(id) ?? 0) + 1;
    seen.set(id, n);
    if (n > 1) id = `${id}-${n}`;
    h.id = id;
    const anchor = document.createElement("a");
    anchor.className = "anchor";
    anchor.dataset.anchor = id;
    anchor.textContent = "#";
    h.append(anchor);
  }
}

function scrollToAnchor(id) {
  const target = document.getElementById(id);
  if (target) target.scrollIntoView({ block: "start" });
}

function metaBar(path, state) {
  const rec = state.index.files[path] ?? {};
  const bar = document.createElement("div");
  bar.className = "doc-meta";

  const kind = document.createElement("span");
  kind.className = "tag accent";
  kind.textContent = label("kind", rec.kind || "note");
  bar.append(kind);

  const axis = document.createElement("span");
  axis.className = "tag";
  axis.textContent = label("axis", rec.axis || "meta");
  bar.append(axis);

  for (const p of (rec.platforms || []).slice(0, 4)) {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = p;
    bar.append(tag);
  }

  bar.append(mirrorControl(path, state, rec));

  const source = document.createElement("a");
  source.className = "path";
  source.href = `${REPO_URL}/blob/${BRANCH}/${path}`;
  source.target = "_blank";
  source.rel = "noopener noreferrer";
  source.textContent = path;
  bar.append(source);
  return bar;
}

function mirrorControl(path, state, rec) {
  if (rec.derived && rec.mirrors) {                       // we are on the Chinese mirror
    const back = document.createElement("a");
    back.className = "mirror";
    back.href = `#/${rec.mirrors}`;
    back.textContent = `🌐 ${t("backToEnglish")}`;
    back.addEventListener("click", () => setLang("en"));
    return back;
  }
  const mirror = state.mirrorOf.get(path);
  if (mirror) {
    const to = document.createElement("a");
    to.className = "mirror";
    to.href = `#/${mirror}`;
    to.textContent = `🌐 ${t("mirrorAvailable")}`;
    to.addEventListener("click", () => setLang("zh"));
    return to;
  }
  const none = document.createElement("button");     // 25 of 193 — say so, do not hide it
  none.type = "button";
  none.disabled = true;
  none.textContent = `🌐 ${t("mirrorMissing")}`;
  return none;
}

/* ── table of contents ────────────────────────────────────────────────────── */

function buildToc(body) {
  const toc = document.getElementById("toc");
  const headings = [...body.querySelectorAll("h2, h3")];
  if (headings.length < 2) { toc.replaceChildren(); return; }

  const title = document.createElement("h2");
  title.textContent = t("onThisPage");
  const links = headings.map((h) => {
    const a = document.createElement("a");
    a.href = "javascript:void 0";
    a.dataset.tocFor = h.id;
    a.className = h.tagName === "H3" ? "h3" : "";
    a.textContent = h.firstChild?.textContent?.trim() ?? h.textContent;
    a.addEventListener("click", (event) => { event.preventDefault(); scrollToAnchor(h.id); });
    return a;
  });
  toc.replaceChildren(title, ...links);

  const spy = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      toc.querySelectorAll("a").forEach((a) =>
        a.classList.toggle("active", a.dataset.tocFor === entry.target.id));
    }
  }, { rootMargin: "-72px 0px -70% 0px" });
  headings.forEach((h) => spy.observe(h));
}

/* ── home, route, 404 ─────────────────────────────────────────────────────── */

const AXIS_BLURB = {
  "start-here":    { en: "The operating model, the why, and the map.", zh: "操作模型、动机与全图。" },
  "foundations":   { en: "What holds under every platform.",           zh: "所有平台底下都成立的东西。" },
  "the-stack":     { en: "Seven layers, physical to security.",        zh: "七层，从物理到安全。" },
  "platforms":     { en: "Seven platforms, one shape each.",           zh: "七个平台，每个一副骨架。" },
  "cross-cutting": { en: "Themes that cut across every platform.",     zh: "横穿所有平台的主题。" },
  "build-out":     { en: "One route across the axes.",                 zh: "横穿这些轴的一条路线。" },
  "toolbox":       { en: "Scripts and roles that run.",                zh: "能跑的脚本与角色。" },
  "meta":          { en: "Decisions, questions, translations.",        zh: "决策、问题与翻译。" },
};
const AXIS_ORDER = ["start-here", "foundations", "the-stack", "platforms",
                    "cross-cutting", "build-out", "toolbox", "meta"];

export function renderHome(state) {
  const lang = getLang();
  const main = document.getElementById("main");
  const counts = new Map();
  let labs = 0, tools = 0, skills = 0;
  for (const [path, rec] of Object.entries(state.index.files)) {
    if (rec.derived || !path.endsWith(".md")) continue;
    counts.set(rec.axis, (counts.get(rec.axis) ?? 0) + 1);
    if (rec.kind === "lab") labs += 1;
    if (rec.kind === "tool" || rec.kind === "ansible-role") tools += 1;
    if (rec.kind === "agent-skill") skills += 1;
  }
  const total = [...counts.values()].reduce((a, b) => a + b, 0);

  main.innerHTML = `
    <div class="doc">
      <div class="home-hero">
        <h1>${t("siteTitle")}</h1>
        <p class="lead">${t("homeLead")}</p>
      </div>
      <figure class="hero-figure">
        <img class="light" src="assets/diagrams/repo-map.light.svg" alt="" onerror="this.closest('figure').remove()">
        <img class="dark"  src="assets/diagrams/repo-map.dark.svg"  alt="">
      </figure>

      <p class="section-label">${t("homeStats")}</p>
      <div class="stat-row">
        <span class="stat"><span class="v">${total}</span><span class="k">${t("documents")}</span></span>
        <span class="stat"><span class="v">${labs}</span><span class="k">${label("kind", "lab")}</span></span>
        <span class="stat"><span class="v">${tools}</span><span class="k">${label("kind", "tool")}</span></span>
        <span class="stat"><span class="v">${skills}</span><span class="k">${label("kind", "agent-skill")}</span></span>
        <span class="stat"><span class="v">${state.mirrorCount}</span><span class="k">🌐 mirrors</span></span>
      </div>

      <p class="section-label">${t("homeAxes")}</p>
      <div class="axis-grid">
        ${AXIS_ORDER.filter((a) => a !== "build-out").map((axis) => `
          <a class="axis-card" href="#/${entryPath(state, axis)}">
            <span class="name">${label("axis", axis)}</span>
            <span class="desc">${AXIS_BLURB[axis]?.[lang] ?? ""}</span>
            <span class="n">${counts.get(axis) ?? 0} ${t("documents")}</span>
          </a>`).join("")}
      </div>

      <p class="section-label">${t("homeRoute")}</p>
      <p class="lead">${t("homeRouteLead")}</p>
      <a class="route-cta" href="#/route">${t("startRoute")} →</a>
    </div>`;
  document.getElementById("toc").replaceChildren();
}

/** The document a reader should land on for an axis: its top-level README. */
function entryPath(state, axis) {
  const candidates = Object.entries(state.index.files)
    .filter(([p, r]) => !r.derived && r.axis === axis && p.endsWith("README.md"))
    .sort(([a], [b]) => a.split("/").length - b.split("/").length);
  if (candidates.length) return candidates[0][0];
  const any = Object.entries(state.index.files).find(([p, r]) => !r.derived && r.axis === axis);
  return any ? any[0] : "README.md";
}

export function renderRoute(state) {
  const steps = Object.entries(state.index.files)
    .filter(([p, r]) => !r.derived && r.kind === "route-step")
    .sort(([a], [b]) => a.localeCompare(b));

  const main = document.getElementById("main");
  main.innerHTML = `
    <article class="doc">
      <div class="doc-meta"><span class="tag accent">${label("axis", "build-out")}</span>
        <span class="path">build-out/</span></div>
      <h1>${t("routeTitle")}</h1>
      <p class="lead">${t("homeRouteLead")}</p>
      <ol class="route-list">
        ${steps.map(([path], i) => `
          <li data-step="${String(i).padStart(2, "0")}">
            <a href="#/${path}">${state.titles[path] ?? path}</a>
            <p>${state.index.files[path].summary ?? ""}</p>
          </li>`).join("")}
      </ol>
    </article>`;
  document.getElementById("toc").replaceChildren();
}

export function renderNotFound(path) {
  document.getElementById("main").innerHTML = `
    <article class="doc">
      <h1>${t("notFound")}</h1>
      <p class="empty">${t("notFoundBody")}</p>
      <p><code>${path}</code></p>
    </article>`;
  document.getElementById("toc").replaceChildren();
}
