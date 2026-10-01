#!/usr/bin/env python3
"""Fail closed on source, native-record, family and gate integrity drift."""
import hashlib,json,pathlib,re,sys
from jsonschema import Draft202012Validator,validators
R=pathlib.Path(__file__).resolve().parents[1]
MEMBERS={'linear-a','linear-b','cypro-minoan','cretan-hieroglyphic','phaistos-disc'}
def require(ok,message):
    if not ok:raise ValueError(message)
def validate(root=R):
    def load(p):return json.loads((root/p).read_text(encoding='utf-8'))
    def digest(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
    version=(root/'VERSION').read_text().strip()
    require(version=='0.1.0','foundation version')
    require(re.search(r'^version: "'+re.escape(version)+'"$',(root/'CITATION.cff').read_text(),re.M),'citation version')
    for p in root.rglob('*.json'):json.loads(p.read_text())
    for p in (root/'schemas').glob('*.json'):validators.validator_for(load(p.relative_to(root))).check_schema(load(p.relative_to(root)))
    sources=load('sources/sources.json');ids=[s['source_id'] for s in sources]
    require(len(ids)==len(set(ids)),'duplicate source');by_source={s['source_id']:s for s in sources}
    unicode=by_source['unicode17']
    require(unicode['full_source_sha256']=='2e1efc1dcb59c575eedf5ccae60f95229f706ee6d031835247d843c11d96470c','full Unicode source pin')
    require(digest(unicode['subset_path'])==unicode['subset_sha256']=='3cbbc1b6112208b4269bb7d01afc67d9cdaeaf1fe31c3a9359b6179194a7afb6','Unicode subset digest')
    require(digest(unicode['license_path'])==unicode['license_sha256']=='e7a93b009565cfce55919a381437ac4db883e9da2126fa28b91d12732bc53d96','Unicode license digest')
    require(unicode['record_license']=='Unicode-3.0' and unicode['acquisition_status']=='authenticated_bytes','Unicode attribution')
    for sid in ['heraklion-catalogue','heraklion-exhibit']:
        require(by_source[sid]['acquisition_status']=='blocked_http_502' and by_source[sid]['record_license']=='NOASSERTION','museum evidence/rights promotion')
    expected=[]
    for line in (root/unicode['subset_path']).read_text().splitlines():
        code,name,category,*_=line.split(';')
        expected.append({'sign_id':'PD-U'+code,'codepoint':'U+'+code,'character':chr(int(code,16)),'unicode_name':name,'unicode_category':category,'kind':'combining_mark' if code=='101FD' else 'base_sign','phonetic_value':None,'source_id':'unicode17'})
    signs=load('signs/unicode-registry.json');require(signs==expected,'registry differs from Unicode witness')
    require([s['codepoint'] for s in signs]==[f'U+{c:X}' for c in range(0x101D0,0x101FE)],'Unicode repertoire coverage')
    sign_ids={s['sign_id'] for s in signs}
    corpus=load('corpus/disc.json');Draft202012Validator(load('schemas/disc-v0.1.schema.json')).validate(corpus)
    require({f['face_id'] for f in corpus['faces']}=={'PD-001-A','PD-001-B'},'face identities')
    for f in corpus['faces']:
        require(f['face_id']==f"PD-001-{f['label']}",'face label alignment')
        require(f['reading_direction'] is None and f['starting_point'] is None and f['coordinate_frame'] is None,'unverified face geometry')
    for a in corpus['inventory_assertions']:require(a['source_id'] in by_source,'orphan inventory source')
    witnesses={w['witness_id']:w for w in corpus['witnesses']}
    require(len(witnesses)==len(corpus['witnesses']),'duplicate witness')
    for w in witnesses.values():require(w['source_id'] in by_source,'orphan witness source')
    occurrences={o['occurrence_id']:o for o in corpus['occurrences']}
    require(len(occurrences)==len(corpus['occurrences']),'duplicate occurrence')
    for o in occurrences.values():
        require(o['witness_id'] in witnesses,'orphan occurrence witness')
        require(o['provenance']['source_id'] in by_source,'orphan occurrence source')
        require(o['sign_id'] is None or o['sign_id'] in sign_ids,'unknown sign identifier')
        require(set(o['alternatives'])<=sign_ids,'unknown sign alternative')
        require(o['sign_id'] is not None or o['uncertainty']!='certain','certain unidentified sign')
        if o['position']:
            require(o['position']['image_source_id'] in by_source,'orphan coordinate image')
            require(corpus['faces'][0 if o['face_id'].endswith('A') else 1]['coordinate_frame'] is not None,'coordinate without checked frame')
    require(len({g['group_id'] for g in corpus['groups']})==len(corpus['groups']),'duplicate group')
    for g in corpus['groups']:
        require(g['witness_id'] in witnesses and g['provenance']['source_id'] in by_source,'orphan group provenance')
        for oid in g['occurrence_ids']:
            require(oid in occurrences,'orphan group occurrence')
            require(occurrences[oid]['witness_id']==g['witness_id'] and occurrences[oid]['face_id']==g['face_id'],'mixed witness/face group')
    # This foundation is explicitly not a transcription release. New evidence needs a new reviewed gate/version.
    require(not witnesses and not occurrences and not corpus['groups'],'unchecked foundation promoted to transcription')
    require(corpus['actual_sign_impression_total'] is None,'unverified impression total')
    gates=load('research/experiment-gates.json')['experiments']
    require({g['id'] for g in gates}=={'transcription-release','frequency-analysis','cross-script-comparison','decipherment'} and len(gates)==4,'gate coverage')
    for g in gates:require(g['state']=='BLOCKED' and g['claim_allowed'] is False and g['result_ref'] is None and g['requires'],'gate leakage')
    family=load('research/family-compatibility-v1.json');suite=load('research/family-compatibility-suite-v1.json')
    require(family['contract_version']==suite['required_contract_version']==suite['suite_version']=='1.1.0','family version')
    require(set(family['members'])==set(suite['required_members'])==MEMBERS and len(family['members'])==5,'family membership')
    require(family['member']=='Phaistos-Disc' and family['member_version']==version,'family member version')
    require(family['membership_boundary']=='Native evidence only; membership implies no linguistic affinity, shared sign identities, or pooled analysis.','family claim boundary')
    for p in suite['required_artifacts']:require((root/p).is_file(),'missing family artifact '+p)
    interop=Draft202012Validator(load('schemas/aegean-interop-v0.1.schema.json'))
    for member in MEMBERS:
        good={'project':member,'record_id':'fixture','assertions':[{'assertion_type':'metadata','value':None,'status':'published','provenance':[{'source_id':'fixture'}]}],'rights':{'record_license':'NOASSERTION'}}
        require(interop.is_valid(good),'interchange member rejected')
        for mutation in ['rights','provenance','unknown']:
            bad=json.loads(json.dumps(good))
            if mutation=='rights':del bad['rights']
            elif mutation=='provenance':bad['assertions'][0]['provenance']=[]
            else:bad['unexpected']=True
            require(not interop.is_valid(bad),'bad interchange accepted')
    status=load('analysis/current-status.json');require(status['repository_version']==version,'status version')
    counts={'object_scaffolds':1,'faces':len(corpus['faces']),'encoded_base_signs':sum(s['kind']=='base_sign' for s in signs),'combining_marks':sum(s['kind']=='combining_mark' for s in signs),'source_checked_transcriptions':sum(w['verification_status']=='source_checked' for w in witnesses.values()),'source_checked_occurrences':sum(o['provenance']['verification_status']=='source_checked' for o in occurrences.values())}
    require(status['committed_evidence_counts']==counts,'evidence count drift')
    require(status['scientific_results']=={'frequency_analysis':'BLOCKED','cross_script_comparison':'BLOCKED','decipherment_claim_allowed':False},'unsupported scientific claim')
    for e in status['evidence']:require(digest(e['path'])==e['sha256'],'evidence digest drift '+e['path'])
    return {'status':'PASS','version':version,'evidence_counts':counts,'scientific_gates':'BLOCKED'}
if __name__=='__main__':
    try:print(json.dumps(validate()))
    except Exception as e:print('FAIL:',e,file=sys.stderr);sys.exit(1)
