"""Prepare/validate reviewer submissions; never adopt them or certify independence."""
import argparse,hashlib,json,pathlib,datetime
R=pathlib.Path(__file__).resolve().parents[1]
def calculate(root=R):
    corpus=(root/'corpus/disc.json').read_bytes();ids=[o['occurrence_id'] for o in json.loads(corpus)['occurrences']]
    return {'format':'PD-review-packet-v1','native_corpus_sha256':hashlib.sha256(corpus).hexdigest(),
            'occurrence_audit_sha256':hashlib.sha256((root/'reviews/occurrence-audit-v1.json').read_bytes()).hexdigest(),
            'reviewer':{'name':None,'affiliation':None,'expertise':None,'conflicts':None,'independence_declared':None},
            'signed_at':None,'entries':[{'occurrence_id':oid,'decision':'unreviewed','source_locator':None,'note':'','ordinal_checked':False,'fine_detail_checked':False} for oid in ids]}
def validate(packet,root=R):
    expected=calculate(root)
    if not isinstance(packet,dict) or set(packet)!=set(expected):raise ValueError('packet fields/schema')
    for k in ['format','native_corpus_sha256','occurrence_audit_sha256']:
        if packet[k]!=expected[k]:raise ValueError('source identity drift')
    reviewer=packet['reviewer']
    if not isinstance(reviewer,dict) or set(reviewer)!=set(expected['reviewer']):raise ValueError('reviewer fields')
    for k in ['name','affiliation','expertise','conflicts']:
        if reviewer[k] is not None and (not isinstance(reviewer[k],str) or not reviewer[k].strip() or len(reviewer[k])>2000):raise ValueError('reviewer text')
    if reviewer['independence_declared'] is not None and type(reviewer['independence_declared']) is not bool:raise ValueError('independence declaration type')
    if not isinstance(packet['entries'],list) or len(packet['entries'])!=242:raise ValueError('complete slot coverage required')
    if [e.get('occurrence_id') for e in packet['entries']]!=[e['occurrence_id'] for e in expected['entries']]:raise ValueError('missing, reordered, duplicate or foreign occurrence')
    decisions=0
    for e in packet['entries']:
        if set(e)!=set(expected['entries'][0]) or e['decision'] not in ['unreviewed','compatible','conflict','unresolvable']:raise ValueError('entry fields/decision')
        if type(e['ordinal_checked']) is not bool or type(e['fine_detail_checked']) is not bool:raise ValueError('check flag type')
        if not isinstance(e['note'],str) or len(e['note'])>4000:raise ValueError('entry note')
        if e['decision']=='unreviewed':
            if e['ordinal_checked'] or e['fine_detail_checked'] or e['source_locator'] is not None:raise ValueError('unreviewed entry claims verification')
        else:
            decisions+=1
            if not isinstance(e['source_locator'],str) or not e['source_locator'].strip():raise ValueError('reviewed decision needs source locus')
            if e['decision'] in ['conflict','unresolvable'] and not e['note'].strip():raise ValueError('conflict/uncertainty needs explanation')
    if decisions:
        if not all(reviewer[k] for k in ['name','expertise','conflicts']) or reviewer['independence_declared'] is None:raise ValueError('attributed submission required')
        if not isinstance(packet['signed_at'],str):raise ValueError('submission timestamp required')
        when=datetime.datetime.fromisoformat(packet['signed_at'].replace('Z','+00:00'))
        if when.tzinfo is None:raise ValueError('timestamp timezone required')
    elif packet['signed_at'] is not None:raise ValueError('draft must not be signed')
    return {'status':'VALID_DRAFT' if not decisions else 'VALID_UNVERIFIED_SUBMISSION',
            'reviewed_decisions':decisions,'unreviewed':242-decisions,'scientific_gate_opened':False,
            'native_changes_applied':False,'identity_or_independence_verified':False,
            'boundary':'Syntax, provenance and coverage checks only. Reviewer identity, expertise, conflicts and actual independence require human verification; no submission is automatically accepted as external review.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--validate',type=pathlib.Path);a=p.parse_args()
    if a.validate:
        if a.validate.stat().st_size>4*1024*1024:raise ValueError('packet size limit')
        print(json.dumps(validate(json.loads(a.validate.read_text()))))
    else:print(json.dumps(calculate(),ensure_ascii=False,separators=(',',':'))+'\n',end='')
