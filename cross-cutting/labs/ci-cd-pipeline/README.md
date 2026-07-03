# Lab — A real CI/CD pipeline (test → build once → gated deploy)

**Goal:** make [the CI/CD chapter](../../ci-cd.md) concrete with a **real, valid
pipeline** over a tiny app — demonstrating the rules that matter: CI on every push
(fast feedback), **build the artifact once and promote it**, a **manual gate** before
prod, and **OIDC instead of a long-lived key**.

**You'll practice:** reading a pipeline as *automation with a gate and a log*, the
build-once-promote rule, and why the deploy job holds no static secret.

## What's here

```
ci-cd-pipeline/
├── app/
│   ├── hostcheck.py          # a tiny, testable unit (hostname validate/normalize)
│   └── test_hostcheck.py     # the tests CI runs on every push (pure stdlib)
└── .github-workflows-example/
    └── ci.yml                # the pipeline — copy to .github/workflows/ to run it
```

The workflow lives under `.github-workflows-example/` **on purpose** — GitHub only
runs workflows in `.github/workflows/`, so it will *not* execute against this teaching
repo. To actually run it, copy `ci.yml` into `.github/workflows/` of a repo that
contains the `app/` directory.

## Run the tests locally (what CI runs, minus GitHub)

The app is pure Python stdlib, so the test job needs no `pip install`:

```bash
cd app
python3 -m unittest -v          # 8 tests, exit 0 = green
python3 hostcheck.py "  Web01.PROD  " "bad_host!"   # see it normalize + reject
```

That `python3 -m unittest` is exactly the command the pipeline's **test** job runs —
the local version of "every commit is built and tested automatically."

## The pipeline, and the rules it encodes

Three jobs, each demonstrating a chapter rule:

- **`test`** — lint (`py_compile`) + `unittest` on every push and PR. Fast feedback in
  minutes, not at release. A red test here stops everything downstream.
- **`build`** — `needs: test`, so it only runs if tests are green, and it **packages
  the app once** into an artifact. The next job promotes *this same artifact* — never
  a rebuild-per-stage (the rule that kills the "works in staging, breaks in prod" bug).
- **`deploy`** — `needs: build`, runs in a `production` **environment** (a protected
  environment = the **manual approval gate**), and requests `id-token: write` so it
  can mint a **short-lived OIDC token** — **no long-lived cloud key in the repo**. The
  commented-out `configure-aws-credentials` step shows where a real role-assume goes.

## The point

- **The pipeline is the only path to prod** — a change that skips it is drift at the
  deployment layer.
- **Build once, promote the same artifact** — `build` produces it, `deploy` consumes
  the exact same one.
- **OIDC over static keys** — the deploy job holds no secret to leak; it mints a
  short-lived token. CI systems can deploy anything, which makes them a high-value
  target — so they hold no standing credential.
- **Gates and logs** — the `production` environment is the human gate; the Actions run
  is the audit log ("who deployed what, when" = the run history).

## Teardown

Nothing to tear down locally. If you copied `ci.yml` into a real repo's
`.github/workflows/`, delete it there to stop the pipeline from running.
