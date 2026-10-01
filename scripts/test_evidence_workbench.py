"""Verify replay, embedded content, provenance tampering and safe HTML text."""
import copy,hashlib,json,pathlib,re,shutil,tempfile,unittest
from evidence_workbench import calculate,html,acceptance,write,R
class EvidenceTests(unittest.TestCase):
 def test_replay_and_embedded_identity(self):
  self.assertEqual(json.loads((R/'analysis/evidence-index-v1.json').read_text()),calculate());self.assertEqual((R/'workbench/evidence.html').read_text(),html());self.assertEqual(json.loads((R/'analysis/workbench-acceptance-v1.json').read_text()),acceptance())
  payload=json.loads(re.search(r'<script id="evidence-data" type="application/json">(.*?)</script>',html(),re.S)[1]);self.assertEqual(payload['index'],calculate());self.assertEqual(payload['index_sha256'],hashlib.sha256((R/'analysis/evidence-index-v1.json').read_bytes()).hexdigest());self.assertFalse(acceptance()['expert_review_granted'])
  if payload['edition']:self.assertEqual(payload['edition']['edition_sha256'],hashlib.sha256((R/'analysis/edition-workbench-v1.json').read_bytes()).hexdigest())
 def test_tampered_pin_and_viewer_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','images','output','node_modules','__pycache__'))
   p=root/'analysis/current-status.json';v=json.loads(p.read_text());entry=next(e for e in v['evidence'] if e['path'] not in __import__('evidence_workbench').GENERATED);entry['sha256']='0'*64;p.write_text(json.dumps(v))
   with self.assertRaisesRegex(ValueError,'pin mismatch'):calculate(root)
   p.write_bytes((R/'analysis/current-status.json').read_bytes());(root/'workbench/evidence.html').write_text('<p>tampered</p>')
   with self.assertRaisesRegex(ValueError,'viewer replay drift'):acceptance(root)
 def test_unsafe_paths_duplicates_and_script_text(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','images','output','node_modules','__pycache__'));p=root/'analysis/current-status.json';base=json.loads(p.read_text())
   v=copy.deepcopy(base);v['evidence'].append(copy.deepcopy(v['evidence'][0]));p.write_text(json.dumps(v))
   with self.assertRaisesRegex(ValueError,'duplicate'):calculate(root)
   v=copy.deepcopy(base);v['evidence'][0]['path']='../escape.json';p.write_text(json.dumps(v))
   with self.assertRaisesRegex(ValueError,'invalid evidence path'):calculate(root)
   v=copy.deepcopy(base);v['scientific_results']['test_text']='</script><script>alert(1)</script>';p.write_text(json.dumps(v));render=html(root);self.assertNotIn(v['scientific_results']['test_text'],render);self.assertIn('\\u003c/script>',render)
if __name__=='__main__':unittest.main()
