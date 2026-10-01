import json,tempfile,pathlib,shutil,unittest
from acceptance_2 import R,calculate
class AcceptanceTests(unittest.TestCase):
    def test_exact_replay_and_real_blockers(self):
        r=calculate();self.assertEqual(r,json.loads((R/'analysis/acceptance-2.0.json').read_text()))
        self.assertTrue(r['candidate_ready']);self.assertFalse(r['final_2_0_allowed'])
        self.assertEqual(r['review_packet_status'],'VALID_DRAFT')
        self.assertEqual(r['occurrence_audit_counts']['ordinal_not_individually_certified'],196)
    def test_fake_review_or_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)/'repo';shutil.copytree(R,root,ignore=shutil.ignore_patterns('.git','__pycache__','images','output'))
            p=root/'research/experiment-gates.json';original=p.read_bytes();x=json.loads(original)
            g=next(g for g in x['experiments'] if g['id']=='external-critical-review');g.update(state='PASS',claim_allowed=True,result_ref='fictional-review')
            p.write_text(json.dumps(x))
            with self.assertRaises(ValueError):calculate(root)
            p.write_bytes(original);p=root/'reviews/occurrence-audit-v1.json';x=json.loads(p.read_text());x['coverage']['fine_detail_certified']=242;p.write_text(json.dumps(x))
            with self.assertRaises(ValueError):calculate(root)
if __name__=='__main__':unittest.main()
