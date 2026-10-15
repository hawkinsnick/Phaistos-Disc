# Attribution review

All seven claims distinguish erased-sign conjecture, sign/mark differences, same-source discrepancies, arithmetic scope and traversal hypotheses.

Existing source consultation receipts and limits are inherited exactly from the referenced native packets. This pass inspects those packets, not the underlying publications afresh. No exhaustive literature search, new autopsy or independent review is claimed.

The complete selections below name the finite native collections reviewed. Other repository records and the broader literature are outside this checkpoint. Case counts are review tasks, not inscriptions, independent witnesses or fully attributed alternative pairs.

| Complete native selection | Rows |
|---|---:|
| `apparatus/claims.json` | 7 |

Use the case query to read the finding together with the complete native evidence, including any named author/publication, source locator, inspection state, qualification and source dependence. Missing metadata stays missing; a source ID alone is not proof of direct consultation.

```sh
python scripts/attribution_review.py --check
python scripts/attribution_review.py --case 'PD-C001'
python scripts/evidence_query.py --list attribution-review
```

| Review ID | Type | Finding | Remaining work |
|---|---|---|---|
| PD-C001 | READING_COMPARISON | The proposed erased sign remains a question-marked conjecture, not a baseline reading. | Check graphic locus and source author identity through sources.json; the erased slot remains null. |
| PD-C002 | READING_COMPARISON | HMU sign25 and the project figure reading07 are different assertions at the declared group/slot. | Confirm counting convention and graphic alignment before treating this as a fully collated sign dispute. |
| PD-C003 | READING_COMPARISON | The same HMU source differs between overview and detail on an underscore. | Omission from a drawing is not physical absence; inspect both representations and mark alignment. |
| PD-C004 | READING_COMPARISON | Evans’s footnote target does not occur in the project figure-derived group. | Align footnote numbering and figure/signary conventions before moving or inventing an occurrence. |
| PD-C005 | COUNT_OR_IDENTITY | Evans’s stated15 and face counts9+7 have an unresolved inclusion/arithmetic scope. | Keep the possible A25 inferred stroke separate; do not force agreement by changing a count. |
| PD-C006 | INTERPRETATION | Evans’s center-to-outer proposal is a source-attributed traversal hypothesis. | Reconcile argument and physical production sequence independently of reversible project traversal. |
| PD-C007 | INTERPRETATION | The Unicode proposal reports a reading consensus and separately specifies exchange directionality. | Encoding left-to-right does not determine ancient physical or linguistic reading direction. |

`research/attribution-review.json` pins every referenced native artifact by SHA-256 and records exact JSON pointers. `analysis/attribution-review-audit.json` is replayed by the checker. Queries reject changed input bytes before returning any case. The earlier native records remain unchanged.

Pair-attribution states describe documentary limitations, not scientific acceptance. A partial located comparison can be a real scholarly alternative without full typographic, physical-position or independent collation. `NOT_APPLICABLE` marks controls and interpretations for which a two-reading pair is not the appropriate unit. No unknown pair/witness total is replaced with zero.
