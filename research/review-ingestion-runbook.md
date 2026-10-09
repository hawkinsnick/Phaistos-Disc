# Human review ingestion runbook

This procedure preserves the distinction between a received review, a valid structured submission, and an accepted independent review.

## 1. Preserve the original
Store the reviewer-returned material without rewriting its claims. Record its provenance and obtain explicit permission before redistributing copyrighted reviewer material.

## 2. Structure without embellishment
Create a V2 packet with `python scripts/review_acceptance.py --template`. Transcribe only what the reviewer actually reported. Missing observations remain unreviewed/unassessed. Do not convert project-derived observations into reviewer observations.

## 3. Validate mechanically
Run `python scripts/review_acceptance.py --submission <packet>`. The validator checks corpus/hash binding, exact occurrence/group membership, source identities, source locators, decision types, and coverage semantics. Passing this step means **structurally valid submission**, not scientific acceptance.

## 4. Human acceptance
A human maintainer verifies identity, expertise, conflicts, independence, redistribution permission, and adequacy of physical evidence. Only then may the maintainer create `reviews/accepted-review.json`, pinned to the exact submitted packet bytes.

## 5. Replay the gate
Run the repository validation suite. `analysis/acceptance-2.0.json` is authoritative for the release gate. Final 2.0 is allowed only when its replayed state says so.

## Non-negotiable safeguards
- Never infer a missing reviewer decision.
- Never mark source-limited imagery as physical-coverage support.
- Never treat a second reproduction of the same witness as an independent object.
- Never let AI attest identity, expertise, independence, or physical inspection.
- Never translate review completion into a decipherment or linguistic claim.
- Preserve disagreements and negative findings.