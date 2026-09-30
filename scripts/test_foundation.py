#!/usr/bin/env python3
"""Adversarial checks of the current source-attributed edition."""
import json,pathlib,tempfile,shutil,hashlib
from validate_current_state import validate,R
assert validate()['status']=='PASS'
checks=0
with tempfile.TemporaryDirectory() as td:
    root=pathlib.Path(td)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__','images','output'))
    def reject(path,edit,reseal=True):
        global checks
        q=root/path;raw=q.read_bytes();state=root/'analysis/current-status.json';state_raw=state.read_bytes();data=json.loads(raw);edit(data);q.write_text(json.dumps(data,ensure_ascii=False))
        if reseal and q!=state:
            s=json.loads(state_raw)
            for e in s['evidence']:
                if e['path']==path:e['sha256']=hashlib.sha256(q.read_bytes()).hexdigest()
            state.write_text(json.dumps(s))
        try:validate(root)
        except Exception:checks+=1
        else:raise AssertionError('Accepted corruption: '+path)
        finally:q.write_bytes(raw);state.write_bytes(state_raw)
    reject('signs/unicode-registry.json',lambda x:x[0].update(phonetic_value='a'))
    reject('signs/evans-unicode-crosswalk.json',lambda x:x['entries'][0].update(sign_id='PD-U101D1'))
    reject('corpus/disc.json',lambda x:x.update(physical_objects=2))
    reject('corpus/disc.json',lambda x:x['faces'][0].update(independent_document=True))
    reject('corpus/disc.json',lambda x:x['faces'][0].update(reading_direction='certain_clockwise'))
    reject('corpus/disc.json',lambda x:x['occurrences'][0].update(sign_id='PD-U101FF'))
    reject('corpus/disc.json',lambda x:next(o for o in x['occurrences'] if o['sign_id'] is None).update(sign_id='PD-U101E3',uncertainty='source_legible'))
    reject('corpus/disc.json',lambda x:x['groups'][0]['provenance'].update(source_id='invented'))
    reject('corpus/disc.json',lambda x:x['groups'][0].update(interpretation_as_word=True))
    reject('corpus/disc.json',lambda x:x['occurrences'].pop())
    reject('reviews/transcription-review-v1.json',lambda x:x.update(external_peer_review_completed=True))
    reject('research/count-assertions.json',lambda x:x['assertions'][0].update(total=242))
    reject('research/experiment-gates.json',lambda x:next(g for g in x['experiments'] if g['id']=='decipherment').update(claim_allowed=True))
    reject('research/family-compatibility-v1.json',lambda x:x['members'].remove('phaistos-disc'))
    reject('sources/sources.json',lambda x:x[0].update(subset_sha256='0'*64))
    reject('analysis/current-status.json',lambda x:x['committed_evidence_counts'].update(unknown_slots=0))
    reject('analysis/current-status.json',lambda x:x['scientific_results'].update(decipherment_claim_allowed=True))
    if (root/'spatial/group-anchors.json').exists():
        reject('spatial/group-anchors.json',lambda x:x[0].update(x=1.2))
        reject('spatial/group-anchors.json',lambda x:x[0].update(approximate=False))
        reject('spatial/group-anchors.json',lambda x:x[0].update(frame_id='invented'))
    if (root/'exports/aegean-interop.json').exists():
        reject('exports/aegean-interop.json',lambda x:x[0]['rights'].update(third_party_material=[]))
        reject('exports/aegean-interop.json',lambda x:x[0]['assertions'][0].update(provenance=[]))
    assert validate(root)['status']=='PASS'
print(json.dumps({'status':'PASS','negative_controls':checks,'restored_positive':'PASS'}))
