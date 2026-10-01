import json,unittest
from source_coverage import R,calculate
class SourceTests(unittest.TestCase):
    def test_exact_replay_and_source_identity(self):
        r=calculate();self.assertEqual(r,json.loads((R/'analysis/source-coverage-v1.json').read_text()))
        self.assertEqual(len(r['sources']),8);self.assertEqual(r['physical_objects'],1)
        self.assertEqual(r['pernier_dates'],{'volume_year':1908,'imprint_year':1909,'archive_metadata_year':'1906','archive_date_adopted':False})
    def test_unknown_scope_and_no_independence_promotion(self):
        r=calculate();rows={s['source_id']:s for s in r['sources']}
        self.assertIsNone(rows['pernier1908']['coverage_units']);self.assertIsNone(rows['hmu-codification']['coverage_units'])
        self.assertTrue(all(not s['complete_object_autopsy'] and not s['independent_review_completed'] for s in rows.values()))
        self.assertEqual(rows['olivier1975']['coverage_units']['individual_ordinal_pending'],196)
if __name__=='__main__':unittest.main()
