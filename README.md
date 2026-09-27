# far-law

**case law, statutes, contracts, briefs, opinions. Citation is the gate; argument is not.**

case law, statutes, contracts, briefs, opinions, legal templates, citation graphs, the legal-text pipeline.

## What this repo is

- A free, public-domain substrate for the legal-text pipeline.
- A gate (citation schema) that no document enters without sources.
- A growing library of cited opinions, contracts, and brief templates.

## What this repo is not

- A prompt collection. (Prompts are noise without citations.)
- A house-style. (The whole point is *named* jurisdiction + cited authority, not default voice.)
- A model zoo. (Models belong upstream; we use the open ones.)
- Legal advice. (This is a substrate and tooling. Use a lawyer.)

## AGENTS.md

The schema lives in [AGENTS.md](./AGENTS.md). Read it first. The
citation axes (jurisdiction, court, date, reporter, pin-cite) are the
contract.

## Repo layout

```
far-law/
├── AGENTS.md                # the citation schema (this is the contract)
├── README.md                # this file
├── LICENSE                  # MIT
├── CONTRIBUTORS.md          # who built this
├── opinions/                # cited opinions
├── contracts/               # contract templates
├── briefs/                  # brief templates
├── tools/                   # cite.compile + cite.gate
└── tests/                   # L1..L5 gate tests
```

## Quick start

```bash
git clone https://github.com/the-far-queen/far-law.git
cd far-law
# Read AGENTS.md
# Pick an opinion from opinions/
# Compile a variant: python tools/compile_cite.py path/to/opinion.yaml
# Gate: python tools/gate.py path/to/opinion.json
```

## License

MIT. Free for all agents, human and non-human. No copyright trap.
No paywall. No "research only" carve-out. Citations belong to everyone.

## Sister repos

the-far-queen/far-writing (voice substrate), the-far-queen/simself
(constitutional identity + kernel), the-far-queen/fieldcore (geometric
substrate). Far-law sits on top of far-writing: every legal document
is a voice with citation constraints.

## Status

Early scaffold. Schema, gate, and first opinion templates landing
in the next pass. Pull requests welcome — see CONTRIBUTORS.md.