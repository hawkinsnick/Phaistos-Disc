"""Compute release-candidate readiness without granting final critical acceptance."""
import hashlib,json,pathlib
from occurrence_audit import calculate as occurrences
from source_coverage import calculate as sources
from research_suite import calculate as research
from review_packet import calculate as packet,validate as validate_packet
R=pathlib.Path(__file__).resolve().parents[1]
def calculate(root=R):
    artifacts=[('reviews/occurrence-audit-v1.json',occurrences),('analysis/source-coverage-v1.json',sources),('analysis/research-suite-v2.json',research),('reviews/review-packet-v1.json',packet)]
    pins=[]
    for path,replay in artifacts:
        raw=(root/path).read_bytes()
        if json.loads(raw)!=replay(root):raise ValueError('acceptance replay drift: '+path)
        pins.append({'path':path,'sha256':hashlib.sha256(raw).hexdigest()})
    audit=occurrences(root);draft=validate_packet(packet(root),root)
    gates=json.loads((root/'research/experiment-gates.json').read_text())['experiments']
    external=next(g for g in gates if g['id']=='external-critical-review')
    if external['state']!='BLOCKED' or external['claim_allowed'] is not False or external['result_ref'] is not None:raise ValueError('unsupported review acceptance')
    return {'target_release':'2.0.0','candidate_release':'2.0.0-rc.1',
            'engineering_artifact_replay':'PASS','candidate_ready':True,
            'final_2_0_allowed':False,'status':'BLOCKED_FOR_FINAL_2_0',
            'native_corpus_sha256':hashlib.sha256((root/'corpus/disc.json').read_bytes()).hexdigest(),
            'artifact_pins':pins,'occurrence_audit_counts':audit['coverage'],
            'review_packet_status':draft['status'],
            'acceptance_requirements':[
                {'id':'source_linked_occurrence_ledger','state':'PASS','scope':'242 rows; bounded inherited evidence, not new certification'},
                {'id':'reproducible_research_and_submission_tools','state':'PASS_ARTIFACT_REPLAY','scope':'Byte-pinned software descriptions and draft submission validation; CI verifies browser and adversarial tests separately'},
                {'id':'independent_human_epigraphic_review','state':'BLOCKED','scope':'Identity, expertise, conflicts, independence and source scope must be verified by a human maintainer'},
                {'id':'complete_occurrence_ordinal_and_detail_assessment','state':'BLOCKED','scope':'196 individual ordinals not yet certified; no exhaustive fine-detail assessment. An uncertainty decision is valid when supported and explicitly scoped'},
                {'id':'complete_mark_coverage_assessment','state':'BLOCKED','scope':'Source-located stroke candidates are not a complete physical mark inventory'}],
            'claim_boundary':'This is a 2.0 release candidate for tools and evidence organization. It is not the independently reviewed critical edition proposed as final 2.0; no language, phonetic value or decipherment is established.'}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,indent=2)+'\n',end='')
