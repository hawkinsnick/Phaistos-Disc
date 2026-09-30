# Phaistos Disc — 0.1.0

An evidence-first foundation for the Phaistos Disc, the fifth member of the Aegean corpus research family. This release supplies a native data model and executable integrity gates.

## Committed evidence

| Layer | Coverage |
|---|---|
| Object scaffold | 1 physical object; 2 editorial faces |
| Unicode repertoire | 45 base signs; 1 separate combining oblique stroke |
| Checked transcription witnesses | 0 |
| Checked sign occurrences | 0 |
| Actual impression count | Unknown in this release |

The Unicode 17 repertoire is derived from authenticated UnicodeData bytes. Standard sign names describe encoding labels; they do not supply phonetic or semantic readings. PD-U identifiers refer to code points, without assuming equivalence to another edition's sign numbering.

The museum catalogue identifier Π-Ν1358 comes from primary-publisher search metadata. Both catalogue and exhibit page retrievals returned HTTP 502 on 2026-09-30; their full records remain unchecked. No museum image or edition transcription is bundled.

## Validate

```sh
python -m pip install -r requirements-validation.txt
python scripts/validate_current_state.py
python scripts/test_foundation.py
```

CI runs both commands. The validator recomputes the Unicode registry from the checked subset, checks source hashes and licenses, validates schemas and references, recomputes evidence counts and rejects gate leakage. Tests deliberately corrupt provenance, signs, object independence, evidence digests and gate flags.

The subset can be reproduced from externally downloaded, digest-checked Unicode 17 data:

```sh
python scripts/extract_unicode_subset.py --source /path/to/UnicodeData.txt --out /tmp/phaistos-subset.txt
```

## Evidence model

`corpus/disc.json` holds one object with faces A/B as editorial labels awaiting alignment to a checked witness. A face is not an independent document. Reading direction and starting point are unknown until attributed to a witness. No synthetic coordinates are generated.

Each future occurrence requires a face, witness, sequence index, sign or uncertainty alternatives and a source locator. Coordinates require an image source, frame, locator and measurement method. Marked groups carry separator assertions; they are not automatically words. Corrections and competing readings belong to witness-specific assertions. The oblique stroke is a combining mark, not a 46th base sign.

## Family boundary

Linear A, Linear B, Cypro-Minoan, Cretan hieroglyphic and Phaistos Disc retain separate native identifiers and evidence. Contract 1.1 adds membership and an interchange project identifier; it makes no claim of linguistic relationship and authorizes no pooled analysis. Existing four-member baselines remain historical artifacts.

## Next milestone: 0.2

Acquire a checkable primary transcription witness and rights statement, align its face/sign numbering, encode source-located occurrences and marked groups, review disagreements independently, then open the transcription release gate. Keep incompatible witnesses separate. Arkalochori and other proposed comparanda require their own objects and explicit relationship claims; they are not silently incorporated into this native corpus.

Code and original project contributions: MIT. Unicode-derived records: Unicode-3.0. See `sources/sources.json` and `licenses/` for source-specific rights.
