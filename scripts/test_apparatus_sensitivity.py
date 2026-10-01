"""Known frequency deltas of the declared source assertions, and native immutability."""
import hashlib,json,math
from apparatus_sensitivity import calculate,summarize,R
before=hashlib.sha256((R/'corpus/disc.json').read_bytes()).hexdigest();d=calculate()
assert d==json.loads((R/'analysis/apparatus-sensitivity-v1.json').read_text())
assert summarize(['a','a','b','b',None])['entropy_bits']==1
assert summarize([None])['entropy_bits'] is None
by={s['scenario_id']:s for s in d['scenarios']}
assert by['native']['summary']['identified']==241 and by['native']['summary']['unknown']==1
assert by['PD-C001']['delta_from_native']['frequency']=={'PD-U101E3':1}
assert by['PD-C002']['delta_from_native']['frequency']=={'PD-U101D6':-1,'PD-U101E8':1}
assert by['PD-C001+PD-C002']['summary']['identified']==242
assert by['PD-C001+PD-C002']['summary']['unknown']==0
assert all(s['readings_adopted'] is False for s in d['scenarios'])
assert d['p_values'] is None and d['uncertainty_probabilities'] is None and d['independent_physical_objects']==1
assert hashlib.sha256((R/'corpus/disc.json').read_bytes()).hexdigest()==before
print(json.dumps({'status':'PASS','source_assertion_scenarios':4,'known_frequency_deltas':2,'native_unchanged':True,'linguistic_claims':False}))
