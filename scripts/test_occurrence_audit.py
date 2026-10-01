import copy,json,tempfile,pathlib,unittest
from occurrence_audit import R,calculate
class AuditTests(unittest.TestCase):
    def test_replay_scope_and_known_loci(self):
        report=calculate();self.assertEqual(report,json.loads((R/'reviews/occurrence-audit-v1.json').read_text()))
        self.assertEqual(report['coverage'],{'slots':242,'source_labeled_exemplars':46,'ordinal_not_individually_certified':196,'fine_detail_certified':0,'external_reviews':0})
        rows={r['occurrence_id']:r for r in report['rows']}
        self.assertEqual(rows['PD-A-E24-S05']['source_exemplar'],'A24.1');self.assertIsNone(rows['PD-A-E24-S05']['native_sign_id'])
        self.assertEqual(rows['PD-A-E02-S02']['source_exemplar'],'A2.1')
        self.assertTrue(all(r['physical_position'] is None and not r['external_review_completed'] for r in rows.values()))
    def test_complete_native_coverage(self):
        actual=calculate()['rows'];native=json.loads((R/'corpus/disc.json').read_text())['occurrences']
        self.assertEqual([r['occurrence_id'] for r in actual],[r['occurrence_id'] for r in native])
        self.assertEqual(len({r['occurrence_id'] for r in actual}),242)
if __name__=='__main__':unittest.main()
