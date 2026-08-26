/* UI chrome in two languages, and the facet labels that go with it.
   Content language and chrome language move together — decided deliberately: a reader
   who switched a document to Chinese did not ask for English buttons around it. */

let strings = null;
let lang = "en";

const STORE_KEY = "ssc.lang";

export function initI18n(loaded) {
  strings = loaded;
  try {
    const saved = localStorage.getItem(STORE_KEY);
    if (saved === "en" || saved === "zh") lang = saved;
  } catch { /* private window, blocked storage — English is a fine default */ }
  document.documentElement.lang = lang === "zh" ? "zh-Hans" : "en";
}

export const getLang = () => lang;

export function setLang(next) {
  lang = next;
  document.documentElement.lang = next === "zh" ? "zh-Hans" : "en";
  try { localStorage.setItem(STORE_KEY, next); } catch { /* not worth failing over */ }
  applyStatic();
}

/** A chrome string. Falls back to English, then to the key itself. */
export function t(key) {
  return (strings?.[lang]?.[key]) ?? (strings?.en?.[key]) ?? key;
}

/** A facet value's display name — `label("axis", "the-stack")` → "The stack". */
export function label(facet, value) {
  const entry = strings?.[facet]?.[value];
  if (entry) return entry[lang] ?? entry.en;
  return value.replace(/-/g, " ");
}

/** Re-stamp every element that declares a string key. */
export function applyStatic() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
  const badge = document.getElementById("lang-label");
  if (badge) badge.textContent = lang === "zh" ? "中文" : "EN";
  document.title = t("siteTitle");
}
