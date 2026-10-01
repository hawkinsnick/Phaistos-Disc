"""Describe four explicit source-assertion scenarios without adopting any reading."""
import collections,hashlib,itertools,json,math,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def summarize(values):
 c=collections.Counter(v for v in values if v is not None);n=sum(c.values())
 return {'slots':len(values),'identified':n,'unknown':len(values)-n,'frequency':dict(sorted(c.items())),'entropy_bits':-sum((v/n)*math.log2(v/n) for v in c.values()) if n else None}
def calculate(root=R):
 corpus=json.loads((root/'corpus/disc.json').read_text());claims=json.loads((root/'apparatus/claims.json').read_text());readings=[next(c for c in claims if c['claim_id']==id) for id in ['PD-C001','PD-C002']]
 rows=[]
 for switches in itertools.product([False,True],repeat=2):
  values={o['occurrence_id']:o['sign_id'] for o in corpus['occurrences']};applied=[]
  for enabled,c in zip(switches,readings):
   if enabled:values[c['locus']]=f"PD-U{0x101CF+c['value']['proposed_evans_sign']:X}";applied.append(c['claim_id'])
  rows.append({'scenario_id':'native' if not applied else '+'.join(applied),'applied_source_assertions':applied,'readings_adopted':False,'summary':summarize(values.values())})
 native=rows[0]['summary']
 for row in rows:
  s=row['summary'];row['delta_from_native']={'identified':s['identified']-native['identified'],'unknown':s['unknown']-native['unknown'],'entropy_bits':s['entropy_bits']-native['entropy_bits'],'frequency':{k:s['frequency'].get(k,0)-native['frequency'].get(k,0) for k in sorted(set(s['frequency'])|set(native['frequency'])) if s['frequency'].get(k,0)!=native['frequency'].get(k,0)}}
 return {'scope':'Conditional description of four combinations of two attributed reading assertions; not a pooled edition, probability model or linguistic test.','native_corpus_sha256':hashlib.sha256((root/'corpus/disc.json').read_bytes()).hexdigest(),'apparatus_sha256':hashlib.sha256((root/'apparatus/claims.json').read_bytes()).hexdigest(),'independent_physical_objects':1,'source_assertions':['PD-C001','PD-C002'],'scenarios':rows,'p_values':None,'uncertainty_probabilities':None,'decipherment_claim_allowed':False}
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
