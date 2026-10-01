"""Known published exemplar labels and adversarial claim-boundary checks."""
import json,pathlib,shutil,tempfile
from validate_witness_audit import validate,R
assert validate()['status']=='PASS'
cross=json.loads((R/'signs/olivier1975-exemplar-crosswalk.json').read_text())
examples={e['source_exemplar']:e['native_occurrence_id'] for e in cross['entries']}
assert examples['A2.1']=='PD-A-E02-S02'
assert examples['A13.4']=='PD-A-E13-S01'
assert examples['B5.2']=='PD-B-E05-S04'
assert examples['B25.1']=='PD-B-E25-S04'
checks=0
with tempfile.TemporaryDirectory() as td:
 root=pathlib.Path(td)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__','images','output'))
 def reject(path,mutate):
  global checks
  p=root/path;raw=p.read_bytes();d=json.loads(raw);mutate(d);p.write_text(json.dumps(d))
  try:validate(root)
  except Exception:checks+=1
  else:raise AssertionError('accepted witness corruption '+path)
  finally:p.write_bytes(raw)
 reject('reviews/photographic-comparison-v1.json',lambda d:d['groups'].pop())
 reject('reviews/photographic-comparison-v1.json',lambda d:d.update(physical_objects=2))
 reject('reviews/photographic-comparison-v1.json',lambda d:d['groups'][0].update(within_group_order_certified=True))
 reject('reviews/photographic-comparison-v1.json',lambda d:d['groups'][0].update(external_human_review_completed=True))
 reject('signs/olivier1975-exemplar-crosswalk.json',lambda d:d['entries'][0].update(source_exemplar='A2.2'))
 reject('signs/olivier1975-exemplar-crosswalk.json',lambda d:d['unknown_exemplar'].update(native_sign_id='PD-U101E3'))
 reject('reviews/stroke-photo-audit-v1.json',lambda d:d.update(statistical_use_allowed=True))
 reject('reviews/stroke-photo-audit-v1.json',lambda d:d['assertion_comparisons'][0].update(meaning='sentence'))
 assert validate(root)['status']=='PASS'
print(json.dumps({'status':'PASS','published_exemplar_oracles':4,'negative_controls':checks}))
