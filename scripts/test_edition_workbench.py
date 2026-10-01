"""Independent arithmetic and coverage controls for conditional Disc descriptions."""
import collections,json,pathlib,unittest
from edition_workbench import calculate,R
class EditionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.result=calculate()
 def test_replay_and_native_identity(self):
  self.assertEqual(self.result,json.loads((R/'analysis/edition-workbench-v1.json').read_text()))
  corpus=json.loads((R/'corpus/disc.json').read_text());self.assertEqual([r['occurrence_id'] for r in self.result['comparison_rows']],[o['occurrence_id'] for o in corpus['occurrences']]);self.assertEqual(len(self.result['group_evidence']),61)
  self.assertEqual(sum(bool(r['limited_competing_assertions']) for r in self.result['comparison_rows']),2)
  self.assertEqual(sum(r['individual_ordinal_evidence']=='published_exemplar_crosswalk' for r in self.result['comparison_rows']),46)
 def test_exhaustive_space_and_frequency_deltas(self):
  cases=self.result['scenarios'];self.assertEqual(len(cases),368);self.assertEqual(len({s['scenario_id'] for s in cases}),368)
  for s in cases:
   expected=collections.Counter()
   if s['unknown_sign_number'] is not None:expected[f"PD-U{0x101CF+s['unknown_sign_number']:X}"]+=1
   if s['b3_sign_number']==25:expected['PD-U101D6']-=1;expected['PD-U101E8']+=1
   self.assertEqual(s['frequency_delta'],{k:v for k,v in expected.items() if v})
   self.assertEqual(s['all_slots']['identified'],241+(s['unknown_sign_number'] is not None))
 def test_group_repetitions_and_order_invariance(self):
  corpus=json.loads((R/'corpus/disc.json').read_text());v={o['occurrence_id']:o['sign_id'] for o in corpus['occurrences']};seq=[tuple(v[k] for k in g['occurrence_ids']) for g in corpus['groups']];complete=[s for s in seq if None not in s]
  expected=sum(complete[i]==complete[j] for i in range(len(complete)) for j in range(i+1,len(complete)))
  self.assertEqual(expected,9)
  for s in self.result['scenarios']:self.assertEqual(s['graphical_groups']['identical_complete_group_pairs'],expected)
  for u in [None,1,20,45]:
   for b in [7,25]:
    cases=[s for s in self.result['scenarios'] if s['unknown_sign_number']==u and s['b3_sign_number']==b];self.assertTrue(all(s['all_slots']==cases[0]['all_slots'] and s['graphical_groups']==cases[0]['graphical_groups'] for s in cases))
 def test_boundaries_and_source_loci(self):
  self.assertEqual(self.result['physical_objects'],1);self.assertFalse(self.result['expert_review_completed']);self.assertIsNone(self.result['p_values'])
  for row in self.result['comparison_rows']:
   self.assertFalse(row['external_review_completed']);self.assertFalse(self.result['group_evidence'][row['group_id']]['published_photograph']['fine_detail_certified'])
  self.assertEqual(self.result['sensitivity_bounds']['identical_adjacent_pairs'],{'minimum':4,'maximum':5})
if __name__=='__main__':unittest.main()
