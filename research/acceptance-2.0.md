# Final 2.0 acceptance

The final 2.0 milestone remains the independently reviewed critical edition
proposed in the roadmap. The 2.0.0-rc.1 prerelease packages the tools and evidence
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

Use `reviews/independent-review-brief.md` and `reviews/review-packet-v1.json`.
The command `python scripts/review_packet.py --validate submission.json` checks
format, source hashes, stable slot membership and required attribution. It never
adopts corrections or opens a scientific gate. Preserve submitted reports and
their original bytes; reconcile accepted changes as separately attributed
assertions before changing any native reading.

`analysis/acceptance-2.0.json` records current readiness and blockers. CI tests
the candidate package, source acquisition, replay, negative controls and browser
workflow. These checks establish software behavior, not human review completion.
