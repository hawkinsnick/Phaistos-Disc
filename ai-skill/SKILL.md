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
