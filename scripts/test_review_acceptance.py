"""Synthetic receipt fixtures exercise logic; none is real human review."""
import copy,hashlib,json,pathlib,shutil,tempfile,unittest
from review_acceptance import R,template,validate_submission,evaluate,RECORD
class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=pathlib.Path(self.temp.name)/'repo';shutil.copytree(R,self.root,ignore=shutil.ignore_patterns('.git','__pycache__','images','output'))
        self.packet=template(self.root);self.packet['reviewer'].update(name='SYNTHETIC REVIEWER FIXTURE',expertise='Synthetic test only',conflicts='Synthetic test only',independence_declared=True);self.packet['signed_at']='2026-10-01T00:00:00Z'
        photo_pages={g['group_id']:g['source_page_sha256'] for g in json.loads((self.root/'reviews/photographic-comparison-v1.json').read_text())['groups']}
        self.packet['review_record_license']='CC0-1.0'
        self.packet['source_evidence']=[{'source_id':'olivier1975','sha256':h,'locator':'Synthetic fixture; not an epigraphic assessment'} for h in sorted(set(photo_pages.values()))]
        for e in self.packet['entries']:e.update(decision='unresolvable',source_locator='Synthetic fixture only',note='Synthetic uncertainty',ordinal_checked=True,fine_detail_checked=True)
        for m in self.packet['mark_assessments']:m.update(coverage='physical_coverage_supported',entire_group_examined=True,source_id='olivier1975',source_sha256=photo_pages[m['group_id']],source_locator='Synthetic fixture only',notes='Synthetic fixture only')
        self.record={'format':'PD-human-review-acceptance-v1','packet_path':'reviews/submissions/synthetic.json','packet_sha256':'',
            'reviewer_name':'SYNTHETIC REVIEWER FIXTURE','maintainer_name':'SYNTHETIC MAINTAINER FIXTURE',
            'maintainer_is_human':True,'reviewer_is_human':True,'identity_verified':True,'expertise_verified':True,
            'conflicts_reviewed':True,'independence_verified':True,'redistribution_permission_verified':True,'physical_evidence_adequacy_verified':True,
            'verification_record':'SYNTHETIC UNIT TEST; not a real verification record','accepted_at':'2026-10-01T01:00:00Z'}
    def write(self):
        p=self.root/self.record['packet_path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(self.packet));self.record['packet_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();(self.root/RECORD).write_text(json.dumps(self.record))
    def test_no_receipt_and_draft_do_not_open_gate(self):
        self.assertFalse(evaluate(self.root)['final_2_0_allowed'])
        result=validate_submission(template(self.root),self.root);self.assertEqual(result['mark_groups_assessed'],0)
        self.assertFalse(result['scientific_gate_opened'])
    def test_synthetic_full_receipt_exercises_conditional_path(self):
        self.write();result=evaluate(self.root);self.assertTrue(result['final_2_0_allowed']);self.assertEqual(result['reviewed_slots'],242)
        self.assertTrue(result['external_review_accepted']);self.assertEqual(result['mark_groups_physical_coverage_supported'],61)
        from acceptance_2 import calculate
        path=self.root/'research/experiment-gates.json';gates=json.loads(path.read_text())
        gate=next(g for g in gates['experiments'] if g['id']=='external-critical-review')
        gate.update(state='READY_RECORDED_HUMAN_REVIEW',claim_allowed=True,result_ref=RECORD)
        path.write_text(json.dumps(gates));self.assertTrue(calculate(self.root)['final_2_0_allowed'])
    def test_source_limited_assessment_does_not_certify_physical_coverage(self):
        for m in self.packet['mark_assessments']:m['coverage']='source_resolution_limited'
        self.record['physical_evidence_adequacy_verified']=False;self.write();r=evaluate(self.root)
        self.assertTrue(r['external_review_accepted']);self.assertFalse(r['physical_mark_coverage_complete']);self.assertFalse(r['final_2_0_allowed'])
    def test_missing_ordinal_stays_blocked(self):
        self.packet['entries'][0]['ordinal_checked']=False;self.write();self.assertFalse(evaluate(self.root)['final_2_0_allowed'])
    def test_negative_receipts(self):
        for key,value in [('maintainer_is_human',False),('reviewer_is_human',False),('identity_verified','true'),('expertise_verified',False),('independence_verified',False),('maintainer_name','SYNTHETIC REVIEWER FIXTURE'),('accepted_at','2026-09-30T00:00:00Z')]:
            original=copy.deepcopy(self.record);self.record[key]=value;self.write()
            with self.subTest(key=key),self.assertRaises(ValueError):evaluate(self.root)
            self.record=original
        self.write();p=self.root/self.record['packet_path'];p.write_text(p.read_text()+' ')
        with self.assertRaises(ValueError):evaluate(self.root)
    def test_bad_coverage_and_provenance(self):
        for mutation in ['group','hash','unknown_source','wrong_target','entry_type','wrong_page','license']:
            p=copy.deepcopy(self.packet)
            if mutation=='group':p['mark_assessments'][1]=p['mark_assessments'][0]
            elif mutation=='hash':p['source_evidence'][0]['sha256']='0'*64
            elif mutation=='unknown_source':p['source_evidence'][0]['source_id']='unregistered'
            elif mutation=='entry_type':p['entries'][0]='not an entry object'
            elif mutation=='wrong_page':p['mark_assessments'][0]['source_sha256']=p['mark_assessments'][-1]['source_sha256']
            elif mutation=='license':p['review_record_license']=None
            else:p['mark_assessments'][0]['observed_marks']=[{'mark_id':'test','classification':'unresolved','target_occurrence_id':'PD-B-E01-S01','note':'test'}]
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):validate_submission(p,self.root)
        self.write();self.record['packet_path']='../escape.json';(self.root/RECORD).write_text(json.dumps(self.record))
        with self.assertRaises(ValueError):evaluate(self.root)
    def test_adversarial_acceptance_cannot_be_self_asserted(self):
        cases=[]
        p=copy.deepcopy(self.packet);p['reviewer']['independence_declared']=False;cases.append(('reviewer independence',p))
        p=copy.deepcopy(self.packet);p['entries'][0]['decision']='accepted';p['entries'][0]['source_locator']=None;cases.append(('missing locator',p))
        p=copy.deepcopy(self.packet);p['entries'][0]['fine_detail_checked']='true';cases.append(('boolean string',p))
        p=copy.deepcopy(self.packet);p['mark_assessments'][0]['coverage']='physical_coverage_supported';p['mark_assessments'][0]['entire_group_examined']=False;cases.append(('partial physical coverage',p))
        p=copy.deepcopy(self.packet);p['source_evidence'].append(copy.deepcopy(p['source_evidence'][0]));cases.append(('duplicate evidence',p))
        for label,p in cases:
            with self.subTest(label=label),self.assertRaises(ValueError):validate_submission(p,self.root)

    def test_acceptance_record_cannot_replace_packet_or_human_checks(self):
        self.write()
        for key in ['identity_verified','expertise_verified','conflicts_reviewed','independence_verified','redistribution_permission_verified','physical_evidence_adequacy_verified']:
            record=copy.deepcopy(self.record);record[key]=False;(self.root/RECORD).write_text(json.dumps(record))
            with self.subTest(key=key),self.assertRaises(ValueError):evaluate(self.root)
        self.write();record=copy.deepcopy(self.record);record['packet_sha256']='0'*64;(self.root/RECORD).write_text(json.dumps(record))
        with self.assertRaises(ValueError):evaluate(self.root)

    def test_final_version_cannot_bypass_missing_acceptance_artifact(self):
        from validate_current_state import validate
        (self.root/'VERSION').write_text('2.0.0\n')
        citation=self.root/'CITATION.cff'
        citation.write_text(__import__('re').sub(r'2\.0\.0-rc\.\d+', '2.0.0', citation.read_text()))
        (self.root/'analysis/acceptance-2.0.json').unlink()
        with self.assertRaisesRegex(ValueError,'final 2.0 requires complete recorded human acceptance'):
            validate(self.root)

if __name__=='__main__':unittest.main()
