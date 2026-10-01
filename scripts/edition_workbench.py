"""Assemble bounded edition evidence and exhaustive conditional descriptions."""
import collections,hashlib,itertools,json,pathlib
from apparatus_sensitivity import summarize
from research_suite import metrics
R=pathlib.Path(__file__).resolve().parents[1]
INPUTS=['corpus/disc.json','apparatus/claims.json','reviews/occurrence-audit-v1.json','reviews/photographic-comparison-v1.json','apparatus/stroke-assertions.json','sources/sources.json','sources/olivier1975-page-manifest.json']
def calculate(root=R):
 load=lambda p:json.loads((root/p).read_text())
 corpus=load(INPUTS[0]);claims=load(INPUTS[1]);audit=load(INPUTS[2]);photo={g['group_id']:g for g in load(INPUTS[3])['groups']};groups={g['group_id']:g for g in corpus['groups']};sources={s['source_id']:s for s in load(INPUTS[5])};pages={p['page']:p for p in load(INPUTS[6])['pages']}
 rows=[]
 for o,a in zip(corpus['occurrences'],audit['rows']):
  assert o['occurrence_id']==a['occurrence_id']
  g=groups[o['group_id']];p=photo[o['group_id']];alternatives=[c for c in claims if c['kind']=='reading' and c['locus']==o['occurrence_id']]
  rows.append({'occurrence_id':o['occurrence_id'],'group_id':o['group_id'],'native_sign_id':o['sign_id'],'native_sign_number':None if o['sign_id'] is None else int(o['sign_id'][4:],16)-0x101CF,
   'historical_figure':{'source_id':'evans1909','locator':a['native_figure_locator'],'sha256':sources['evans1909']['full_source_sha256'],'url':sources['evans1909']['download_url']+'#page='+('298' if '-A-' in o['occurrence_id'] else '300'),'scope':'Inherited project transcription of numbered figures'},
   'published_photograph':{'source_id':'olivier1975','locator':p['locator'],'sha256':p['source_page_sha256'],'url':pages[p['page']]['url'],'scope':p['comparison_scope'],'outcome':p['outcome'],'individual_ordinal_evidence':a['ordinal_evidence'],'source_exemplar':a['source_exemplar'],'fine_detail_certified':False},
   'limited_competing_assertions':[{'claim_id':c['claim_id'],'source_id':c['source_id'],'locator':c['locator'],'sha256':sources[c['source_id']]['full_source_sha256'],'url':sources[c['source_id']]['url'],'proposed_sign_number':c['value']['proposed_evans_sign'],'status':c['status'],'adopted':False} for c in alternatives],
   'external_review_completed':False})
 group_evidence={};
 for row in rows:
  gid=row['group_id'];group_evidence[gid]={'historical_figure':row.pop('historical_figure'),'published_photograph':row.pop('published_photograph')}
  row['individual_ordinal_evidence']=group_evidence[gid]['published_photograph'].pop('individual_ordinal_evidence');row['source_exemplar']=group_evidence[gid]['published_photograph'].pop('source_exemplar')
 scenarios=[];original={o['occurrence_id']:o['sign_id'] for o in corpus['occurrences']}
 for unknown,b3,group_reverse,slot_reverse in itertools.product([None]+list(range(1,46)),[7,25],[False,True],[False,True]):
  values=original.copy();values['PD-A-E24-S05']=None if unknown is None else f'PD-U{0x101CF+unknown:X}';values['PD-B-E03-S05']=f'PD-U{0x101CF+b3:X}'
  faces={};all_groups=[]
  for face in ['A','B']:
   selected=[g for g in corpus['groups'] if g['face_id']=='PD-001-'+face]
   if group_reverse:selected.reverse()
   seq=[[values[k] for k in (list(reversed(g['occurrence_ids'])) if slot_reverse else g['occurrence_ids'])] for g in selected]
   all_groups+=seq;bigram=collections.Counter((x,y) for group in seq for x,y in zip(group,group[1:]) if x is not None and y is not None)
   faces[face]={'groups':metrics(seq),'distinct_ordered_within_group_bigrams':len(bigram),'repeated_ordered_bigram_pairs':sum(n*(n-1)//2 for n in bigram.values()),'ordered_bigram_sha256':hashlib.sha256(json.dumps([(x,y,n) for (x,y),n in sorted(bigram.items())],separators=(',',':')).encode()).hexdigest()}
  scenarios.append({'scenario_id':f"u{'unknown' if unknown is None else unknown:}-b{b3}-g{int(group_reverse)}-s{int(slot_reverse)}",'unknown_sign_number':unknown,'b3_sign_number':b3,'reverse_group_order':group_reverse,'reverse_within_group':slot_reverse,'attributed_assertions_enabled':(['PD-C001'] if unknown==20 else [])+(['PD-C002'] if b3==25 else []),'readings_adopted':False,'all_slots':summarize(values.values()),'graphical_groups':metrics(all_groups),'faces':faces})
 baseline=summarize(original.values())
 for scenario in scenarios:
  freq=scenario['all_slots'].pop('frequency');scenario['frequency_delta']={k:freq.get(k,0)-baseline['frequency'].get(k,0) for k in sorted(set(freq)|set(baseline['frequency'])) if freq.get(k,0)!=baseline['frequency'].get(k,0)}
 bounds={k:{'minimum':min(s['all_slots'][k] for s in scenarios),'maximum':max(s['all_slots'][k] for s in scenarios)} for k in ['identified','unknown','entropy_bits']}
 bounds.update({k:{'minimum':min(s['graphical_groups'][k] for s in scenarios),'maximum':max(s['graphical_groups'][k] for s in scenarios)} for k in ['identical_complete_group_pairs','identical_adjacent_pairs']})
 return {'format':'disc-edition-workbench-v1','milestone':'research-workbench-1.0.0','input_pins':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in INPUTS],
  'implementation_sha256':hashlib.sha256((root/'scripts/edition_workbench.py').read_bytes()).hexdigest(),'group_evidence':group_evidence,'baseline_frequency':baseline['frequency'],'comparison_rows':rows,'scenario_count':len(scenarios),'scenarios':scenarios,'sensitivity_bounds':bounds,
  'source_coverage':'Evans figure transcription and inherited bounded Olivier group/exemplar review; only two HMU reading assertions, not a complete HMU transcription or a new source inspection. Pernier is contextual evidence, not another certified transcription.',
  'hypothesis_space':'Erased slot unknown or each of 45 base signs; B3 slot 5 native07 or attributed25; group and within-group order reversed independently. No probabilities, invented signs, stroke semantics or further unrecorded readings.',
  'boundary':'One physical object. Faces are not independent replications. Graphical groups are not established words. Hypothesis bounds describe this enumerated space only; no optimal reading, language, decipherment or physical mark completeness is established.',
  'physical_objects':1,'expert_review_completed':False,'native_changes_applied':False,'p_values':None}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,separators=(',',':')))
