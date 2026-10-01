import copy,json,unittest
from review_packet import R,calculate,validate
class ReviewTests(unittest.TestCase):
    def test_draft_exact_and_unreviewed(self):
        p=calculate();self.assertEqual(p,json.loads((R/'reviews/review-packet-v1.json').read_text()))
        self.assertEqual(validate(p)['status'],'VALID_DRAFT');self.assertEqual(validate(p)['unreviewed'],242)
    def test_synthetic_submission_stays_unverified(self):
        p=calculate();p['reviewer'].update(name='SYNTHETIC TEST ONLY',expertise='test',conflicts='none claimed',independence_declared=True);p['signed_at']='2026-10-01T00:00:00Z'
        p['entries'][0].update(decision='conflict',source_locator='synthetic fixture',note='test disagreement')
        r=validate(p);self.assertEqual(r['status'],'VALID_UNVERIFIED_SUBMISSION');self.assertFalse(r['scientific_gate_opened']);self.assertFalse(r['identity_or_independence_verified'])
    def test_negative_controls(self):
        for mutation in ['hash','drop','duplicate','promotion','type','missing_locus']:
            p=calculate()
            if mutation=='hash':p['native_corpus_sha256']='0'*64
            elif mutation=='drop':p['entries'].pop()
            elif mutation=='duplicate':p['entries'][1]=p['entries'][0]
            elif mutation=='promotion':p['entries'][0]['fine_detail_checked']=True
            elif mutation=='type':p['entries'][0]['ordinal_checked']='true'
            else:p['entries'][0]['decision']='compatible'
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate(p)
if __name__=='__main__':unittest.main()
