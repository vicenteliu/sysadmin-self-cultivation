#!/usr/bin/env python3
"""
four_causes_drill.py — "the VPN won't connect" is not a diagnosis.

Four unrelated causes produce a user report that is word-for-word identical.
Guessing picks one and is usually wrong. Elimination — where every check is
chosen because it *rules something out* — gets there every time, and its worst
case is bounded.

The four, from build-out step 10:
  1. expired certificate on the gateway
  2. the identity provider is unreachable
  3. a captive portal is intercepting (hotel / cafe / airport wifi)
  4. the tunnel installs a more-specific route that does not carry auth traffic

No network, no VPN, no credentials, no external dependencies. Pure stdlib.

Two traps are modelled on purpose, because they are what actually costs the hours:
  - #2 and #3 MASQUERADE as each other: both look like "the directory is down".
    Exactly one observation separates them.
  - #4 fails AFTER the tunnel reports connected, so every check that asks
    "is the tunnel up?" answers yes and eliminates nothing.

Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass

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


# --- the model ---------------------------------------------------------------

# What the user says. Identical in all four worlds — that is the whole point.
USER_REPORT = "I can't connect. It just says authentication failed."


@dataclass(frozen=True)
class World:
    """One incident. Exactly one of these four is the real cause."""
    name: str
    cert_valid: bool = True
    idp_reachable_from_client: bool = True
    dns_answers_are_honest: bool = True      # False under a captive portal
    tunnel_carries_auth_subnet: bool = True

    @property
    def cause(self):
        if not self.cert_valid:
            return "expired-certificate"
        if not self.dns_answers_are_honest:
            return "captive-portal"
        if not self.idp_reachable_from_client:
            return "idp-unreachable"
        if not self.tunnel_carries_auth_subnet:
            return "route-specificity"
        return "no-fault"

    @property
    def tunnel_reports_connected(self):
        # #4 is the trap: the tunnel comes up fine, then auth fails inside it.
        return self.cause == "route-specificity"

    def user_visible_symptom(self):
        return USER_REPORT


WORLDS = [
    World("gateway cert expired over the weekend", cert_valid=False),
    World("identity provider having a bad hour", idp_reachable_from_client=False),
    World("hotel wifi captive portal", dns_answers_are_honest=False,
          idp_reachable_from_client=False),
    World("tunnel route does not carry the auth subnet",
          tunnel_carries_auth_subnet=False),
]


# --- the checks: each one is defined by what it ELIMINATES --------------------

@dataclass(frozen=True)
class Check:
    name: str
    # observe(world) -> a hypothesis set that remains possible given the result
    observe: object
    note: str = ""


ALL_CAUSES = {"expired-certificate", "idp-unreachable", "captive-portal",
              "route-specificity"}


def chk_cert(w):
    """Read the gateway's certificate expiry. Cheap, and eliminates one cause."""
    return ({"expired-certificate"} if not w.cert_valid
            else ALL_CAUSES - {"expired-certificate"})


def chk_dns_honesty(w):
    """Resolve a known name and compare against the expected answer.
    This is the ONE observation that separates a captive portal from a real
    outage — a portal answers everything, and answers it with itself."""
    return ({"captive-portal"} if not w.dns_answers_are_honest
            else ALL_CAUSES - {"captive-portal"})


def chk_idp_reachable(w):
    """Can we reach the identity provider at all?
    NOTE: this is FALSE under a captive portal too — it does not distinguish."""
    if not w.idp_reachable_from_client:
        return {"idp-unreachable", "captive-portal"}
    return ALL_CAUSES - {"idp-unreachable", "captive-portal"}


def chk_route_for_auth(w):
    """After the tunnel is up, which route wins for the auth subnet?"""
    return ({"route-specificity"} if not w.tunnel_carries_auth_subnet
            else ALL_CAUSES - {"route-specificity"})


def chk_restart_client(w):
    """The reflex. Eliminates nothing, in any world."""
    return set(ALL_CAUSES)


def chk_tunnel_up(w):
    """'Is the tunnel connected?' — feels diagnostic, and is not: it is TRUE in
    exactly the one case (#4) where something is still wrong."""
    return set(ALL_CAUSES)


ELIMINATION_ORDER = [
    Check("read the gateway certificate expiry", chk_cert,
          "cheapest, and one of the four is now gone"),
    Check("resolve a known name, compare the answer", chk_dns_honesty,
          "the single observation that separates a portal from an outage"),
    Check("reach the identity provider directly", chk_idp_reachable,
          "only meaningful AFTER the portal question is settled"),
    Check("check which route wins for the auth subnet", chk_route_for_auth,
          "the one that only shows up after the tunnel says 'connected'"),
]

GUESS_ORDER = [
    Check("restart the client", chk_restart_client, "eliminates nothing"),
    Check("is the tunnel connected?", chk_tunnel_up, "eliminates nothing"),
    Check("reach the identity provider directly", chk_idp_reachable,
          "narrows to two — and stops there"),
    Check("read the gateway certificate expiry", chk_cert, ""),
]


def diagnose(world, order, narrate=False):
    """Run checks in order, intersecting the possibility set. Stop at one."""
    possible = set(ALL_CAUSES)
    used = 0
    for c in order:
        possible &= c.observe(world)
        used += 1
        if narrate:
            log(f"     {used}. {c.name:<44} → {len(possible)} left"
                f"{'  (' + c.note + ')' if c.note else ''}")
        if len(possible) == 1:
            break
    return possible, used


# --- the drill ---------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", action="store_true",
                    help="deliberately corrupt one check so the drill FAILS — "
                         "proves the self-verification is real")
    a = ap.parse_args()

    if a.break_it:
        # Make the portal check useless. Elimination should now fail to separate
        # #2 from #3, and the drill must exit non-zero.
        ELIMINATION_ORDER[1] = Check("resolve a known name (SABOTAGED)",
                                     chk_restart_client, "eliminates nothing now")
        log("!! running with --break-it: the portal check has been sabotaged\n")

    step(1, "Four different incidents. One user report.")
    reports = {w.user_visible_symptom() for w in WORLDS}
    for w in WORLDS:
        log(f"  {w.cause:<22} → \"{w.user_visible_symptom()}\"")
    check(len(reports) == 1,
          "all four produce a byte-identical user report — the symptom carries "
          "zero diagnostic information",
          "the symptoms differ, so the model is not reproducing the real problem")

    step(2, "The reflex checks eliminate nothing")
    for c in (Check("restart the client", chk_restart_client),
              Check("is the tunnel connected?", chk_tunnel_up)):
        survived = [len(c.observe(w)) for w in WORLDS]
        check(all(s == len(ALL_CAUSES) for s in survived),
              f"'{c.name}' leaves all {len(ALL_CAUSES)} causes possible in every world",
              f"'{c.name}' unexpectedly narrowed something")
    log("     (they feel like progress because they produce a result, not because "
        "they remove a possibility)")

    step(3, "The masquerade: #2 and #3 look the same")
    idp_down = next(w for w in WORLDS if w.cause == "idp-unreachable")
    portal = next(w for w in WORLDS if w.cause == "captive-portal")
    check(chk_idp_reachable(idp_down) == chk_idp_reachable(portal),
          "'can I reach the IdP?' returns the SAME answer for a real outage and a "
          "captive portal — it cannot tell them apart",
          "the IdP check distinguished them; the masquerade is not modelled")
    check(chk_dns_honesty(idp_down) != chk_dns_honesty(portal),
          "checking whether DNS answers honestly is the one observation that does "
          "separate them",
          "the DNS-honesty check failed to separate the two")

    step(4, "The phase trap: #4 fails after 'connected'")
    route = next(w for w in WORLDS if w.cause == "route-specificity")
    check(route.tunnel_reports_connected,
          "the tunnel reports CONNECTED and authentication still fails — every "
          "check that asks 'is it up?' answers yes",
          "the route-specificity world does not report connected; trap not modelled")
    check(not any(w.tunnel_reports_connected for w in WORLDS if w is not route),
          "and it is the only one that does, which is why the reflex check is "
          "worse than useless here — it points away from the fault",
          "more than one world reports connected")

    step(5, "Guessing vs. eliminating, over all four incidents")
    log("  Elimination order — every check chosen because it rules something out:")
    elim_ok, elim_cost = 0, []
    for w in WORLDS:
        log(f"\n   · {w.name}")
        found, used = diagnose(w, ELIMINATION_ORDER, narrate=True)
        hit = found == {w.cause}
        elim_ok += hit
        elim_cost.append(used)
        log(f"     → {'correct' if hit else 'WRONG'}: {sorted(found)} in {used} checks")

    log("\n  Guess order — habit first, cheapest-to-type first:")
    guess_ok, guess_cost = 0, []
    for w in WORLDS:
        found, used = diagnose(w, GUESS_ORDER)
        hit = found == {w.cause}
        guess_ok += hit
        guess_cost.append(used)
        log(f"   · {w.name:<48} → {'correct' if hit else 'inconclusive'}"
            f" ({sorted(found)}) after {used} checks")

    step(6, "What that cost")
    check(elim_ok == len(WORLDS),
          f"elimination identified the cause in {elim_ok}/{len(WORLDS)} incidents",
          f"elimination only got {elim_ok}/{len(WORLDS)} — the ordering does not work")
    check(guess_ok < len(WORLDS),
          f"the guess order resolved only {guess_ok}/{len(WORLDS)} — it runs out of "
          "checks while two causes are still possible",
          "the guess order did as well as elimination; the contrast is not modelled")
    check(max(elim_cost) <= len(ALL_CAUSES),
          f"elimination's worst case is bounded: {max(elim_cost)} checks, never more "
          f"than the {len(ALL_CAUSES)} causes",
          "elimination exceeded its bound")

    # --- verdict -------------------------------------------------------------
    log("\n" + "=" * 72)
    if FAILURES:
        log(f"FAILED — {len(FAILURES)} assertion(s) did not hold:")
        for f in FAILURES:
            log(f"  ✗ {f}")
        return 1

    log("PASSED — the lessons held.\n")
    log('  1. "The VPN won\'t connect" is a symptom shared by four unrelated causes.')
    log("     Diagnosing from the symptom is guessing with extra steps.")
    log("  2. A check is worth running because of what it ELIMINATES. 'Restart it'")
    log("     and 'is it up?' produce a result and remove nothing.")
    log("  3. Two causes can masquerade: a captive portal and a real identity")
    log("     outage give the same answer to 'can I reach the IdP?'. Ask whether")
    log("     DNS is answering honestly — that is the one that separates them.")
    log("  4. One cause fails AFTER the tunnel says connected, so the reflex check")
    log("     actively points away from it.")
    log("\n  Same discipline as toolbox/linux-triage: order the checks by what each")
    log("  one rules out, and the worst case stops being unbounded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
