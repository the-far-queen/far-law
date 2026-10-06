# AGENTS.md — far-law (the citation contract)

> A legal claim without a citation is not a claim. It is a vibe.

This file is the contract. Every commit gate checks against it.
Every document references it. Every test reads it.

If you change the schema, update AGENTS.md first. The repo is
downstream of this file.

## What this repo is

A free, open-source **law school** for humans and for AI: cited
opinions, statutes, contracts, briefs, and the tools that keep them
honest. Organized by Yale Law School's academic divisions, because
those are the sharpest existing map of what legal scholarship actually
covers.

**Purpose: order.** The school is real — it teaches, it gates, it
refuses to take a student who cannot cite an authority. It is not a
university in the accreditation sense: no credits, no tuition, no
enrollment office, nothing for sale. What it produces is a substrate
that AI agents and the humans working with them can use directly.

The Yale divisions are borrowed as an organizational map. No Yale
material is reproduced and no Yale endorsement is implied.

## What this repo is NOT

- **Not a university.** No credits, no tuition, no accreditation, no
  enrollment. A school without a price.
- **Not legal advice.** This is a school and tooling. Use a lawyer.
- **Not a prompt collection.** Prompts are noise without citations.
- **Not a house style.** The point is *named jurisdiction + cited
  authority*, not a default voice.
- **Not a model zoo.** Models belong upstream; we use the open ones.

## Divisions (the taxonomy)

far-law is organized by Yale Law School's academic divisions. Each
division is a directory under `divisions/`. Each division carries its
own `terms/` (defined terms) and `sources/` (open textbooks).

```
divisions/
├── constitutional/     # constitutional law, federalism, courts
├── criminal/           # criminal law + procedure, sentencing
├── corporate/          # corporations, securities, M&A, governance
├── environmental/      # environmental + energy law
├── health/             # health law, bioethics, public health
├── intellectual-property/  # copyright, patent, trademark, trade secret
├── legislation-policy/ # statutory interpretation, legislation, policy
├── litigation/         # civil procedure, ADR, evidence
├── tax/                # tax law, estate & succession
├── commercial/         # contracts, commercial transactions, negotiable instruments
├── international/      # public international law, transnational
├── labor/              # employment, labor law
└── clinical/           # legal clinic, legal aid, public interest
```

## Packet

```
Opinion    opinion_id | jurisdiction | court | date | reporter | pin_cite | citations[]
Statute    statute_id | jurisdiction | code | section | title | year | source_url
Term       term_id    | division     | definition | citation | source
Contract   contract_id| jurisdiction | parties | clauses[] | governing_law
Brief      brief_id   | jurisdiction | court | issue | holdings[] | authorities[]
```

**No document without jurisdiction + citation.** The gate refuses naked
documents.

## Axes (the document contract)

| Axis | Type | Values |
|---|---|---|
| `jurisdiction` | enum | us-federal, us-state-{2-letter}, uk, eu, international, other |
| `court` | string | the deciding body (for judicial documents) |
| `date` | ISO-8601 | filing, decision, or effective date |
| `reporter` | string | official reporter citation (e.g. `410 U.S. 113`) |
| `pin_cite` | string | the specific page/section relied on |
| `division` | enum | one of the directories under `divisions/` |
| `source_url` | url | where the underlying text came from |
| `license` | enum | public-domain, cc-by, cc-by-sa, other |

## License rules per source class (load-bearing)

This repo is MIT, but MIT on **our own** material. It cannot relicense
someone else's copyrighted work. The gate records `license` per
document and refuses to place non-free material under our MIT blanket.

| Material | Status | Verdict |
|---|---|---|
| US Constitution | US government work | **SAFE** |
| US federal statutes (uscode.house.gov) | US government work | **SAFE** |
| US federal court opinions (govinfo.gov, CourtListener/RECAP) | US government work | **SAFE** |
| Caselaw Access Project (`case.law`) | verify current status | verify before use |
| Black's Law Dictionary (any edition) | Thomson Reuters, copyrighted | **NOT SAFE** |
| Restatement of the Law | ALI, copyrighted | **NOT SAFE** |
| OpenStax / MIT OCW / H2O / OpenLaw (CC-BY) | check per work | safe if CC-BY |
| LibreTexts | typically CC-BY-NC-SA | **NC + SA constrain use** |
| Yale's own casebooks | Yale University Press, copyrighted | **NOT SAFE** |

## Surface

```
cite.compile(document)
cite.gate(document)     # refuses naked documents
term.compile(division, term)
term.gate(term)
opinion.compile(axes)
```

## Gate

The gate checks:

1. `jurisdiction` is set and recognized
2. `citation` present and non-empty (or `source_url` for primary text)
3. `division` is a real directory under `divisions/`
4. `license` is recorded and is not a bare "unknown"
5. Date parses as ISO-8601
6. No document claims a license more permissive than its source

A naked document (no jurisdiction, no citation) is refused with reason
`no_jurisdiction` / `no_citation`.

## Tests

| # | Test | What it checks |
|---|---|---|
| L1 | repro id | same axes → same document id |
| L2 | citation required | document without citation is refused |
| L3 | jurisdiction required | document without jurisdiction is refused |
| L4 | division valid | division not on disk is refused |
| L5 | license recorded | document with no license is refused |
| L6 | license not upgraded | source license beats claimed license |
| L7 | term in division | term cites a definition that exists |
| L8 | pin-cite present | opinion without a pin-cite is refused |

## Anti-patterns

- unsourced legal assertions
- hallucinated citations (a plausible-looking reporter cite is worse
  than none — the gate exists to stop exactly this)
- one house voice across all jurisdictions
- copying a copyrighted dictionary into the repo
- AI-generated case summaries presented as the actual holding

## Related

- the-far-queen/far-writing/ — voice schema + voice.py
- the-far-queen/simself/ — constitutional identity + kernel
- the-far-queen/fieldcore/ — geometric substrate

## License

MIT for our own material. Third-party material retains its own
license, recorded per document. No copyright trap. No paywall.
