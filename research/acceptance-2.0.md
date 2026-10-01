# Final 2.0 acceptance

The final 2.0 milestone remains the independently reviewed critical edition
proposed in the roadmap. The 2.0.0-rc.2 prerelease packages the tools and evidence
prepared toward it. Version numbers do not replace missing review.

Final acceptance requires a completed source-located review of all native slots,
within-group ordinal assessment beyond the 46 published exemplars, fine-detail
and physical-mark coverage assessment, and an explicit account of unresolved
observations. Supported uncertainty is retained; agreement with the project is
not required. Assessments must state the limits of the available photographs.

A human maintainer must verify reviewer identity, relevant epigraphic expertise,
conflicts and independence, then commit the attributed report and a documented
acceptance decision. A self-declaration or a schema-valid JSON file does not
establish independence. The preparation agent cannot perform that verification
or act as an independent epigraphic reviewer.

Use `reviews/independent-review-brief.md` and `reviews/review-packet-v2.json`.
The command `python scripts/review_acceptance.py --submission submission.json` checks
format, source hashes, stable slot membership, all 61 mark-assessment groups and
required attribution and review-record license. It never
adopts corrections or accepts a person as an independent reviewer. Preserve submitted reports and
their original bytes; reconcile accepted changes as separately attributed
assertions before changing any native reading.

`analysis/acceptance-2.0.json` records current readiness and blockers. CI tests
the candidate package, source acquisition, replay, negative controls and browser
workflow. These checks establish software behavior, not human review completion.

The v1 editor remains a draft-note tool. V2 adds source-evidence identities and
one physical-mark coverage assessment for every graphical group. An assessment
limited by source resolution remains distinct from supported physical coverage;
an empty observed-mark list is not evidence that marks are absent.

After actual human verification, a human maintainer may commit the original
review bytes under `reviews/submissions/` and create `reviews/accepted-review.json`
using `reviews/acceptance-record-template.json`. The template is intentionally
invalid for acceptance: no person, permission or verification is pre-certified.
Record identity, expertise, conflicts, independence, redistribution permission,
evidence adequacy and acceptance timing in the verification record. A reviewer
cannot attest their own independence. The packet must declare a permitted record
license; this does not license redistribution of its source photographs.

`python scripts/review_acceptance.py` evaluates the committed receipt against
the exact submitted bytes. `scripts/acceptance_2.py` then computes the gate states
from that evidence. Update the experiment gate and current-status evidence pins
to the resulting states, rerun the full checks and publish final 2.0 only if all
requirements pass. Final `VERSION=2.0.0` is rejected without complete recorded
acceptance. No corrections are automatically applied to the native corpus.

The receipt replays a human-maintainer attestation. The software does not prove
identity or expertise electronically. The preparation agent must not create a
receipt pretending that an external person reviewed the corpus. Synthetic
positive/negative tests live only in temporary test fixtures, not production
review records.
