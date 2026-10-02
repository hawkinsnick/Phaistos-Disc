#!/usr/bin/env python3
"""Audit rights/provenance declarations without expanding any license."""
import json,pathlib,re,sys
R=pathlib.Path(__file__).resolve().parents[1]; errors=[]
sources=json.loads((R/"sources/sources.json").read_text())
for s in sources:
    sid=s.get("source_id","<missing>")
    if not s.get("record_license"): errors.append(f"{sid}: missing record_license")
    if not (s.get("citation") or s.get("title") or s.get("publication_title")): errors.append(f"{sid}: missing citation/title")
    for key in ("subset_path","license_path","manifest_path"):
        if s.get(key) and not (R/s[key]).is_file(): errors.append(f"{sid}: missing {key} {s[key]}")
exports=json.loads((R/"exports/aegean-interop.json").read_text())
for i,r in enumerate(exports):
    rights=r.get("rights")
    if not isinstance(rights,dict) or not rights.get("record_license"): errors.append(f"interop[{i}]: missing record license")
    if not r.get("assertions") or any(not a.get("provenance") for a in r.get("assertions",[])): errors.append(f"interop[{i}]: missing assertion provenance")
matrix=(R/"DATA-LICENSE-MATRIX.md").read_text()
for required in ["Unicode","Evans","Olivier"]:
    if required.lower() not in matrix.lower(): errors.append("license matrix missing "+required)
readme=(R/"README.md").read_text()
if "These rights do not license modern museum photographs or scholarly editions." not in readme: errors.append("README upstream-rights boundary missing")
report={"format":"PD-rights-provenance-audit-v1","sources_checked":len(sources),"interop_records_checked":len(exports),"status":"PASS" if not errors else "FAIL","errors":errors,"boundary":"This audit checks declared provenance/rights plumbing; it is not legal advice and does not grant rights absent from upstream sources."}
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
