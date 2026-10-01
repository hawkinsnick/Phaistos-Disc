#!/usr/bin/env python3
"""Release-level adversarial checks: embedded data, readiness and declared scope."""
import hashlib,json,pathlib,re,shutil,tempfile
from validate_current_state import validate,R
from validate_family_readiness import validate as family_validate
from analyze import analyze
from export_corpus import export_records
assert validate()['status']=='PASS' and family_validate()['status']=='PASS'
html=(R/'workbench/index.html').read_text();match=re.search(r'<script id="edition-data" type="application/json">(.*?)</script>',html,re.S);assert match
embedded=json.loads(match.group(1).replace('<\\/','</'))
for key,path in [('corpus','corpus/disc.json'),('claims','apparatus/claims.json'),('frames','spatial/frames.json'),('anchors','spatial/group-anchors.json')]:assert embedded[key]==json.loads((R/path).read_text()),'workbench/native drift '+key
assert 'No translation' not in html or 'phonetic' in html
assert 'eval(' not in html and 'fetch(' not in html,'offline workbench must not require a server or eval data'
assert html.count('id="face"')==1 and html.count('id="direction"')==1
with tempfile.TemporaryDirectory() as td:
    root=pathlib.Path(td)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__','images','output'))
    p=root/'research/family-readiness-v1.json';raw=p.read_bytes()
    mutations=[lambda d:d.update(pooled_analysis_allowed=True),lambda d:d['linguistic_known_answer_control'].update(state='PASS'),lambda d:next(m for m in d['members'] if m['repository']=='Phaistos-Disc')['metrics']['physical_objects'].update(value=2),lambda d:next(m for m in d['members'] if m['repository']=='Linear-B')['metrics']['linguistic_gold'].update(value=0)]
    for mutate in mutations:
        d=json.loads(raw);mutate(d);p.write_text(json.dumps(d))
        try:family_validate(root)
        except Exception:pass
        else:raise AssertionError('family readiness accepted claim/unit promotion')
        p.write_bytes(raw)
    assert family_validate(root)['status']=='PASS'
assert analyze()==json.loads((R/'analysis/descriptive-v1.json').read_text()) and export_records()==json.loads((R/'exports/aegean-interop.json').read_text())
print(json.dumps({'status':'PASS','embedded_workbench_data':'EXACT','descriptive_replay':'EXACT','export_replay':'EXACT','family_negative_controls':4,'linguistic_gates':'BLOCKED'}))
