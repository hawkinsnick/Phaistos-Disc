#!/usr/bin/env python3
"""Replay deterministic local research products without asserting scholarly truth."""
import argparse,hashlib,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1]
CHECKS=[
 ("native","scripts/validate_current_state.py"),
 ("foundation","scripts/test_foundation.py"),
 ("analysis","scripts/test_analysis.py"),
 ("exports","scripts/test_exports.py"),
 ("witness","scripts/test_witness_audit.py"),
 ("apparatus","scripts/test_apparatus_sensitivity.py"),
 ("family","scripts/validate_family_readiness.py"),
 ("occurrences","scripts/test_occurrence_audit.py"),
 ("coverage","scripts/test_source_coverage.py"),
 ("research","scripts/test_research_suite.py"),
 ("review-draft","scripts/test_review_packet.py"),
 ("acceptance","scripts/test_acceptance_2.py"),
 ("human-review-gate","scripts/test_review_acceptance.py"),
 ("evidence-workbench","scripts/test_evidence_workbench.py"),
 ("edition-workbench","scripts/test_edition_workbench.py"),
 ("correction-ledger","scripts/test_release_change_ledger.py"),
]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):
    results=[]
    for name,rel in CHECKS:
        p=R/rel
        if not p.exists(): continue
        q=subprocess.run([sys.executable,str(p)],cwd=R,text=True,capture_output=True)
        results.append({"name":name,"path":rel,"status":"PASS" if q.returncode==0 else "FAIL","stdout":q.stdout[-2000:],"stderr":q.stderr[-2000:]})
        if q.returncode: break
    return results
def main():
    p=argparse.ArgumentParser();p.add_argument("--json",action="store_true");a=p.parse_args()
    results=run(a)
    tracked=["corpus/disc.json","analysis/current-status.json","analysis/acceptance-2.0.json","analysis/research-suite-v2.json","exports/aegean-interop.json","reviews/review-packet-v2.json"]
    report={"format":"PD-reproducibility-report-v1","version":(R/"VERSION").read_text().strip(),"all_local_checks_pass":all(x["status"]=="PASS" for x in results),"checks":results,"artifact_sha256":{x:sha(R/x) for x in tracked if (R/x).exists()},"boundaries":["Local replay verifies deterministic software/artifact consistency, not epigraphic truth.","Authenticated primary-source acquisition is separately exercised by CI.","Human review and physical evidence adequacy cannot be reproduced by software."]}
    if a.json: print(json.dumps(report,indent=2))
    else:
        for x in results: print(f'{x["status"]:4} {x["name"]}: {x["path"]}')
        print("PASS" if report["all_local_checks_pass"] else "FAIL")
    raise SystemExit(0 if report["all_local_checks_pass"] else 1)
if __name__=="__main__":main()
