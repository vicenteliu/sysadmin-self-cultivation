#!/usr/bin/env python3
"""Prove `serve.py` answers correctly — without binding a port.

    python3 site/serve-smoke.py             # run the cases, report
    python3 site/serve-smoke.py --verbose   # and show the access log

Seven requests, three that must be answered and four that must not. The four are the
ones that matter: `serve.py` sits one directory below the repo root, so a `/doc/` path
that escapes upward, names a dotfile, or names a source file is the failure this repo
would be embarrassed to ship. `site/README.md` describes that allowlist; this asserts it.

**It never listens on anything.** A smoke test that starts a server has to pick a port,
wait for it, and clean it up, and it cannot run where binding is denied — a locked-down
CI runner, a sandbox, a container without loopback. None of that is needed: an HTTP
handler is a function from bytes to bytes, and `serve.py`'s `Handler` will take those
bytes from any object that offers `makefile()` and `sendall()`. So it gets one. The
request goes in as a literal `GET … HTTP/1.0` line and the response comes back out of a
buffer, through exactly the routing, allowlist and error paths a socket would reach.

Nothing here is a stub of `serve.py`. The only thing this file overrides is the access
log, and only so a passing run stays one screen.
"""
import argparse, importlib.util, io, os, sys

SITE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SITE)


def load_serve():
    """Import site/serve.py by path — it is a script, not an installed module."""
    spec = importlib.util.spec_from_file_location("serve", os.path.join(SITE, "serve.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


serve = load_serve()


class Wire:
    """Everything `socketserver.StreamRequestHandler` asks of a socket, and nothing more.

    `setup()` calls `makefile()` twice — once to read the request, once to write the
    response — and on Python 3.6+ the write side is a `_SocketWriter` that calls
    `sendall()`. Satisfying those three is the whole trick.
    """

    def __init__(self, request):
        self.incoming = io.BytesIO(request)
        self.outgoing = io.BytesIO()

    def makefile(self, mode, *args, **kwargs):
        return self.incoming if "r" in mode else self.outgoing

    def sendall(self, data):
        self.outgoing.write(data)

    def close(self):
        pass


class Bench:
    """`BaseHTTPRequestHandler` reads these two off the server for the Host header."""
    server_name = "127.0.0.1"
    server_port = 8000


def request(path, quiet=True):
    """Send one GET through the real handler. Returns (status, body)."""
    handler = serve.Handler
    if quiet:
        handler = type("Quiet", (serve.Handler,), {"log_message": lambda *a, **k: None})
    wire = Wire(f"GET {path} HTTP/1.0\r\n\r\n".encode())
    handler(wire, ("127.0.0.1", 0), Bench())
    raw = wire.outgoing.getvalue()
    head, _, body = raw.partition(b"\r\n\r\n")
    return int(head.split()[1]), body


#  path                          status  a byte the body must contain
CASES = [
    ("/",                            200, b"<"),
    ("/doc/docs/index.json",         200, b'"files"'),
    ("/doc/the-stack/02-network.md", 200, b"#"),
    ("/doc/../.git/config",          404, b""),   # escapes the root
    ("/doc/.git/config",             404, b""),   # names it outright
    ("/doc/.serena/project.yml",     404, b""),   # a private tool's directory
    ("/doc/site/serve.py",           404, b""),   # source, not a document
]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--verbose", action="store_true", help="show the access log")
    args = parser.parse_args()

    if not os.path.exists(os.path.join(ROOT, "docs", "index.json")):
        print("docs/index.json is missing — run docs/build-index.py", file=sys.stderr)
        return 1

    passed = 0
    for path, expected, needle in CASES:
        try:
            status, body = request(path, quiet=not args.verbose)
        except Exception as error:
            print(f"FAIL  {path} — {type(error).__name__}: {error}", file=sys.stderr)
            continue
        if status == expected and (not needle or needle in body):
            passed += 1
            print(f"ok    {status}  {len(body):>7,}B  {path}")
        else:
            print(f"FAIL  {status} (expected {expected})  {path}", file=sys.stderr)

    print(f"\n{passed}/{len(CASES)} · allowlist resolves {len(serve.allowlist())} paths")
    if passed != len(CASES):
        print("serve.py does not answer the way site/README.md says it does",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
