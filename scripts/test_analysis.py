#!/usr/bin/env python3
"""Known-answer arithmetic and reversible-transformation software controls."""
import json,math
from analyze import summarize,analyze,R
s=summarize([['1','2','1'],['2','3']])
assert s['sign_frequencies']=={'1':2,'2':2,'3':1}
assert s['within_group_identified_pairs']==3 and s['adjacent_pair_frequencies']=={'1 > 2':1,'2 > 1':1,'2 > 3':1}
assert abs(s['shannon_bits']-1.521928094887)<1e-12
assert s['group_length_histogram']=={'2':1,'3':1}
u=summarize([['1',None,'1'],['2','3']]);assert u['identified_slots']==4 and u['unknown_slots']==1 and u['shannon_bits']==1.5
assert u['adjacent_pair_frequencies']=={'2 > 3':1},'unknown must not connect adjacent known symbols'
assert summarize([[None]])['shannon_bits'] is None,'unknown-only is not measured zero entropy'
assert summarize([])['shannon_bits'] is None
r=summarize([list(reversed(x)) for x in reversed([['1','2','1'],['2','3']])]);assert r['sign_frequencies']==s['sign_frequencies'] and r['shannon_bits']==s['shannon_bits'] and r['adjacent_pair_frequencies']['3 > 2']==1
real=analyze();assert real==json.loads((R/'analysis/descriptive-v1.json').read_text())
assert real['statistical_inference_allowed'] is False and len(real['directional_sensitivity'])==4
assert len(real['unknown_slot_sensitivity']['assignments'])==45
for view in real['directional_sensitivity']:
    assert view['physical_objects']==1
    for face in 'AB':assert view['faces'][face]['sign_frequencies']==real['baseline_faces'][face]['sign_frequencies']
assert sum(real['baseline_faces'][f]['slots'] for f in 'AB')==242
assert sum(real['baseline_faces'][f]['identified_slots'] for f in 'AB')==241
print(json.dumps({'status':'PASS','known_answer_scope':'software arithmetic and transformations only','linguistic_gold':False,'directional_views':4,'unknown_hypotheses':45}))
