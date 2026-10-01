# Research evidence workbench 1.0

This is an engineering milestone for Phaistos-Disc. Existing scientific gates remain in force.

## Open without coding

Download and extract the research workbench release ZIP, then open `workbench/evidence.html` in your browser. Everything shown is embedded locally. Publisher links open external sources only when you choose them. Search the pinned files, select a category, and open a record to inspect its actual source references and rights statements. The index covers current-status evidence; it is not the complete corpus or all historical files.

Metric units and definitions are shown together. Unknown remains unknown. Counts of catalogue entries, conventional phonetic transcriptions, physical objects and source-checked readings are different quantities. Each project remains separate.

## Review and corrections

Use “Record an inspection note” to record an evidence path or stable native ID, a source locator, what you observed and any uncertainty. Download the note before closing the page. Its evidence-index hash identifies the inspected snapshot. Notes are unverified observations and cannot open scientific gates. You can submit a correction through a GitHub issue yourself; no message is sent automatically.

A reviewer may supply a plain written report with stable IDs and source locations. Maintainers can convert a real review into the appropriate structured format while preserving the original report and getting the reviewer’s approval. Reviewers do not need to write code or edit JSON. Expert identity, expertise, independence and permission to publish their review must be checked before attribution.

## Reproduce the build

With Python installed, run `python scripts/evidence_workbench.py` to check committed outputs, or `python scripts/evidence_workbench.py --write` to rebuild them. `python scripts/test_evidence_workbench.py` tests tampering and embedding controls. Browser tests run in GitHub Actions. Hash agreement proves byte identity, not scientific correctness.

## Disc comparison and sensitivity

The ledger has all 242 native slots. Evans provides the project’s numbered-figure transcription. Olivier provides inherited group-level photographic comparison and 46 labeled exemplar mappings; this does not certify every ordinal or fine stamp detail. Two HMU reading disagreements are recorded, with no claim of a complete HMU comparison. No new photographic inspection is asserted by this milestone.

Select the erased A24 slot as unknown or one of 45 base signs, B3 slot 5 as native 07 or the attributed 25, and reverse group/within-group order independently. These 368 descriptions preserve native bytes. Bounds cover only this declared hypothesis space. They are not probabilities, population intervals, a best reading or evidence of decipherment. Boundary-crossing bigrams and physical stroke semantics are excluded.

Open `workbench/index.html` for the historical figure viewer. The native release ZIP includes five public-domain Evans renders. Modern publisher photographs remain external links, with no redistribution license implied.

## Review sheets without coding

Open `reviews/occurrence-review-sheet.tsv` and `reviews/group-mark-review-sheet.tsv` in a spreadsheet application, or read them as text. All 242 occurrences and 61 groups have stable IDs. Fill in observations with source locators and a written account of your method. The sheets start unreviewed/unassessed. Existing source references are navigation aids, not records of your inspection.

For marks, report whether the evidence can support examining the entire group. An empty observed-mark list does not prove physical absence. Distinguish a source-resolution limitation from supported coverage. Final epigraphic 2.0 still needs the recorded human acceptance procedure in `research/acceptance-2.0.md`.
