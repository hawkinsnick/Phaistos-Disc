# Validation and AI research use

This guide documents existing verification boundaries; it does not certify new source observations or independent review.

## Reproducible local checks

From a checked-out repository, install the validation requirements and run:

```sh
python -m pip install -r requirements-validation.txt
python scripts/validate_current_state.py
python scripts/test_foundation.py
python scripts/build_corpus.py
```

Record the exact Git commit, Python version, command output and any failures when reporting results. A successful software check is not a scholarly acceptance decision.

## Evidence and interpretation boundaries

- The corpus concerns one physical object with two faces, not two independent documents.
- Its 61 graphical groups must not be silently interpreted as words.
- The project counts 242 graphical occurrence slots (241 identified and one erased/unknown), while the historical edition reports 241. Preserve the discrepancy rather than silently resolving it.
- Historical figure transcription, photographic comparison, stroke observations, computational results and interpretation are different evidentiary layers.
- No established phonetic decipherment or independent epigraphic certification follows from computational tests.

## Human review gate

Follow [final 2.0 acceptance](acceptance-2.0.md) and the [independent review brief](../reviews/independent-review-brief.md). Final 2.0 requires source-located human assessment, all occurrence ordinal/detail assessments, adequate physical-mark coverage evidence and documented independent-review verification. Do not manufacture review attestations or convert draft notes into accepted readings.

## AI skill and cross-corpus use

Read [the repository AI skill](../ai-skill/SKILL.md) and check `ai-skill/generated/source-state.json` before relying on generated research packages. Canonical corpus records take precedence over generated summaries. For combined-corpus comparisons, establish source independence and comparability first; fleet membership alone does not establish sign equivalence or linguistic affinity.

## Provenance and rights

Keep original evidence citations, uncertainty, exclusions and record-specific licensing attached to outputs. Do not redistribute modern copyrighted photographs or scholarly editions merely because project-original material is under noncommercial licenses.
