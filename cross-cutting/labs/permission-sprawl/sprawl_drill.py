#!/usr/bin/env python3
"""
sprawl_drill.py — "who can see this?" is not answered by reading the permissions.

Two estates, built the same week, holding the same documents for the same hundred
people. One granted access only through groups and kept sharing links on a leash.
The other said "just this once" a few dozen times and left link sharing open.

The sprawled one has a few more names in the access-control list. That difference
is visible, unremarkable, and completely misleading — because **the ACL undercounts
in both**, and in the sprawled estate it undercounts by ninety-three.

A sharing link is a second grant path. It does not appear in the permissions, it is
not walked by an access review, and "anyone with the link" means the whole company.

Three things this drill measures rather than asserts:
  1. what it COSTS to answer "who can see this?" in each estate
  2. whether the answer is CORRECT
  3. whether an access review that reads group membership — the way almost every
     access review is actually performed — notices any of it

No cloud, no tenant, no credentials, no external dependencies. Pure stdlib.
Exit code 0 means every assertion about the lesson held. Run it in CI.
"""

import argparse
import sys
from dataclasses import dataclass, field

FAILURES = []
AUDIT_FOLLOWS_LINKS = True   # --break-it flips this: audit the way most people do


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

@dataclass
class Estate:
    name: str
    groups: dict = field(default_factory=dict)      # group -> set(members) | nested group names
    acl: dict = field(default_factory=dict)         # doc -> set(principals: "g:eng" or "u:dana")
    links: dict = field(default_factory=dict)       # doc -> list of link dicts
    grant_reason: dict = field(default_factory=dict)  # (doc, principal) -> why

    def members(self, g, seen=None):
        """Group membership, following nesting. Nesting is why 'read the group'
        is not a local operation."""
        seen = seen or set()
        if g in seen:
            return set()
        seen.add(g)
        out = set()
        for m in self.groups.get(g, set()):
            if m.startswith("g:"):
                out |= self.members(m[2:], seen)
            else:
                out.add(m)
        return out

    def acl_readers(self, doc):
        """What an admin sees when they open the sharing dialog."""
        out = set()
        for p in self.acl.get(doc, set()):
            out |= self.members(p[2:]) if p.startswith("g:") else {p[2:]}
        return out

    def effective_readers(self, doc, population):
        """Who can actually open it. ACLs PLUS anything a live link admits."""
        out = self.acl_readers(doc)
        if AUDIT_FOLLOWS_LINKS:
            for lk in self.links.get(doc, []):
                if lk["expired"]:
                    continue
                out |= set(population) if lk["scope"] == "anyone" else set(lk["scope"])
        return out

    def lookups_to_answer(self, doc):
        """A crude but honest cost model: one lookup per ACL entry, one per nested
        group hop, one per link that has to be found and read."""
        n = 0
        for p in self.acl.get(doc, set()):
            n += 1
            if p.startswith("g:"):
                stack, seen = [p[2:]], set()
                while stack:
                    g = stack.pop()
                    if g in seen:
                        continue
                    seen.add(g)
                    n += 1
                    stack += [m[2:] for m in self.groups.get(g, set()) if m.startswith("g:")]
        n += len(self.links.get(doc, []))
        return n


POPULATION = [f"p{i:03d}" for i in range(100)]
DOC = "Q3-pricing.xlsx"


def build_clean():
    e = Estate("group-only, links on a leash")
    e.groups = {
        "finance": {f"p{i:03d}" for i in range(0, 8)},
        "finance-leads": {"g:finance-core"},
        "finance-core": {f"p{i:03d}" for i in range(0, 3)},
    }
    e.acl[DOC] = {"g:finance-leads"}
    e.grant_reason[(DOC, "g:finance-leads")] = "role: finance lead"
    e.links[DOC] = [{"scope": ["p041"], "expired": False, "note": "named auditor, scoped"}]
    return e


def build_sprawled():
    e = Estate("'just this once', links open")
    # Same nominal group, same intent...
    e.groups = {
        "finance": {f"p{i:03d}" for i in range(0, 8)},
        "finance-leads": {"g:finance-core"},
        "finance-core": {f"p{i:03d}" for i in range(0, 3)},
    }
    # ...plus the individual grants that felt like one click at the time.
    e.acl[DOC] = {"g:finance-leads", "u:p017", "u:p044", "u:p061", "u:p083"}
    e.grant_reason[(DOC, "g:finance-leads")] = "role: finance lead"
    for u in ("p017", "p044", "p061", "p083"):
        e.grant_reason[(DOC, f"u:{u}")] = "(no reason recorded)"
    # And the link nobody revoked.
    e.links[DOC] = [
        {"scope": "anyone", "expired": False, "note": "'anyone with the link', no expiry"},
        {"scope": ["p041"], "expired": True, "note": "old auditor link, expired"},
    ]
    return e


def access_review(estate):
    """The review as it is actually performed: walk the groups, confirm each member
    still belongs. Returns the set of principals it EXAMINED."""
    examined = set()
    for p in estate.acl.get(DOC, set()):
        if p.startswith("g:"):
            examined |= estate.members(p[2:])
    return examined


# --- the drill ---------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--break-it", action="store_true",
                    help="audit ACLs only, ignoring sharing links — the way most "
                         "access reviews are actually done. The drill must FAIL.")
    a = ap.parse_args()

    global AUDIT_FOLLOWS_LINKS
    if a.break_it:
        AUDIT_FOLLOWS_LINKS = False
        log("!! running with --break-it: the audit now ignores sharing links\n")

    clean, sprawl = build_clean(), build_sprawled()

    step(1, "Same document, same people, one visible difference")
    for e in (clean, sprawl):
        n_ind = sum(1 for p in e.acl[DOC] if p.startswith("u:"))
        log(f"  {e.name:<34} ACL names {len(e.acl_readers(DOC))} people"
            f"  ({n_ind} of them granted individually)")
    check(clean.acl_readers(DOC) == sprawl.acl_readers(DOC) - {"p017", "p044", "p061", "p083"},
          "identical group structure underneath — the only ACL difference is four "
          "individual grants, which reads as a minor untidiness",
          "the two estates differ in their group structure; the comparison is unfair")
    log("     that four-name difference is the part you can see. It is not the part")
    log("     that matters.")

    step(2, "The ACL answer is wrong in one of them")
    for e in (clean, sprawl):
        acl = e.acl_readers(DOC)
        eff = e.effective_readers(DOC, POPULATION)
        hidden = eff - acl
        log(f"\n  {e.name}")
        log(f"     ACL says      : {len(acl)} people")
        log(f"     can ACTUALLY  : {len(eff)} people")
        log(f"     appear in no ACL: {len(hidden)}")
        for lk in e.links.get(DOC, []):
            state = "expired" if lk["expired"] else "LIVE"
            log(f"     link [{state}] {lk['note']}")

    hidden_clean = clean.effective_readers(DOC, POPULATION) - clean.acl_readers(DOC)
    hidden_sprawl = sprawl.effective_readers(DOC, POPULATION) - sprawl.acl_readers(DOC)
    check(len(hidden_sprawl) > len(hidden_clean),
          f"the sprawled estate has {len(hidden_sprawl)} readers its ACL does not "
          f"name, against {len(hidden_clean)} in the clean one — a link is a second "
          "grant path, and reading permissions cannot see it",
          "the sprawled estate has no hidden readers; the link path is not modelled")
    check(len(hidden_sprawl) > 50,
          f"'anyone with the link' means {len(hidden_sprawl)} of {len(POPULATION)} "
          "people, which is the whole company",
          "the open link did not admit the population")

    step(3, "The access review passes — on the wrong thing")
    for e, hidden in ((clean, hidden_clean), (sprawl, hidden_sprawl)):
        examined = access_review(e)
        missed = hidden - examined
        log(f"  {e.name:<34} review examined {len(examined):>3}, missed {len(missed):>3}")
    check(len(hidden_sprawl - access_review(sprawl)) > 0,
          "a review that walks group membership examines nobody who got in by link "
          "— it returns clean and is clean about the wrong set",
          "the group-membership review caught the link readers")
    check(not any(p.startswith("u:") for p in access_review(sprawl)),
          "and it never sees the individual grants either — they are not group "
          "members, so a group walk steps straight past them",
          "the review examined individual grants")

    step(4, "'Why does this person have access?'")
    for e in (clean, sprawl):
        reasons = {r for r in e.grant_reason.values()}
        unexplained = sum(1 for k, v in e.grant_reason.items() if "no reason" in v)
        log(f"  {e.name:<34} {len(reasons)} distinct reasons, "
            f"{unexplained} grants with none")
    check(all("no reason" not in v for v in clean.grant_reason.values()),
          "in the group-only estate every grant answers with a role — the reason is "
          "structural, so it survives the person who granted it leaving",
          "the clean estate has unexplained grants")
    check(sum(1 for v in sprawl.grant_reason.values() if "no reason" in v) >= 4,
          "in the sprawled estate the individual grants have no recorded reason, and "
          "there is no way to reconstruct one — this is what makes a review "
          "archaeology rather than a review",
          "the sprawled estate's grants are explained")

    step(5, "What it costs to answer the question at all")
    cc, sc = clean.lookups_to_answer(DOC), sprawl.lookups_to_answer(DOC)
    log(f"  {clean.name:<34} {cc} lookups")
    log(f"  {sprawl.name:<34} {sc} lookups")
    check(sc > cc,
          f"answering 'who can see this?' costs {sc} lookups against {cc} — and the "
          "gap grows with every 'just this once'",
          "the sprawled estate was not more expensive to answer")

    step(6, "Revoking one person")
    victim = "p002"   # a finance-core member, i.e. in via the nested group
    for e in (clean, sprawl):
        before = victim in e.effective_readers(DOC, POPULATION)
        e2 = build_clean() if e is clean else build_sprawled()
        e2.groups["finance-core"] = e2.groups["finance-core"] - {victim}
        after = victim in e2.effective_readers(DOC, POPULATION)
        log(f"  {e.name:<34} removed from the group → still has access: {after}")
    c2 = build_clean(); c2.groups["finance-core"] -= {victim}
    s2 = build_sprawled(); s2.groups["finance-core"] -= {victim}
    check(victim not in c2.effective_readers(DOC, POPULATION),
          "in the group-only estate, one removal revokes everywhere",
          "the clean estate did not revoke on group removal")
    check(victim in s2.effective_readers(DOC, POPULATION),
          "in the sprawled estate the same removal revokes nothing — the open link "
          "still admits them, and nobody looking at the group would know",
          "the sprawled estate revoked correctly; the residual path is not modelled")

    # --- verdict -------------------------------------------------------------
    log("\n" + "=" * 72)
    if FAILURES:
        log(f"FAILED — {len(FAILURES)} assertion(s) did not hold:")
        for f in FAILURES:
            log(f"  ✗ {f}")
        return 1

    log("PASSED — the lessons held.\n")
    log("  1. Two estates can present the same ACL and grant access to very")
    log("     different sets of people. Reading permissions is not an answer.")
    log("  2. A sharing link is a SECOND grant path. Perfect group hygiene is")
    log("     blind to it, and 'anyone with the link' means everyone.")
    log("  3. A review that walks group membership returns clean while examining")
    log("     none of the individual grants and none of the link readers. It is")
    log("     not a wrong answer — it is a correct answer to another question.")
    log("  4. Group grants carry their reason (a role). Individual grants lose it")
    log("     the moment the person who clicked leaves, and it cannot be rebuilt.")
    log("  5. Revocation is the test. One removal should revoke everywhere; if it")
    log("     does not, you do not have a permission model, you have a history.")
    log("\n  The auditor's question is not 'is it locked down'. It is 'who can see")
    log("  this, and how do you know'. The second half is the one that fails.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
