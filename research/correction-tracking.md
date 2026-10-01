# Correction tracking

Compare two local Git revisions without editing the corpus or opening scientific gates:

```sh
python scripts/release_change_ledger.py --baseline research-workbench-v1.0.0 --target HEAD --output output/release-change-ledger.json
```

Run this in a Git checkout with both revisions available (`git fetch --tags` when needed). An extracted release ZIP has no history: use the repository checkout for this tool. The JSON records immutable commit IDs, all changed tracked paths, file hashes and exact JSON object changes. The companion Markdown gives a readable file inventory. CI publishes both reports as artifacts on each change.

Arrays are replaced as a whole: their order can matter, and this generic tool does not guess stable scientific identities. Whitespace-only JSON changes remain visible as changed bytes but have no JSON value changes. Additions and deletions retain null hashes on the absent side. File modes and submodule commit changes are included. Paths classify navigation only; reviewers must assess whether a change is scientifically meaningful. This is correction tracking, not correction approval. Reports may contain source material from the compared commits; apply the original rights restrictions before sharing them.
