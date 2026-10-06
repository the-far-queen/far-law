"""
test_cite.py — L1..L8 gate tests for far-law.

The important ones are L2/L3/L6/L8: the gate exists to stop an
AI-written legal corpus from filling up with plausible-sounding
fabrication, so the tests that matter are the ones where a bad
document is REFUSED.

Run:  python tests/test_cite.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))

from cite import (  # noqa: E402
    Citation, Document, DIVISIONS, JURISDICTIONS, LICENSES,
    LICENSE_RANK, Term, compile_doc, gate, gate_term, load_terms,
)

DISK = list(DIVISIONS)


def good_opinion(**over):
    base = dict(
        kind="opinion",
        title="Marbury v. Madison",
        jurisdiction="us-federal",
        division="constitutional",
        doc_date="1803-02-24",
        license="public-domain",
        citation=Citation(
            reporter="5 U.S. 137",
            pin_cite="177",
            source_url="https://tile.loc.gov/storage-services/service/ll/usrep/usrep005/usrep005137/usrep005137.pdf",
            court="U.S. Supreme Court",
            year=1803,
        ),
    )
    base.update(over)
    return compile_doc(**base)


def t_L1_repro_id():
    """same axes -> same id, regardless of body text."""
    a = good_opinion()
    b = good_opinion()
    assert a.doc_id() == b.doc_id(), "same document, different id"
    c = good_opinion(title="A Different Case")
    assert a.doc_id() != c.doc_id(), "different document, same id"
    print("L1: ok (deterministic document id)")


def t_L2_citation_required():
    """a document with no reporter and no URL is refused."""
    d = good_opinion(citation=Citation())
    v = gate(d, DISK)
    assert not v.allow, "uncited document was ALLOWED"
    assert "no_citation" in v.reasons, f"wrong reason: {v.reasons}"
    print(f"L2: ok (uncited refused: {v.reasons})")


def t_L2b_hallucinated_reporter_still_needs_url():
    """a plausible-looking reporter cite with no source_url is refused.

    This is the fabrication case: the citation reads correctly and there
    is nowhere to check it. The gate must not accept it."""
    d = good_opinion(citation=Citation(
        reporter="410 U.S. 113 (NEVER EXISTED)", pin_cite="125"))
    v = gate(d, DISK)
    assert not v.allow, "hallucinated reporter cite with no URL was ALLOWED"
    assert "unverifiable_cite" in v.reasons, f"wrong reason: {v.reasons}"
    print(f"L2b: ok (unverifiable cite refused: {v.reasons})")


def t_L3_jurisdiction_required():
    """no jurisdiction, no entry."""
    d = good_opinion(jurisdiction="")
    v = gate(d, DISK)
    assert not v.allow
    assert "no_jurisdiction" in v.reasons, f"wrong reason: {v.reasons}"
    d2 = good_opinion(jurisdiction="atlantis-federal")
    v2 = gate(d2, DISK)
    assert not v2.allow, "made-up jurisdiction was ALLOWED"
    assert any(x.startswith("unknown_jurisdiction") for x in v2.reasons)
    print(f"L3: ok (jurisdiction enforced: {v2.reasons})")


def t_L4_division_valid():
    """a division that isn't a real directory is refused."""
    d = good_opinion(division="wizard-law")
    v = gate(d, DISK)
    assert not v.allow
    assert any(x.startswith("unknown_division") for x in v.reasons)
    print(f"L4: ok (fake division refused: {v.reasons})")


def t_L5_license_recorded():
    """no license, no entry — we cannot ship what we cannot account for."""
    d = good_opinion(license="")
    v = gate(d, DISK)
    assert not v.allow
    assert "no_license" in v.reasons
    print("L5: ok (missing license refused)")


def t_L6_license_never_upgraded():
    """a CC-BY-NC-SA source may not be republished as CC-BY."""
    d = good_opinion(license="cc-by")
    d.extra["source_license"] = "cc-by-nc-sa"
    v = gate(d, DISK)
    assert not v.allow, "license upgrade was ALLOWED"
    assert any(x.startswith("license_upgrade") for x in v.reasons), v.reasons
    # and the reverse is fine: a PD source may be labeled cc-by
    d2 = good_opinion(license="cc-by")
    d2.extra["source_license"] = "public-domain"
    v2 = gate(d2, DISK)
    assert v2.allow, f"legitimate narrower license refused: {v2.reasons}"
    print(f"L6: ok (no license upgrade: {v.reasons})")


def t_L7_term_in_division():
    """terms must carry a definition and a source."""
    t = Term(term="Hearsay", division="litigation",
             definition="an out-of-court statement offered for truth",
             source="https://example.gov/rule801", license="public-domain")
    v = gate_term(t)
    assert v.allow, f"good term refused: {v.reasons}"
    bad = Term(term="", division="litigation", definition="", source="", license="")
    v2 = gate_term(bad)
    assert not v2.allow
    print(f"L7: ok (term gate: {[r for r in v2.reasons]})")


def t_L8_pin_cite_required_for_opinions():
    """an unpinned opinion cite is not citable."""
    d = good_opinion(citation=Citation(
        reporter="5 U.S. 137", pin_cite="",
        source_url="https://tile.loc.gov/..."))
    v = gate(d, DISK)
    assert not v.allow, "unpinned opinion was ALLOWED"
    assert "no_pin_cite" in v.reasons, v.reasons
    print("L8: ok (opinions need a pin-cite)")


def t_L9_bad_date_refused():
    d = good_opinion(doc_date="24 February 1803")
    v = gate(d, DISK)
    assert not v.allow
    assert any(x.startswith("bad_date") for x in v.reasons)
    print(f"L9: ok (non-ISO date refused: {v.reasons})")


def t_L10_taxonomy_covers_divisions():
    """every declared division is on disk and unique."""
    assert len(DIVISIONS) == len(set(DIVISIONS)), "duplicate division"
    for d in DIVISIONS:
        assert d in DISK, f"{d} declared but not scaffolded"
    print(f"L10: ok ({len(DIVISIONS)} divisions declared and scaffolded)")


def main():
    t_L1_repro_id()
    t_L2_citation_required()
    t_L2b_hallucinated_reporter_still_needs_url()
    t_L3_jurisdiction_required()
    t_L4_division_valid()
    t_L5_license_recorded()
    t_L6_license_never_upgraded()
    t_L7_term_in_division()
    t_L8_pin_cite_required_for_opinions()
    t_L9_bad_date_refused()
    t_L10_taxonomy_covers_divisions()
    print("\nALL FAR-LAW GATE TESTS PASS (L1..L10)")


if __name__ == "__main__":
    main()
