"""Build an offline explorer of committed evidence, without certifying epigraphy."""
import argparse,csv,hashlib,json,pathlib,re
R=pathlib.Path(__file__).resolve().parents[1]
GENERATED={'analysis/evidence-index-v1.json','analysis/workbench-acceptance-v1.json','workbench/evidence.html','research/workbench-milestone-v1.json','scripts/evidence_workbench.py','scripts/test_evidence_workbench.py','scripts/test_evidence_browser.cjs','workbench/evidence-template.html'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def calculate(root=R):
 state=json.loads((root/'analysis/current-status.json').read_text());family=json.loads((root/'research/family-compatibility-v1.json').read_text());report=json.loads((root/'research/family-readiness-v1.json').read_text());member=next(m for m in report['members'] if m['repository']==family['member']);rows=[]
 for e in state['evidence']:
  if e['path'] in GENERATED:continue
  p=(root/e['path']).resolve()
  if not p.is_relative_to(root.resolve()) or not p.is_file():raise ValueError('invalid evidence path')
  actual=digest(p)
  if actual!=e['sha256']:raise ValueError('evidence pin mismatch: '+e['path'])
  value=json.loads(p.read_text()) if p.suffix=='.json' else None
  summary={k:value[k] for k in ['format','scope','boundary','status','source_id','record_license','acquisition_status','interpretation'] if isinstance(value,dict) and k in value}
  rows.append({'path':e['path'],'sha256':actual,'bytes':p.stat().st_size,'category':e['path'].split('/')[0],'summary':summary})
 if len({e['path'] for e in rows})!=len(rows):raise ValueError('duplicate evidence path')
 return {'format':'research-evidence-index-v1','workbench_version':'1.0.0','project':family['member'],'repository_version':state['repository_version'],'evidence':rows,'scientific_results':state['scientific_results'],'blocking_dependencies':member['blocking_dependencies'],'metrics':member['metrics'],
  'family_report_sha256':digest(root/'research/family-readiness-v1.json'),'implementation_sha256':digest(root/'scripts/evidence_workbench.py'),
  'boundary':'Committed file integrity and attributed project records. Hashes do not establish epigraphic truth, image adequacy or independent human review. Native units stay separate; no pooled sign identities or linguistic inference.'}
def html(root=R):
 data=calculate(root);payload={'index':data,'index_sha256':hashlib.sha256((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest(),'edition':None}
 if (root/'analysis/edition-workbench-v1.json').exists():
  v=json.loads((root/'analysis/edition-workbench-v1.json').read_text());payload['edition']={k:v[k] for k in ['comparison_rows','group_evidence','sensitivity_bounds','source_coverage','hypothesis_space','boundary','scenario_count']}
  payload['edition']['scenarios']=[{k:s[k] for k in ['scenario_id','unknown_sign_number','b3_sign_number','reverse_group_order','reverse_within_group','all_slots','graphical_groups','frequency_delta']} for s in v['scenarios']]
 raw=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('&','\\u0026')
 return (root/'workbench/evidence-template.html').read_text().replace('__PAYLOAD__',raw)
def acceptance(root=R):
 spec=json.loads((root/'research/workbench-milestone-v1.json').read_text())
 if spec['milestone']!='research-workbench' or spec['version']!='1.0.0' or spec['expert_review_granted'] is not False or spec['native_changes_applied'] is not False or spec['human_review_required_for_this_engineering_milestone'] is not False:raise ValueError('engineering milestone scope drift')
 if not (root/'research/workbench-guide.md').is_file():raise ValueError('missing readable review guide')
 index=calculate(root)
 if json.loads((root/'analysis/evidence-index-v1.json').read_text())!=index:raise ValueError('index replay drift')
 if (root/'workbench/evidence.html').read_text()!=html(root):raise ValueError('offline viewer replay drift')
 edition=None
 if index['project']=='Phaistos-Disc':
  from edition_workbench import calculate as edition_calculate
  edition=json.loads((root/'analysis/edition-workbench-v1.json').read_text())
  if edition!=edition_calculate(root):raise ValueError('edition replay drift')
  with (root/'reviews/occurrence-review-sheet.tsv').open(newline='') as f:slots=list(csv.DictReader(f,delimiter='\t'))
  with (root/'reviews/group-mark-review-sheet.tsv').open(newline='') as f:groups=list(csv.DictReader(f,delimiter='\t'))
  if [s['occurrence_id'] for s in slots]!=[s['occurrence_id'] for s in edition['comparison_rows']] or [g['group_id'] for g in groups]!=list(edition['group_evidence']):raise ValueError('readable review sheet coverage drift')
  if any(s['decision']!='unreviewed' or s['ordinal_checked']!='false' or s['fine_detail_checked']!='false' for s in slots) or any(g['coverage']!='unassessed' or g['entire_group_examined']!='false' for g in groups):raise ValueError('blank review sheet promoted to review')
 return {'format':'research-workbench-acceptance-v1','milestone_version':'1.0.0','project':index['project'],'status':'PASS_ARTIFACT_REPLAY','evidence_files':len(index['evidence']),'index_sha256':digest(root/'analysis/evidence-index-v1.json'),'viewer_sha256':digest(root/'workbench/evidence.html'),'disc_comparison_rows':len(edition['comparison_rows']) if edition else None,'disc_scenarios':edition['scenario_count'] if edition else None,'native_changes_applied':False,'expert_review_granted':False,'final_epigraphic_acceptance_granted':False,'boundary':'Engineering milestone only. Browser behavior and adversarial controls are tested separately in CI.'}
def write(root=R):
 (root/'workbench').mkdir(exist_ok=True)
 (root/'analysis/evidence-index-v1.json').write_text(json.dumps(calculate(root),ensure_ascii=False,indent=2)+'\n')
 (root/'workbench/evidence.html').write_text(html(root))
 (root/'analysis/workbench-acceptance-v1.json').write_text(json.dumps(acceptance(root),indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
 if a.write:write()
 else:
  expected=acceptance();actual=json.loads((R/'analysis/workbench-acceptance-v1.json').read_text())
  if expected!=actual:raise ValueError('workbench acceptance drift')
  print(json.dumps(actual))
