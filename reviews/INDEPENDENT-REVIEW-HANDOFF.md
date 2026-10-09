# Independent epigraphic review handoff

This packet is for a qualified independent human reviewer. It does **not** ask the reviewer to endorse a decipherment, linguistic affiliation, phonetic values, or the project's conclusions.

## What must be reviewed
1. Inspect all 242 stable occurrence IDs in `reviews/occurrence-review-sheet.tsv`.
2. Record an ordinal assessment and fine-detail assessment for every occurrence, with source locator(s) and notes sufficient to understand the decision.
3. Inspect all 61 groups in `reviews/group-mark-review-sheet.tsv`.
4. For each group, distinguish `source_resolution_limited` from `physical_coverage_supported`. Do not infer physical absence from an empty visible-mark list.
5. State the sources actually inspected. Existing project references are navigation aids, not proof that the reviewer inspected them.
6. State name, affiliation (if any), relevant expertise, conflicts, independence, and whether the review record may be redistributed.

## No-code workflow
The reviewer may return the completed TSV sheets plus a signed plain-text/PDF report keyed to stable IDs. The reviewer does not need Git, Python, JSON, or a GitHub account. A maintainer may transcribe that material into a V2 submission **without changing the substance**, retain the original report, and obtain reviewer approval of the structured transcription.

For a structured submission, generate the canonical V2 template with:

`python scripts/review_acceptance.py --template > reviews/submissions/reviewer.json`

Validate before acceptance with:

`python scripts/review_acceptance.py --submission reviews/submissions/reviewer.json`

## Acceptance boundary
A schema-valid file is not accepted review. A human maintainer must separately verify reviewer identity, relevant expertise, conflicts, independence, redistribution permission, and physical-evidence adequacy, then create `reviews/accepted-review.json` from `reviews/acceptance-record-template.json`.

Final 2.0 remains blocked unless the machine-replayed acceptance report confirms all 242 ordinal/detail assessments, all 61 group assessments, adequate physical coverage, and the recorded human verification.