"""Validate photographic review boundaries and source-attested ordinal examples."""
import hashlib,json,pathlib,re
R=pathlib.Path(__file__).resolve().parents[1]
def validate(root=R):
 def read(p):return json.loads((root/p).read_text())
 def require(ok,message):
  if not ok:raise ValueError(message)
 sources={s['source_id']:s for s in read('sources/sources.json')}
 source=sources['olivier1975'];manifest=read(source['manifest_path'])
 require(hashlib.sha256((root/source['manifest_path']).read_bytes()).hexdigest()==source['manifest_sha256'],'photographic page manifest identity')
 require(source['record_license']=='NOASSERTION' and manifest['redistribution_allowed'] is False,'photograph rights promoted')
 pages={e['page']:e for e in manifest['pages']}
 require(set(pages)==set(range(5,35)) and len(manifest['pages'])==30,'photographic page acquisition coverage')
 for n,e in pages.items():
  require(e['url']==f'https://www.persee.fr/renderPage/bch_0007-4217_1975_num_99_1_2067/bch_0007-4217_1975_num_99_1_T1_{n:04d}_0000_710.jpg' and re.fullmatch('[a-f0-9]{64}',e['sha256']) and e['bytes']>0,'page locator/identity')
 corpus=read('corpus/disc.json');groups={g['group_id']:g for g in corpus['groups']};labels={g['evans_label']:g for g in groups.values()};occ={o['occurrence_id']:o for o in corpus['occurrences']}
 review=read('reviews/photographic-comparison-v1.json')
 require(review['physical_objects']==1 and review['native_corpus_sha256']==hashlib.sha256((root/'corpus/disc.json').read_bytes()).hexdigest(),'photo/native evidence identity')
 require(review['photographic_acquisition_reported']=='1971-02' and review['source_id']=='olivier1975','photographic lineage')
 rows=review['groups'];require(len(rows)==61 and {r['group_id'] for r in rows}==set(groups),'photo group coverage')
 for r in rows:
  g=groups[r['group_id']]
  require(r['source_group_label']==g['evans_label'] and r['source_page_sha256']==pages[r['page']]['sha256'],'photo locus identity')
  require(r['slot_count']==len(g['occurrence_ids']),'photo slot accounting')
  require(r['outcome']==('compatible_with_unknown_preserved' if g['evans_label']=='A24' else 'compatible_at_digitization_resolution'),'photo uncertainty')
  require(r['comparison_scope']=='slot_count_and_coarse_glyph_compatibility_up_to_reversal' and r['within_group_order_certified'] is False and r['fine_detail_certified'] is False and r['external_human_review_completed'] is False,'photo review promoted')
 cross=read('signs/olivier1975-exemplar-crosswalk.json');entries=cross['entries']
 require(len(entries)==45 and {e['evans_sign_number'] for e in entries}==set(range(1,46)),'exemplar coverage')
 for e in entries:
  label,ordinal=e['source_exemplar'].split('.');g=labels[label];n=int(ordinal)
  require(1<=n<=len(g['occurrence_ids']),'source exemplar ordinal outside group')
  target=g['occurrence_ids'][len(g['occurrence_ids'])-n]
  require(e['native_occurrence_id']==target and e['native_sign_id']==occ[target]['sign_id']==f"PD-U{0x101CF+e['evans_sign_number']:X}",'source exemplar/slot transform')
 require(cross['unknown_exemplar']=={'source_exemplar':'A24.1','source_page':31,'native_occurrence_id':'PD-A-E24-S05','native_sign_id':None},'unreadable exemplar imputed')
 audit=read('reviews/stroke-photo-audit-v1.json');marks=read('apparatus/stroke-assertions.json')
 require(len(audit['groups_inspected'])==61 and set(audit['groups_inspected'])==set(groups),'stroke panel inspection coverage')
 observations=audit['assertion_comparisons']
 require(len(observations)==16 and {m['mark_id'] for m in observations}=={m['mark_id'] for m in marks['marks']},'stroke assertion comparison coverage')
 for m in observations:
  baseline=next(b for b in marks['marks'] if b['mark_id']==m['mark_id'])
  candidates=[o['occurrence_id'] for o in corpus['occurrences'] if o['group_id']==baseline['group_id'] and o['sign_id']==f"PD-U{0x101CF+baseline['asserted_evans_sign']:X}"]
  require(m['candidate_occurrence_ids']==candidates and m['meaning'] is None and m['native_assertion_replaced'] is False and m['certainty']=='project_visual_candidate','photo stroke evidence promoted')
  require(m['preferred_occurrence_id'] is None or m['preferred_occurrence_id'] in candidates,'invalid photo stroke candidate')
 require(audit['statistical_use_allowed'] is False and audit['meaning_assigned'] is False and audit['external_review_completed'] is False,'stroke gate promoted')
 require(audit['historical_unresolved_targets']==['PD-M002','PD-M004'] and audit['proposed_typographical_explanation']['status']=='unadopted_hypothesis','historical ambiguity overwritten')
 return {'status':'PASS','groups_compared':61,'source_attested_identified_exemplars':45,'unknown_exemplar':1,'stroke_assertions_compared':16,'external_review':'BLOCKED'}
if __name__=='__main__':print(json.dumps(validate()))
