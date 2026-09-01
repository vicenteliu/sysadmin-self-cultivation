---
kind: adr
axis: meta
themes: []
platforms: []
summary: "The repo now ships a browser at site/ — navigation, full-text search, a language switcher, rendered diagrams. It is the first thing here that is neither a document nor a tool, and the question it raises is what it is allowed to become."
---
# The site is a view over the material, not a seventh axis

> 🌐 **Languages:** English (default) · [中文](../zh/docs/adr/0005-the-site-is-a-view-not-a-seventh-axis.md)

The repo now ships a browser at [`site/`](../../site/README.md) — navigation,
full-text search, a language switcher, rendered diagrams. It is the first thing here
that is neither a document nor a tool, and the question it raises is what it is allowed
to become. Every documentation site the author has watched grow eventually sprouted
pages of its own: a "getting started" that is not in the repo, a landing page that
paraphrases the README, a tutorial that exists only on the site.

## Decision

**The site renders the material and adds none of it.** Every word a reader sees is
either in a Markdown file that GitHub also renders, or it is UI chrome — a button, a
facet name, an empty-state message. There is no page of the site that is not a file in
the repo, and there is no file in the repo that the site improves upon.

This is [ADR-0001](0001-the-build-out-is-a-route-not-a-seventh-axis.md)'s test applied
to a second candidate: *does it teach a new page?* `build-out/` did not, and was filed
as a route. The site does not, and is filed as a view.

## Considered options

- **A documentation site with its own content layer** — a hand-written home page,
  section landings, a tour. Rejected. It is the same failure ADR-0001 rejected, in a
  medium where it is harder to see: a site page has no path in the tree, so nothing
  makes it show up in `docs/index.json`, nothing makes it mirror to `docs/zh/`, and
  nothing catches it going stale. The material would fork, and the fork would be the
  copy people actually read.

- **No site at all; GitHub is the reader.** Genuinely tempting, and it is what the repo
  did for its whole life until now. Rejected for one reason that GitHub cannot fix:
  200,000 words with no full-text search. Everything else the site does — facets, the
  language toggle, a themed diagram — is a convenience. Search is not.

## Consequences

- **The home page is generated, not written.** Its counts, its axis cards and its route
  entry are computed from `docs/index.json` at load time. When an axis gains a
  document, the home page says so without anyone editing it — and cannot say anything
  the index does not know.
- **`build-out/` gets a view, not a card.** The site renders the sixteen route-steps as
  a linear track, deliberately outside the axis list, because drawing it as a seventh
  card would re-make ADR-0001's mistake in pixels.
- **A "site-only feature" request is a content question.** If a reader needs something
  the site cannot show, the fix is a Markdown file — then the site shows it, GitHub
  shows it, the index finds it, and the Chinese mirror can follow. The viewer is never
  the place where a fact first appears.
- **The site can be deleted without losing anything.** That is the test. If deleting
  `site/` would cost the repo a fact, the boundary has been crossed.
