import json,unittest
from research_suite import R,metrics,calculate
class ResearchTests(unittest.TestCase):
    def test_known_toy_counts(self):
        m=metrics([['a','a'],['a','a'],['b',None,'a']])
        self.assertEqual(m,{'groups':3,'complete_groups':2,'incomplete_groups':1,'eligible_adjacent_pairs':2,'identical_adjacent_pairs':2,'identical_complete_group_pairs':1,'distinct_complete_group_sequences':1})
        self.assertEqual(metrics([[]])['eligible_adjacent_pairs'],0)
    def test_exact_replay_and_single_cluster(self):
        r=calculate();self.assertEqual(r,json.loads((R/'analysis/research-suite-v2.json').read_text()))
        self.assertEqual(r['physical_objects'],1);self.assertIsNone(r['p_values']);self.assertFalse(r['linguistic_inference_allowed'])
        self.assertEqual(r['faces']['A']['observed']['incomplete_groups'],1)
        self.assertEqual(r['faces']['B']['observed']['incomplete_groups'],0)
        for f in r['faces'].values():self.assertEqual(f['observed'],f['reversed_group_sequences'])
    def test_unknown_exclusion(self):
        self.assertEqual(metrics([[None,None],['a','b']])['eligible_adjacent_pairs'],1)
        self.assertEqual(metrics([[None,None],['a','b']])['complete_groups'],1)
if __name__=='__main__':unittest.main()
