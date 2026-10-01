"""Compute release-candidate readiness without granting final critical acceptance."""
import hashlib,json,pathlib
from occurrence_audit import calculate as occurrences
from source_coverage import calculate as sources
from research_suite import calculate as research
from review_packet import calculate as packet,validate as validate_packet
from review_acceptance import template as packet_v2,evaluate as evaluate_review,validate_submission
R=pathlib.Path(__file__).resolve().parents[1]
def calculate(root=R):
    artifacts=[('reviews/occurrence-audit-v1.json',occurrences),('analysis/source-coverage-v1.json',sources),('analysis/research-suite-v2.json',research),('reviews/review-packet-v1.json',packet),('reviews/review-packet-v2.json',packet_v2)]
    pins=[]
    for path,replay in artifacts:
        raw=(root/path).read_bytes()
        if json.loads(raw)!=replay(root):raise ValueError('acceptance replay drift: '+path)
        pins.append({'path':path,'sha256':hashlib.sha256(raw).hexdigest()})
    audit=occurrences(root);draft=validate_packet(packet(root),root)
    gates=json.loads((root/'research/experiment-gates.json').read_text())['experiments']
    external=next(g for g in gates if g['id']=='external-critical-review')
    review=evaluate_review(root)
    expected_state='READY_RECORDED_HUMAN_REVIEW' if review['external_review_accepted'] else 'BLOCKED'
    expected_ref='reviews/accepted-review.json' if review['external_review_accepted'] else None
    if external['state']!=expected_state or external['claim_allowed']!=review['external_review_accepted'] or external['result_ref']!=expected_ref:raise ValueError('review gate does not match recorded acceptance')
    return {'target_release':'2.0.0','candidate_release':'2.0.0-rc.2',
            'engineering_artifact_replay':'PASS','candidate_ready':True,
            'final_2_0_allowed':review['final_2_0_allowed'],'status':'READY_FOR_FINAL_2_0' if review['final_2_0_allowed'] else 'BLOCKED_FOR_FINAL_2_0',
            'native_corpus_sha256':hashlib.sha256((root/'corpus/disc.json').read_bytes()).hexdigest(),
            'artifact_pins':pins,'occurrence_audit_counts':audit['coverage'],
            'review_packet_status':draft['status'],'review_evidence':review,
            'acceptance_requirements':[
                {'id':'source_linked_occurrence_ledger','state':'PASS','scope':'242 rows; bounded inherited evidence, not new certification'},
                {'id':'reproducible_research_and_submission_tools','state':'PASS_ARTIFACT_REPLAY','scope':'Byte-pinned software descriptions and draft submission validation; CI verifies browser and adversarial tests separately'},
                {'id':'independent_human_epigraphic_review','state':'PASS_RECORDED_HUMAN_ACCEPTANCE' if review['external_review_accepted'] else 'BLOCKED','scope':'Identity, expertise, conflicts, independence and source scope must be verified by a human maintainer'},
                {'id':'complete_occurrence_ordinal_and_detail_assessment','state':'PASS_RECORDED_ASSESSMENT' if review['ordinal_and_detail_complete'] else 'BLOCKED','scope':f"Recorded human ordinal assessments {review['ordinal_assessments']}/242; detail assessments {review['detail_assessments']}/242. Historical project exemplars are separate evidence; supported uncertainty is retained."},
                {'id':'complete_mark_coverage_assessment','state':'PASS_RECORDED_PHYSICAL_COVERAGE' if review['physical_mark_coverage_complete'] else 'BLOCKED','scope':f"Recorded physical coverage support {review['mark_groups_physical_coverage_supported']}/61 groups. Source-limited observations do not establish physical completeness; a human must verify evidence adequacy."}],
            'claim_boundary':'Acceptance is conditional on recorded human review and source adequacy, not a version number or a schema-valid declaration. No native correction, language, phonetic value or decipherment is automatically established.'}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,indent=2)+'\n',end='')
