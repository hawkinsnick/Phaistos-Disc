"""Evaluate recorded human review evidence; JSON syntax cannot verify a person.

Only a human maintainer may create the acceptance record after checking the
reviewer and evidence. The evaluator replays that recorded attestation; it does
not independently authenticate identity, expertise or truthful observations.
"""
import hashlib,json,pathlib,datetime
from review_packet import calculate as draft_v1,validate as validate_v1
R=pathlib.Path(__file__).resolve().parents[1]
RECORD='reviews/accepted-review.json'
def template(root=R):
    packet=draft_v1(root);packet['format']='PD-review-packet-v2'
    packet['review_record_license']=None
    corpus=json.loads((root/'corpus/disc.json').read_text())
    packet['source_evidence']=[]
    packet['mark_assessments']=[{'group_id':g['group_id'],'coverage':'unassessed',
        'entire_group_examined':False,'source_id':None,'source_sha256':None,
        'source_locator':None,'notes':'','observed_marks':[]} for g in corpus['groups']]
    return packet
def known_sources(root):
    registry=json.loads((root/'sources/sources.json').read_text());known=set()
    for s in registry:
        if s.get('full_source_sha256'):known.add((s['source_id'],s['full_source_sha256']))
        if s.get('manifest_path'):
            for p in json.loads((root/s['manifest_path']).read_text())['pages']:known.add((s['source_id'],p['sha256']))
    return known
def validate_submission(packet,root=R):
    expected=template(root)
    if not isinstance(packet,dict) or set(packet)!=set(expected) or packet['format']!='PD-review-packet-v2':raise ValueError('v2 packet fields')
    base={k:packet[k] for k in draft_v1(root)};base['format']='PD-review-packet-v1';result=validate_v1(base,root)
    known=known_sources(root);refs=set()
    photo_pages={g['group_id']:g['source_page_sha256'] for g in json.loads((root/'reviews/photographic-comparison-v1.json').read_text())['groups']}
    if not isinstance(packet['source_evidence'],list):raise ValueError('source evidence list')
    for e in packet['source_evidence']:
        if not isinstance(e,dict) or set(e)!={'source_id','sha256','locator'} or not isinstance(e['locator'],str) or not e['locator'].strip():raise ValueError('source evidence fields')
        if not isinstance(e['source_id'],str) or not isinstance(e['sha256'],str):raise ValueError('source identity must be text')
        ref=(e['source_id'],e['sha256'])
        if ref not in known or ref in refs:raise ValueError('unknown or duplicate authenticated source')
        refs.add(ref)
    marks=packet['mark_assessments']
    if not isinstance(marks,list) or len(marks)!=61 or any(not isinstance(m,dict) for m in marks):raise ValueError('complete group mark coverage required')
    if [m.get('group_id') for m in marks]!=[m['group_id'] for m in expected['mark_assessments']]:raise ValueError('missing, duplicate or foreign mark group')
    corpus=json.loads((root/'corpus/disc.json').read_text());members={g['group_id']:set(g['occurrence_ids']) for g in corpus['groups']}
    seen=set();assessed=adequate=0
    for m in marks:
        if set(m)!=set(expected['mark_assessments'][0]) or m['coverage'] not in ['unassessed','source_resolution_limited','physical_coverage_supported']:raise ValueError('mark assessment fields/coverage')
        if type(m['entire_group_examined']) is not bool or not isinstance(m['notes'],str) or len(m['notes'])>4000 or not isinstance(m['observed_marks'],list):raise ValueError('mark assessment types')
        if m['coverage']=='unassessed':
            if m['entire_group_examined'] or m['observed_marks'] or any(m[k] is not None for k in ['source_id','source_sha256','source_locator']):raise ValueError('unassessed group claims inspection')
        else:
            assessed+=1
            if (m['source_id'],m['source_sha256']) not in refs or not isinstance(m['source_locator'],str) or not m['source_locator'].strip() or not m['notes'].strip():raise ValueError('source-located mark assessment required')
            if m['source_id']=='olivier1975' and m['source_sha256']!=photo_pages[m['group_id']]:raise ValueError('photographic page does not contain this group')
            if not m['entire_group_examined']:raise ValueError('partial group cannot complete coverage assessment')
            adequate+=m['coverage']=='physical_coverage_supported'
        for mark in m['observed_marks']:
            if not isinstance(mark,dict) or set(mark)!={'mark_id','classification','target_occurrence_id','note'}:raise ValueError('observed mark fields')
            if not isinstance(mark['mark_id'],str) or not mark['mark_id'].strip() or mark['mark_id'] in seen:raise ValueError('duplicate/empty mark ID')
            seen.add(mark['mark_id'])
            if mark['classification'] not in ['incision_candidate','scratch_candidate','damage','unresolved'] or not isinstance(mark['note'],str) or not mark['note'].strip():raise ValueError('mark classification/note')
            if mark['target_occurrence_id'] is not None and mark['target_occurrence_id'] not in members[m['group_id']]:raise ValueError('mark target belongs to another group')
    if (result['reviewed_decisions'] or assessed) and not refs:raise ValueError('review needs authenticated source evidence')
    if result['reviewed_decisions'] or assessed:
        if packet['review_record_license'] not in ['MIT','CC0-1.0','CC-BY-4.0']:raise ValueError('reviewer redistribution license required')
    elif packet['review_record_license'] is not None:raise ValueError('unassigned draft must not claim reviewer license')
    if assessed and result['reviewed_decisions']==0:raise ValueError('mark-only draft needs attributed submission entries')
    result.update(mark_groups_assessed=assessed,mark_groups_physical_coverage_supported=adequate,
                  ordinal_assessments=sum(e['ordinal_checked'] for e in packet['entries']),
                  detail_assessments=sum(e['fine_detail_checked'] for e in packet['entries']))
    return result
def timestamp(value):
    if not isinstance(value,str):raise ValueError('timestamp required')
    when=datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
    if when.tzinfo is None:raise ValueError('timestamp timezone required')
    return when
def evaluate(root=R):
    absent={'record_present':False,'external_review_accepted':False,'ordinal_and_detail_complete':False,
            'physical_mark_coverage_complete':False,'final_2_0_allowed':False,
            'reviewed_slots':0,'ordinal_assessments':0,'detail_assessments':0,'mark_groups_assessed':0,
            'mark_groups_physical_coverage_supported':0,'receipt':None,
            'boundary':'No human acceptance record exists. Pending review is not completed review.'}
    record_path=root/RECORD
    if not record_path.exists():return absent
    record=json.loads(record_path.read_text())
    keys={'format','packet_path','packet_sha256','reviewer_name','maintainer_name','maintainer_is_human',
          'reviewer_is_human','identity_verified','expertise_verified','conflicts_reviewed',
          'independence_verified','redistribution_permission_verified','physical_evidence_adequacy_verified','verification_record','accepted_at'}
    if not isinstance(record,dict) or set(record)!=keys or record['format']!='PD-human-review-acceptance-v1':raise ValueError('human acceptance record fields')
    for k in ['reviewer_name','maintainer_name','verification_record']:
        if not isinstance(record[k],str) or not record[k].strip():raise ValueError('human verification attribution required')
    if record['maintainer_name'].strip().casefold()==record['reviewer_name'].strip().casefold():raise ValueError('reviewer cannot verify their own independence')
    required=['maintainer_is_human','reviewer_is_human','identity_verified','expertise_verified','conflicts_reviewed','independence_verified','redistribution_permission_verified']
    if any(record[k] is not True for k in required) or type(record['physical_evidence_adequacy_verified']) is not bool:raise ValueError('missing recorded human checks')
    if not isinstance(record['packet_path'],str):raise ValueError('packet path type')
    path=(root/record['packet_path']).resolve()
    if not path.is_relative_to((root/'reviews/submissions').resolve()) or not path.is_file():raise ValueError('review submission must be contained in reviews/submissions')
    raw=path.read_bytes()
    if len(raw)>4*1024*1024 or hashlib.sha256(raw).hexdigest()!=record['packet_sha256']:raise ValueError('submitted bytes/hash drift')
    packet=json.loads(raw);summary=validate_submission(packet,root)
    if packet['reviewer']['name']!=record['reviewer_name'] or packet['reviewer']['independence_declared'] is not True:raise ValueError('accepted reviewer identity/declaration mismatch')
    if timestamp(record['accepted_at'])<timestamp(packet['signed_at']):raise ValueError('acceptance predates review submission')
    external=summary['reviewed_decisions']==242 and summary['mark_groups_assessed']==61
    ordinal=summary['ordinal_assessments']==242 and summary['detail_assessments']==242
    marks=summary['mark_groups_physical_coverage_supported']==61 and record['physical_evidence_adequacy_verified']
    return {'record_present':True,'external_review_accepted':external,'ordinal_and_detail_complete':external and ordinal,
            'physical_mark_coverage_complete':external and marks,'final_2_0_allowed':external and ordinal and marks,
            'reviewed_slots':summary['reviewed_decisions'],'ordinal_assessments':summary['ordinal_assessments'],
            'detail_assessments':summary['detail_assessments'],'mark_groups_assessed':summary['mark_groups_assessed'],
            'mark_groups_physical_coverage_supported':summary['mark_groups_physical_coverage_supported'],
            'receipt':{'path':RECORD,'sha256':hashlib.sha256(record_path.read_bytes()).hexdigest(),'packet_path':record['packet_path'],'packet_sha256':record['packet_sha256']},
            'boundary':'Recorded human-maintainer attestation replayed, not electronic proof of identity or expertise. No native correction or decipherment is automatically adopted.'}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--template',action='store_true');p.add_argument('--submission',type=pathlib.Path);a=p.parse_args()
    if a.template:print(json.dumps(template(),ensure_ascii=False,separators=(',',':')))
    elif a.submission:
        if a.submission.stat().st_size>4*1024*1024:raise ValueError('packet size limit')
        print(json.dumps(validate_submission(json.loads(a.submission.read_text())),indent=2))
    else:print(json.dumps(evaluate(),indent=2))
