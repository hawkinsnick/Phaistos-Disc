---
name: phaistos-disc-research
description: Evidence-first AI research skill for the Phaistos Disc corpus.
version: 0.3.1
---

# Phaistos Disc Research Skill

This skill is an interface to the corpus in this repository. The corpus remains the canonical source of truth. Never maintain an independent scholarly dataset inside the skill.

## Governing rules
1. Separate physical/epigraphic observation, source transcription, normalization, computational derivation, scholarly interpretation, and AI-derived analysis.
2. Prefer canonical machine-readable corpus records over prose summaries for record-level questions.
3. Preserve identifiers, provenance, uncertainty, disagreements, corrections, negative results, and superseded analyses.
4. Never invent missing signs, readings, restorations, provenience, bibliography, source independence, or rights.
5. Label calculations performed by the AI and state enough method for reproduction.
6. Respect record/source-specific licensing and attribution. Repository-level licensing must not erase upstream restrictions.
7. For cross-corpus claims, establish comparability and source independence before interpreting similarity.
8. Report blocked or missing evidence rather than filling gaps.

## Corpus-specific caution
Unique/limited-context artifact: avoid treating sign recurrence, directionality assumptions, segmentation, or proposed parallels as decipherment or independent linguistic confirmation.

## Default research response
Give the direct answer, followed as relevant by Evidence; Evidentiary status; Uncertainty/limitations; Reproducibility; Rights/attribution.

## Synchronization
Read `ai-skill/generated/source-state.json` before substantive work. It records the corpus commit from which the AI-facing package was synchronized. Generated files are rebuildable views; canonical corpus files govern if a discrepancy is found.

## Academic-scrutiny gates
- One physical object with two faces is not two independent documents
- Graphical groups are not assumed to be words
- No phonetic values or decipherment are established
- Final 2.0 and independent human epigraphic review remain blocked
- Historical and project slot counts must remain distinct where they disagree


## Offline corpus browser
Run `python scripts/build_corpus_browser.py` to generate `workbench/corpus-browser.html`. The browser is self-contained and searches only the explicitly allowlisted files in `research/browser-sources.json`. Adding a file to the browser requires a rights/provenance check; never recursively ingest repository data or restricted upstream material. Browser display does not establish decipherment, source independence, or expert validation.

## Validation and AI-use documentation
Before reporting validation or scholarly readiness, consult `research/validation-and-ai-use.md` alongside `research/acceptance-2.0.md`. Distinguish reproducible software checks from independently verified epigraphic assessment; record the repository commit and command results. Preserve the 241 historical versus 242 project slot-count discrepancy, source dependencies and rights boundaries in all AI-facing summaries.

## Evidence-denominator policy
Always distinguish the historical 241 assertion from the project's 242 graphical slots. State the unit and witness dependence for any statistic; do not infer linguistic words from graphical groups or scientific acceptance from reproducible checks. Apply the final 2.0 review and physical-evidence gates in `research/acceptance-2.0.md`.

## Human-review gate
Read `analysis/acceptance-2.0.json` before making any statement about independent review or final-2.0 readiness. A received or schema-valid review packet is not accepted review. AI must never attest reviewer identity, expertise, conflicts, independence, redistribution permission, physical inspection, or evidence adequacy. Those checks require a recorded human-maintainer acceptance. Until the replayed acceptance report sets `final_2_0_allowed` to true, describe final 2.0 as blocked.


## Enforced assertion, dependency and bundle integrity

Read `docs/AI-INTEGRITY.md` and the required `research/cross-corpus-dependencies.json` before source counts or cross-corpus analysis. Use qualified assertion views when provided; original source literals must travel with their reconciliation, uncertainty and identity context. The dependency register does not certify physical identity or linguistic affinity. Shared catalogue references and duplicated digital sources are not independent witnesses. Missing links mean unknown, not independent. `scripts/check_cross_corpus_dependencies.py` screens declared record selections and rejects pooled physical/witness counts and phonetic transfer. Native AI bundle validation checks the dependency projection and local evidence hashes. Bundle publication validates the exact source parent and never rebases or force-pushes the validated artifact. Software and packaging checks do not establish expert or model-behavior acceptance.

## Corpus-native evidence and alternatives

Read `docs/EVIDENCE-AND-ALTERNATIVES.md`, `research/evidence-query-profile.json` and `analysis/evidence-query-coverage.json` for evidence or competing-reading questions. Use `scripts/evidence_query.py` with exact native IDs and an explicit collection when ambiguous. Preserve `native_record`, every uncertainty/editorial mark, source attribution, locator, inspection status and rights. Cite artifact path, JSON pointer and SHA-256; hashes certify bytes only. Treat explicitly linked records as declared ID associations, not physical certification or independent witnesses. Context resources have corpus-level scope and are not automatically about the queried record. Distinguish a named source reading from a legacy queue label, uninspected bibliographic lead, count convention or hypothesis. Do not infer a count of collated alternative pairs or independent witnesses from searchable rows; those metrics remain unknown. Report the native units and scope of each view separately, and defer to the corpus-specific limits. No new readings, expert acceptance or decipherment follows from this interface.
