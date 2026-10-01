#!/usr/bin/env python3
"""Check typed readiness, source identities and scientific claim boundaries."""
import hashlib,json,pathlib,re,sys
R=pathlib.Path(__file__).resolve().parents[1]
REPOS={'Linear-A','Linear-B','Cypro-Minoan','Cretan-hieroglpyhs','Phaistos-Disc'}
def validate(root=R):
    report=json.loads((root/'research/family-readiness-v1.json').read_text());family=json.loads((root/'research/family-compatibility-v1.json').read_text())
    assert report['family_contract_version']==family['contract_version']=='1.2.0'
    assert set(report['target_versions'])==REPOS
    assert report['target_versions'][family['member']]==(root/'VERSION').read_text().strip()
    assert {m['repository'] for m in report['members']}==REPOS and len(report['members'])==5
    assert report['pooled_analysis_allowed'] is False and report['cross_script_identity_claim_allowed'] is False
    assert report['linguistic_known_answer_control']['state']=='BLOCKED'
    assert report['software_known_answer_control']['scope'].startswith('Frequency/entropy arithmetic')
    for member in report['members']:
        assert member['comparison_status']=='BLOCKED' and member['blocking_dependencies']
        if member['snapshot_commit'] is not None:assert re.fullmatch('[0-9a-f]{40}',member['snapshot_commit'])
        for e in member['native_evidence']:
            assert re.fullmatch('[0-9a-f]{64}',e['sha256']) and e['path']
            if member['repository']==family['member']:
                assert hashlib.sha256((root/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
        for metric in member['metrics'].values():
            assert metric['unit'] and metric['definition']
            if metric['status']=='unknown':assert metric['value'] is None
            else:assert metric['status']=='measured' and isinstance(metric['value'],int) and metric['value']>=0
    disc=next(m for m in report['members'] if m['repository']=='Phaistos-Disc')
    assert disc['metrics']['physical_objects']['value']==1 and disc['metrics']['faces']['value']==2
    assert disc['metrics']['graphical_slots']['value']==242 and disc['metrics']['identified_slots']['value']==241
    return {'status':'PASS','family_contract':'1.2.0','members':5,'pooled_analysis':'BLOCKED','linguistic_control':'BLOCKED'}
if __name__=='__main__':
    try:print(json.dumps(validate()))
    except Exception as e:print('FAIL:',e,file=sys.stderr);sys.exit(1)
