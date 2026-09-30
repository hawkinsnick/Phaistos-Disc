#!/usr/bin/env python3
"""Negative controls for evidence promotion, witness identity and contract drift."""
import json,pathlib,tempfile,shutil,hashlib
from validate_current_state import validate,R
assert validate()['status']=='PASS'
with tempfile.TemporaryDirectory() as td:
    root=pathlib.Path(td)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
    def reject(path,edit,reseal=False):
        q=root/path;raw=q.read_bytes();state=root/'analysis/current-status.json';state_raw=state.read_bytes()
        data=json.loads(raw);edit(data);q.write_text(json.dumps(data,ensure_ascii=False))
        if reseal:
            s=json.loads(state_raw)
            for e in s['evidence']:
                if e['path']==path:e['sha256']=hashlib.sha256(q.read_bytes()).hexdigest()
            state.write_text(json.dumps(s))
        try:
            validate(root)
        except Exception:pass
        else:raise AssertionError('Accepted corruption: '+path)
        finally:q.write_bytes(raw);state.write_bytes(state_raw)
    reject('signs/unicode-registry.json',lambda x:x[0].update(phonetic_value='a'),True)
    reject('corpus/disc.json',lambda x:x.update(object_count=2),True)
    reject('corpus/disc.json',lambda x:x['faces'][1].update(face_id='PD-001-A'),True)
    reject('corpus/disc.json',lambda x:x['faces'][0].update(reading_direction='clockwise'),True)
    reject('corpus/disc.json',lambda x:x.update(actual_sign_impression_total=241),True)
    reject('corpus/disc.json',lambda x:x['witnesses'].append({'witness_id':'w1','source_id':'invented','locator':'p1','verification_status':'source_checked','reading_direction':None,'starting_point':None}),True)
    reject('research/experiment-gates.json',lambda x:x['experiments'][0].update(claim_allowed=True),True)
    reject('research/experiment-gates.json',lambda x:x['experiments'][0].update(state='READY'),True)
    reject('research/family-compatibility-v1.json',lambda x:x['members'].remove('phaistos-disc'))
    reject('sources/sources.json',lambda x:x[0].update(subset_sha256='0'*64),True)
    reject('analysis/current-status.json',lambda x:x['committed_evidence_counts'].update(source_checked_occurrences=241))
    reject('analysis/current-status.json',lambda x:x['scientific_results'].update(decipherment_claim_allowed=True))
    assert validate(root)['status']=='PASS'
print(json.dumps({'status':'PASS','negative_controls':12,'recovery':'PASS'}))
