#!/usr/bin/env python3
"""Serve the documentation browser with nothing installed.

    python3 site/serve.py               # http://127.0.0.1:8000
    python3 site/serve.py --port 9000

Standard library only — that is the whole point. `site/` is served at `/`, and the
Markdown the browser renders is fetched through one extra endpoint:

    /doc/<repo-relative-path>.md    e.g. /doc/the-stack/02-network.md
    /doc/docs/index.json            the retrieval index the navigation is built from

**The endpoint is an allowlist, not a file server.** Only paths that `docs/index.json`
already lists are reachable; everything else is 404, so `.git/`, `.serena/`, and every
private file in the tree stay unreachable even though the repo root is one level up.
A repo that ships a hardening baseline should not ship a viewer that publishes its own
`.git` directory to localhost. `nginx.conf` implements the same URL contract for the
container; it enforces by extension and dotfile rules rather than by the allowlist, so
it is the *slightly* looser of the two.

Binds to 127.0.0.1. Serving this to a network is not a supported mode.
"""
import argparse, http.server, json, os, posixpath, socketserver, sys, urllib.parse

SITE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SITE)
INDEX_PATH = os.path.join(ROOT, "docs", "index.json")
DOC_PREFIX = "/doc/"
INDEX_ROUTE = "/doc/docs/index.json"


_allow = {"mtime": None, "paths": frozenset()}


def allowlist():
    """Every Markdown path the retrieval index lists, re-read when the index changes.

    Plus one derived family: a walkthrough script's sibling `*.floor.json`, which the
    floor needs and the index does not record because it is not a document. It is
    *derived* from the index rather than listed by hand, so a walkthrough that has not
    been written cannot have its scene data served, and nothing here needs maintaining
    when one is added.

    Reading it once at startup was the first version, and it was wrong in the way that
    matters: you write a new document, run `docs/build-index.py`, reload — and the
    server 404s the file you just wrote until you restart it. Stat-then-maybe-read is
    cheap enough to do per request.
    """
    try:
        mtime = os.stat(INDEX_PATH).st_mtime_ns
    except OSError:
        return _allow["paths"]
    if mtime != _allow["mtime"]:
        with open(INDEX_PATH, encoding="utf-8") as handle:
            paths = {p for p in json.load(handle)["files"] if p.endswith(".md")}
            for p in list(paths):
                if p.startswith("walkthrough/") and p.count(".") >= 2:
                    for scene in (p.rsplit(".", 2)[0] + ".floor.json",
                                  "walkthrough/reference-office.plate.json"):
                        if os.path.exists(os.path.join(ROOT, scene)):
                            paths.add(scene)
            _allow["paths"] = frozenset(paths)
        _allow["mtime"] = mtime
    return _allow["paths"]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE, **kwargs)

    def do_GET(self):
        served = self.serve_doc()
        if served is None:
            super().do_GET()

    def do_HEAD(self):
        served = self.serve_doc(body=False)
        if served is None:
            super().do_HEAD()

    def serve_doc(self, body=True):
        """Handle /doc/… — or return None to let the static handler take the request."""
        path = urllib.parse.urlparse(self.path).path
        if not path.startswith(DOC_PREFIX):
            return None

        if path == INDEX_ROUTE:
            return self.send_file(INDEX_PATH, "application/json; charset=utf-8", body)

        rel = posixpath.normpath(urllib.parse.unquote(path[len(DOC_PREFIX):]))
        if rel not in allowlist():
            self.send_error(404, "Not in the retrieval index")
            return True
        kind = ("application/json" if rel.endswith(".json") else "text/markdown")
        return self.send_file(os.path.join(ROOT, rel), f"{kind}; charset=utf-8", body)

    def send_file(self, full, content_type, body=True):
        try:
            with open(full, "rb") as handle:
                payload = handle.read()
        except OSError:
            self.send_error(404, "File not found")
            return True
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if body:
            self.wfile.write(payload)
        return True

    def end_headers(self):
        # A development server: you edit a file and reload. Nothing here is cached,
        # including the JS modules — the container is where caching is tuned.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "--quiet" not in sys.argv:
            super().log_message(fmt, *args)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(INDEX_PATH):
        print("docs/index.json is missing — run docs/build-index.py", file=sys.stderr)
        return 1
    if not os.path.exists(os.path.join(SITE, "corpus.json")):
        print("site/corpus.json is missing — run site/build-corpus.py", file=sys.stderr)
        return 1

    with Server(("127.0.0.1", args.port), Handler) as httpd:
        print(f"The Sysadmin's Self-Cultivation — http://127.0.0.1:{args.port}")
        print(f"serving {len(allowlist())} documents · Ctrl-C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
