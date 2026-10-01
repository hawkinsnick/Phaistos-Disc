"""Check typed readiness, source identities and scientific claim boundaries."""
import hashlib, json, pathlib, re, sys
R = pathlib.Path(__file__).resolve().parents[1]
REPOS = {'Linear-A', 'Linear-B', 'Cypro-Minoan', 'Cretan-hieroglpyhs', 'Phaistos-Disc'}

def validate(root=R):
    report = json.loads((root / 'research/family-readiness-v1.json').read_text())
    family = json.loads((root / 'research/family-compatibility-v1.json').read_text())
    if not report['family_contract_version'] == family['contract_version'] == '1.2.0':
        raise ValueError('family readiness invariant violated')
    if not set(report['target_versions']) == REPOS:
        raise ValueError('family readiness invariant violated')
    if not report['target_versions'][family['member']] == (root / 'VERSION').read_text().strip():
        raise ValueError('family readiness invariant violated')
    if not ({m['repository'] for m in report['members']} == REPOS and len(report['members']) == 5):
        raise ValueError('family readiness invariant violated')
    if not (report['pooled_analysis_allowed'] is False and report['cross_script_identity_claim_allowed'] is False):
        raise ValueError('family readiness invariant violated')
    if not report['linguistic_known_answer_control']['state'] == 'BLOCKED':
        raise ValueError('family readiness invariant violated')
    if not report['software_known_answer_control']['scope'].startswith('Frequency/entropy arithmetic'):
        raise ValueError('family readiness invariant violated')
    for member in report['members']:
        if not (member['comparison_status'] == 'BLOCKED' and member['blocking_dependencies']):
            raise ValueError('family readiness invariant violated')
        if member['snapshot_commit'] is not None:
            if not re.fullmatch('[0-9a-f]{40}', member['snapshot_commit']):
                raise ValueError('family readiness invariant violated')
        for e in member['native_evidence']:
            if not (re.fullmatch('[0-9a-f]{64}', e['sha256']) and e['path']):
                raise ValueError('family readiness invariant violated')
            if member['repository'] == family['member']:
                if not hashlib.sha256((root / e['path']).read_bytes()).hexdigest() == e['sha256']:
                    raise ValueError(e['path'])
        for metric in member['metrics'].values():
            if not (metric['unit'] and metric['definition']):
                raise ValueError('family readiness invariant violated')
            if metric['status'] == 'unknown':
                if not metric['value'] is None:
                    raise ValueError('family readiness invariant violated')
            elif not (metric['status'] == 'measured' and isinstance(metric['value'], int) and (metric['value'] >= 0)):
                raise ValueError('family readiness invariant violated')
    disc = next((m for m in report['members'] if m['repository'] == 'Phaistos-Disc'))
    if not (disc['metrics']['physical_objects']['value'] == 1 and disc['metrics']['faces']['value'] == 2):
        raise ValueError('family readiness invariant violated')
    if not (disc['metrics']['graphical_slots']['value'] == 242 and disc['metrics']['identified_slots']['value'] == 241):
        raise ValueError('family readiness invariant violated')
    return {'status': 'PASS', 'family_contract': '1.2.0', 'members': 5, 'pooled_analysis': 'BLOCKED', 'linguistic_control': 'BLOCKED'}
if __name__ == '__main__':
    try:
        print(json.dumps(validate()))
    except Exception as e:
        print('FAIL:', e, file=sys.stderr)
        sys.exit(1)
