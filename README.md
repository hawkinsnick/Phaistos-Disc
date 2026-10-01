# Phaistos Disc — 0.3.0

A source-attributed research corpus and reproducible workbench within the five-member Aegean corpus family.

| Evidence | Committed coverage |
|---|---:|
| Physical objects | 1 |
| Faces of that object | 2 |
| Checked graphical witnesses | 1 published witness |
| Source-delimited graphical groups | 61 |
| Project-transcribed occurrence slots | 242 |
| Identified slots | 241 |
| Erased/unknown slots | 1 |
| Encoded repertoire | 45 base signs and a separate combining mark |

This is a project transcription of Evans's 1909 Figures128/129, checked against the numbered signary. It is not a new examination of the original object, an externally peer-reviewed critical edition or a decipherment. The historical edition reports a total241, while the project counts242 graphical slots in its figures. Both assertions remain visible. No phonetic values are assigned.

## Use the release

Download a versioned ZIP from [Releases](https://github.com/hawkinsnick/Phaistos-Disc/releases), extract it, and read the source, rights and evidence boundaries before analysis. Published ZIPs include faithful public-domain source-page images. Original sourcePDF and modern copyrighted editions are not bundled.

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

## Limits and remaining gates

Project visual review and separate software accounting are documented; no independent human epigraphic review has occurred. Stroke coverage is incomplete and source assertions conflict. The modern university codification contributes only attributed disagreement observations; its full transcription and PDF are not redistributed. Museum inventory metadata remains pending a full catalogue check after access failures.

Frequency summaries are conditional on this transcription. Software known-answer tests check arithmetic and reversible transforms; they do not replace LinearB linguistic gold. Cross-script inference, pooled analysis, stroke-semantic interpretation and decipherment remain blocked.

## Family alignment

LinearA, LinearB, Cypro-Minoan, Cretan hieroglyphic and Phaistos Disc share provenance, rights, unknown-value, interchange and gate contracts. Native identifiers remain separate. Membership asserts no linguistic affinity. Frozen historical baselines keep their original scope; current readiness is recorded separately.

## Rights and citation

Original code and project-created transcription records: MIT. Unicode-derived records: Unicode-3.0 (`licenses/Unicode-3.0.txt`). Historical Evans pages: public-domain edition, with author, publication and digitization attribution in `sources/sources.json`. These rights do not license modern museum photographs or scholarly editions. See `CITATION.cff` and cite the original evidence used.

See `releases/` for milestone-specific scope and acceptance records. The next evidence milestone is external epigraphic review plus additional checked witnesses, keeping unresolved disagreements intact.
