# Phaistos Disc — 1.6.0

A source-attributed research corpus and reproducible workbench within the five-member Aegean corpus family.

| Evidence | Committed coverage |
|---|---:|
| Physical objects | 1 |
| Faces of that object | 2 |
| Checked graphical witnesses | 1 published graphical baseline |
| Project-compared photographic witnesses | 1 newer photographic acquisition |
| Source-delimited graphical groups | 61 |
| Project-transcribed occurrence slots | 242 |
| Identified slots | 241 |
| Erased/unknown slots | 1 |
| Encoded repertoire | 45 base signs and a separate combining mark |

This is a project transcription of Evans's 1909 Figures128/129, checked against the numbered signary. It is not a new examination of the original object, an externally peer-reviewed critical edition or a decipherment. The historical edition reports a total241, while the project counts242 graphical slots in its figures. Both assertions remain visible. No phonetic values are assigned.

## Use the release

Download a versioned ZIP from [Releases](https://github.com/hawkinsnick/Phaistos-Disc/releases), extract it, and read the source, rights and evidence boundaries before analysis. Published ZIPs include faithful public-domain source-page images. Original sourcePDF and modern copyrighted editions are not bundled.

Open `workbench/index.html` directly in a browser for face/group navigation and source-linked records. It works without a server.

## Reproduce the checks

```sh
python -m pip install -r requirements-validation.txt
python scripts/validate_current_state.py
python scripts/test_foundation.py
python scripts/build_corpus.py
```

The source ledger, raw numeric transcription and review records have explicit SHA256 identities. The builder preserves native Evans labels A1–A31/B1–B30 while its declared project traversal runs outer-to-inner. Traversal can be reversed; it is not a linguistic reading conclusion. Graphical groups are not assumed words. Faces are not independent documents, and editions sharing photographs are not independent objects.

To acquire exact primary-source bytes and render checked historical pages (requires Poppler's `pdftoppm`):

```sh
python scripts/fetch_primary_sources.py --cache /tmp/phaistos-primary --render
```

A source-byte mismatch stops acquisition; pins are never updated automatically. Native glyph coordinates remain unknown. Where group anchors are provided, they locate approximate group labels in historical drawings, not physical stamp centroids, millimetres or object measurements.

## Available layers

- Source-critical apparatus and separate stroke assertions
- 61 approximate source-figure group anchors
- Descriptive statistics and sensitivity to traversal/unknown readings
- Five-member comparison-readiness report
- Validated interchange and CSV exports
- Offline research workbench with per-group photographic comparisons and exemplar IDs
- Four explicit source-assertion sensitivity scenarios

## Limits and remaining gates

Project visual review and separate software accounting are documented; no independent human epigraphic review has occurred. All 61 Olivier group panels have a bounded project comparison and stroke inspection record. Fine-detail certification, complete physical mark coverage and source conflicts remain unresolved. The modern university codification contributes only attributed disagreement observations; its full transcription and PDF are not redistributed. Museum inventory metadata remains pending a full catalogue check after access failures.

Frequency summaries are conditional on this transcription. Software known-answer tests check arithmetic and reversible transforms; they do not replace LinearB linguistic gold. Cross-script inference, pooled analysis, stroke-semantic interpretation and decipherment remain blocked.

## Family alignment

LinearA, LinearB, Cypro-Minoan, Cretan hieroglyphic and Phaistos Disc share provenance, rights, unknown-value, interchange and gate contracts. Native identifiers remain separate. Membership asserts no linguistic affinity. Frozen historical baselines keep their original scope; current readiness is recorded separately.

## Rights and citation

Original code and project-created transcription records: MIT. Unicode-derived records: Unicode-3.0 (`licenses/Unicode-3.0.txt`). Historical Evans pages: public-domain edition, with author, publication and digitization attribution in `sources/sources.json`. These rights do not license modern museum photographs or scholarly editions. See `CITATION.cff` and cite the original evidence used.

See `releases/` for milestone-specific scope and acceptance records. The next evidence gate is independent epigraphic review; see `reviews/independent-review-brief.md`. The photograph comparison and source-exemplar crosswalk are under `reviews/` and `signs/`.

1.2.1 aligns the shared family evidence report with the checked companion milestones, including the first two-object CHIC source-access pilot. Corpus readings, photographic audit and sensitivity results retain their prior bytes and scope.

## Milestone 1.3.0

Adds a source-linked evidence row for every one of the 242 native slots. Forty-six labeled photographic exemplars are distinguished from 196 ordinals not individually certified. Native readings and all unknown, position and review boundaries remain unchanged.

## Milestone 1.4.0

Adds a typed, replayable eight-source coverage ledger: encoding standards, historical baseline, bounded photographic comparison, dependent assertions and context evidence remain distinct. Preserves the Pernier volume/imprint/catalogue date conflict and unresolved photographic lineage. Museum pages still return HTTP 502; no metadata is invented.

## Milestone 1.5.0

Adds a retrospectively registered, byte-pinned descriptive suite with exact group repetition and adjacent-repeat counts, unknown exclusions, reversible group views, and 1000 deterministic within-face shuffle references. Graphical lengths, per-face glyph counts and unknown positions are preserved. No p-values, population confidence intervals or linguistic inference are produced.

## Milestone 1.6.0

Adds a complete 242-slot review draft, attributed submission validator and offline occurrence-note editor. Draft import/export preserves stable native IDs under view reversal and rejects source hash, missing-slot and review-state tampering. Submitted decisions are never automatically accepted as independent review or applied to native readings.
