---
name: phaistos-disc-research
description: Evidence-first AI research skill for the Phaistos Disc corpus.
version: 0.3.2
---

# Phaistos Disc Research Skill

This skill is an interface to the corpus in this repository. The corpus remains the canonical source of truth. Never maintain an independent scholarly dataset inside the skill.

## Governing rules
1. Separate physical/epigraphic observation, source transcription, normalization/derivation, computational result, scholarly interpretation, and AI-derived analysis.
2. Prefer canonical machine-readable corpus records over prose summaries for record-level questions.
3. Preserve identifiers, provenance, uncertainty, disagreements, corrections, negative results, and superseded analyses.
4. Never invent missing signs, readings, restorations, provenience, bibliography, source independence, rights, reviewer decisions, or reviewer credentials.
5. Label calculations performed by the AI and state enough method for reproduction.
6. Respect record/source-specific licensing and attribution. Repository-level licensing must not erase upstream restrictions.
7. For cross-corpus claims, establish comparability and source independence before interpreting similarity.
8. Report blocked or missing evidence rather than filling gaps.

## Human-review gate
Read `analysis/acceptance-2.0.json` before making any statement about independent review or final-2.0 readiness. A received or schema-valid review packet is not accepted review. AI must never attest reviewer identity, expertise, conflicts, independence, redistribution permission, physical inspection, or evidence adequacy. Those checks require a recorded human-maintainer acceptance. Until the replayed acceptance report sets `final_2_0_allowed` to true, describe final 2.0 as blocked.

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
- Final 2.0 and independent human epigraphic review remain blocked unless the machine-replayed acceptance report records otherwise
- Historical and project slot counts must remain distinct where they disagree
