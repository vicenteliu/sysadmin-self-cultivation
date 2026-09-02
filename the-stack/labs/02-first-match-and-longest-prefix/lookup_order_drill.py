#!/usr/bin/env python3
"""
lookup_order_drill.py — prove, in your own hands, a lesson chapter 02 states twice
and that almost nobody holds as one idea: **a network path is decided by two lookup
disciplines that look identical on the page and are not.**

    a routing table   resolves by LONGEST PREFIX  — order-independent
    a firewall rules   resolves by FIRST MATCH     — order-dependent

Both are a list of lines with an address on each. Neither says which discipline it
uses. So an operator carries one intuition into the other, and gets two failures
that are exact mirrors:

  * moves a route line up to "prioritise" it, nothing changes, and concludes the
    route is not the problem — when it is
  * adds a broad allow at the top of a ruleset "to unblock the ticket", and silently
    disables every rule below it, with nothing anywhere reporting that

No cloud, no credentials, no dependencies. Pure Python stdlib. Exit code 0 means
every assertion about the lesson held. Run it in CI.

    python3 lookup_order_drill.py
    python3 lookup_order_drill.py --sabotage routes-first-match
    python3 lookup_order_drill.py --sabotage rules-longest-prefix
"""

import argparse
import ipaddress
import random
import sys

SABOTAGE = None


# --- the reporter — vendored, byte for byte, in every drill (ADR-0017) ------------
# check.py holds the canonical copy and fails a drill whose copy differs. Change it
# there and then everywhere; a drill imports nothing from this repo.

FAILURES = []


def log(msg=""):
    print(msg, flush=True)


def step(n, title):
    log(f"\n=== {n}. {title} ===")


def check(cond, ok_msg, fail_msg):
    if cond:
        log(f"  ✓ {ok_msg}")
    else:
        log(f"  ✗ {fail_msg}")
        FAILURES.append(fail_msg)
    return cond


def verdict(held, broken=False):
    """What main() returns: 1 with every failure listed, or 0 with the lessons that
    held — one line each, in the drill's own words."""
    log("\n" + "=" * 70)
    if FAILURES:
        log(f"FAILED — {len(FAILURES)} assertion(s) did not hold:")
        for f in FAILURES:
            log(f"  ✗ {f}")
        if broken:
            log("\nThat is the point of --break-it. Re-run without it.")
        return 1
    log("PASSED — the lessons held:")
    for line in held:
        log(line)
    return 0

# --- end of the reporter ------------------------------------------------------------


# --------------------------------------------------------------------------
# The two lookup disciplines. Same shape on the page; different rule for who wins.
# --------------------------------------------------------------------------

class RouteTable:
    """Longest-prefix match. The most specific prefix that contains the address
    wins, no matter where it sits in the file."""

    def __init__(self, routes):
        # routes: list of (prefix, next_hop) in file order
        self.routes = [(ipaddress.ip_network(p), nh) for p, nh in routes]

    def lookup(self, addr):
        ip = ipaddress.ip_address(addr)
        hits = [(net, nh) for net, nh in self.routes if ip in net]
        if not hits:
            return None
        if SABOTAGE == "routes-first-match":
            # The sabotage: resolve the way a ruleset does. This is the mistaken
            # model, implemented, so the drill can show what it would predict.
            return hits[0][1]
        return max(hits, key=lambda h: h[0].prefixlen)[1]

    def reordered(self, order):
        t = RouteTable([])
        t.routes = [self.routes[i] for i in order]
        return t


class RuleSet:
    """First match wins. The first line whose selectors match decides, and every
    line below it that would also have matched is never consulted."""

    def __init__(self, rules):
        # rules: list of (action, dst_prefix, port) in file order
        self.rules = [(a, ipaddress.ip_network(p), port) for a, p, port in rules]

    def _matches(self, rule, addr, port):
        _, net, rport = rule
        return ipaddress.ip_address(addr) in net and rport in ("any", port)

    def evaluate(self, addr, port):
        hits = [r for r in self.rules if self._matches(r, addr, port)]
        if not hits:
            return "deny", None  # default deny — the posture chapter 02 argues for
        if SABOTAGE == "rules-longest-prefix":
            # The sabotage: resolve the way a route table does.
            win = max(hits, key=lambda r: r[1].prefixlen)
        else:
            win = hits[0]
        return win[0], self.rules.index(win)

    def shadowed(self):
        """Rules that can never decide anything, because an earlier rule matches
        every address-and-port they would have matched. A ruleset still *contains*
        them; no console, no diff and no review reports that they are inert."""
        dead = []
        for i, (act, net, port) in enumerate(self.rules):
            covered = False
            for eact, enet, eport in self.rules[:i]:
                if enet.supernet_of(net) or enet == net:
                    if eport == "any" or eport == port:
                        covered = True
                        break
            if covered:
                dead.append((i, act, str(net), port))
        return dead

    def reordered(self, order):
        r = RuleSet([])
        r.rules = [self.rules[i] for i in order]
        return r


# --------------------------------------------------------------------------
# The estate: the reference office's three tiers, addressed once.
# --------------------------------------------------------------------------

ROUTES = [
    ("0.0.0.0/0",      "internet-gw"),
    ("10.20.0.0/16",   "vpc-local"),
    ("10.20.11.0/24",  "nat-gw"),        # the private app subnet, egress via NAT
    ("10.20.11.7/32",  "inspection-fw"), # one host is steered through inspection
]

RULES = [
    ("allow", "10.20.1.0/24",  443),   # public LB tier
    ("deny",  "10.20.11.7/32", "any"), # the quarantined host — a real intent
    ("allow", "10.20.11.0/24", 5432),  # app tier reaches the database
]

PROBES = ["10.20.1.9", "10.20.11.4", "10.20.11.7", "8.8.8.8"]


def verdicts_routes(table):
    return {a: table.lookup(a) for a in PROBES}


def verdicts_rules(rs):
    return {(a, p): rs.evaluate(a, p)[0]
            for a in PROBES for p in (443, 5432)}


def run():
    log(__doc__.strip().split("\n\n")[0])

    # ---------------------------------------------------------------- 1
    step(1, "Two files. Same shape. Nothing on the page says which rule wins.")
    log("  routing table                       firewall ruleset")
    for i in range(max(len(ROUTES), len(RULES))):
        left = f"{ROUTES[i][0]:<16} -> {ROUTES[i][1]}" if i < len(ROUTES) else ""
        right = (f"{RULES[i][0]:<5} {RULES[i][1]:<16} {RULES[i][2]}"
                 if i < len(RULES) else "")
        log(f"  {left:<36}{right}")
    log("  Both are ordered lists of prefixes. Only one of them cares about order.")

    # ---------------------------------------------------------------- 2
    step(2, "Shuffle both files and re-read every verdict")
    table, rules = RouteTable(ROUTES), RuleSet(RULES)
    base_r, base_f = verdicts_routes(table), verdicts_rules(rules)

    rng = random.Random(7)
    route_stable = True
    for _ in range(20):
        order = list(range(len(ROUTES)))
        rng.shuffle(order)
        if verdicts_routes(table.reordered(order)) != base_r:
            route_stable = False
            break
    check(route_stable,
          "20 shuffles of the routing table: every verdict identical — order is not "
          "the discipline (LESSON 1)",
          "reordering the routing table changed a verdict — longest prefix is not "
          "deciding")

    changed = 0
    for _ in range(20):
        order = list(range(len(RULES)))
        rng.shuffle(order)
        if verdicts_rules(rules.reordered(order)) != base_f:
            changed += 1
    check(changed > 0,
          f"20 shuffles of the ruleset: {changed} produced a different verdict — "
          "order IS the discipline (LESSON 2)",
          "reordering the ruleset changed nothing — first-match is not deciding")

    # ---------------------------------------------------------------- 3
    step(3, "The mirror error #1 — 'move the route up to prioritise it'")
    log("  A ticket says 10.20.11.7 is going out the wrong way. The reflex is to")
    log("  move its line to the top of the routing table.")
    promoted = table.reordered([3, 0, 1, 2])
    log(f"  before: 10.20.11.7 -> {table.lookup('10.20.11.7')}")
    log(f"  after : 10.20.11.7 -> {promoted.lookup('10.20.11.7')}")
    check(promoted.lookup("10.20.11.7") == table.lookup("10.20.11.7"),
          "promoting the line changed nothing — and the operator now believes the "
          "route is not the problem (LESSON 3)",
          "promoting a route line changed the verdict")
    log("  The fix, if the next hop is wrong, is a different PREFIX or next hop.")
    log("  Nothing about where the line sits was ever going to matter.")

    # ---------------------------------------------------------------- 4
    step(4, "The mirror error #2 — 'add a broad allow at the top to unblock it'")
    before_dead = rules.shadowed()
    log(f"  ruleset today: {len(RULES)} rules, {len(before_dead)} of them shadowed")
    unblocked = RuleSet([("allow", "10.20.0.0/16", "any")] + RULES)
    quarantined = unblocked.evaluate("10.20.11.7", 5432)[0]
    dead = unblocked.shadowed()
    log(f"  after one broad allow at the top: {len(unblocked.rules)} rules, "
        f"{len(dead)} shadowed")
    for i, act, net, port in dead:
        log(f"    rule {i}: {act:<5} {net:<16} {port}   — can never match")
    check(quarantined == "allow" and len(dead) == 3,
          "the quarantine deny is now inert, and so is every rule under the broad "
          "allow — three rules that still exist and never fire (LESSON 4)",
          "the broad allow did not shadow the rules below it")
    log("  The ruleset still CONTAINS the deny. A screenshot of it is truthful.")
    log("  Nothing in a console, a diff or an access review reports 'never matches'.")

    # ---------------------------------------------------------------- 5
    step(5, "The asymmetry worth carrying: specificity beats position, one way only")
    log("  A /32 added at the BOTTOM of a routing table wins over a /0 at the top.")
    log("  A /32 added at the BOTTOM of a ruleset loses to a /16 at the top.")
    log(f"  route : 10.20.11.7 -> {table.lookup('10.20.11.7')}"
        "   (the /32, and it is the last line)")
    log(f"  rule  : 10.20.11.7:5432 -> {quarantined}"
        "   (the /32 deny lost to the /16 above it)")
    check(table.lookup("10.20.11.7") == "inspection-fw" and quarantined == "allow",
          "the same specific line wins in one file and loses in the other — this is "
          "the whole of it (LESSON 5)",
          "specificity behaved the same way in both files")

    # ---------------------------------------------------------------- verdict
    return verdict([
        "  1. A routing table is order-independent: longest prefix decides.",
        "  2. A ruleset is order-dependent: first match decides.",
        "  3. Promoting a route line is a no-op that reads as a ruled-out theory.",
        "  4. A broad allow at the top makes the rules below it inert, silently.",
        "  5. Specificity beats position in one file and loses to it in the other.",
        "",
        "Before you read either file, ask which discipline it uses. It is the one",
        "question neither file answers, and both failures above are what happens",
        "when the answer is carried over from the other one.",
    ], broken=bool(SABOTAGE))


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sabotage", choices=["routes-first-match", "rules-longest-prefix"],
                    help="break the model on purpose; the drill must then fail")
    args = ap.parse_args()
    global SABOTAGE
    SABOTAGE = args.sabotage
    if SABOTAGE:
        log(f"*** SABOTAGE: {SABOTAGE} — assertions are expected to fail ***")
    sys.exit(run())


if __name__ == "__main__":
    main()
