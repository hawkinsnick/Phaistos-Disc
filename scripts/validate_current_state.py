#!/usr/bin/env python3
"""Validate a source-attributed research edition without opening stronger claims."""
import collections,csv,hashlib,json,pathlib,re,sys
from jsonschema import Draft202012Validator,validators
from build_corpus import build
R=pathlib.Path(__file__).resolve().parents[1]
MEMBERS={'linear-a','linear-b','cypro-minoan','cretan-hieroglyphic','phaistos-disc'}
def require(ok,message):
    if not ok:raise ValueError(message)
def validate(root=R):
    def load(p):return json.loads((root/p).read_text())
    def sha(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
    version=(root/'VERSION').read_text().strip();require(re.fullmatch(r'(0\.[2-9]\.0|1\.[0-6]\.0|1\.2\.1|2\.0\.0-rc\.1)',version),'unsupported milestone version')
    require(re.search(r'^version: "'+re.escape(version)+'"$',(root/'CITATION.cff').read_text(),re.M),'citation version drift')
    for p in root.rglob('*.json'):
        if '.git' not in p.parts and 'output' not in p.parts:json.loads(p.read_text())
    for p in (root/'schemas').glob('*.json'):validators.validator_for(load(p.relative_to(root))).check_schema(load(p.relative_to(root)))
    sources=load('sources/sources.json');ids=[s['source_id'] for s in sources];require(len(ids)==len(set(ids)),'duplicate source')
    source={s['source_id']:s for s in sources};u=source['unicode17']
    require(sha(u['subset_path'])==u['subset_sha256']=='3cbbc1b6112208b4269bb7d01afc67d9cdaeaf1fe31c3a9359b6179194a7afb6','Unicode subset digest')
    require(sha(u['license_path'])==u['license_sha256']=='e7a93b009565cfce55919a381437ac4db883e9da2126fa28b91d12732bc53d96','Unicode license digest')
    require(u['record_license']=='Unicode-3.0','Unicode attribution')
    expected=[]
    for line in (root/u['subset_path']).read_text().splitlines():
        code,name,category,*_=line.split(';');expected.append({'sign_id':'PD-U'+code,'codepoint':'U+'+code,'character':chr(int(code,16)),'unicode_name':name,'unicode_category':category,'kind':'combining_mark' if code=='101FD' else 'base_sign','phonetic_value':None,'source_id':'unicode17'})
    registry=load('signs/unicode-registry.json');require(registry==expected and len(registry)==46,'Unicode registry mismatch')
    e=source['evans1909'];require(e['full_source_sha256']=='b06f8a04f3f7e33578f28aa0e88be600a13ebc6d03891a79c721558ca50c05e7' and e['acquisition_status']=='authenticated_bytes','primary source identity')
    require(e['publication_year']==1909 and e['rights_evidence_url'] and e['record_license'].startswith('Public-domain'),'primary source rights/attribution')
    policy=load('research/transcription-policy-v1.json');review=load('reviews/transcription-review-v1.json')
    require(sha(policy['input_path'])==policy['input_sha256']==review['input_sha256'],'transcription source pin')
    require(review['source_sha256']==e['full_source_sha256'] and review['external_peer_review_completed'] is False and review['epigraphic_truth_certified'] is False,'review scope promotion')
    require(set(review['checked_groups'])=={f'{f}{i}' for f,n in [('A',31),('B',30)] for i in range(1,n+1)} and len(review['checked_groups'])==61,'review coverage')
    crosswalk=load('signs/evans-unicode-crosswalk.json')['entries'];require(crosswalk==[{'evans_number':i,'sign_id':f'PD-U{0x101CF+i:X}'} for i in range(1,46)],'numbering crosswalk')
    corpus=load('corpus/disc.json');Draft202012Validator(load('schemas/disc-v1.schema.json')).validate(corpus)
    require(corpus==build(root),'native record/source-ledger mismatch')
    groups=corpus['groups'];occ=corpus['occurrences'];gids={g['group_id'] for g in groups};oids={o['occurrence_id'] for o in occ}
    require(len(gids)==len(groups)==61 and len(oids)==len(occ)==242,'native identity/accounting')
    # Independent lexical accounting checks the raw ledger without using builder output.
    with (root/policy['input_path']).open(newline='') as f:rows=list(csv.DictReader(f))
    lexical=collections.Counter(token for row in rows for token in row['sign_numbers'].split())
    encoded=collections.Counter('?' if o['sign_id'] is None else f"{int(o['sign_id'][4:],16)-0x101CF:02d}" for o in occ)
    require(lexical==encoded and lexical['?']==1,'source/encoded sign histogram drift')
    for face,n,slots in [('A',31,123),('B',30,119)]:
        selected=[g for g in groups if g['face_id']==f'PD-001-{face}'];require(len(selected)==n and sum(len(g['occurrence_ids']) for g in selected)==slots,'face group/slot count')
        require([g['outer_index'] for g in selected]==list(range(1,n+1)),'traversal index')
        require([g['evans_label'] for g in selected]==[f'{face}{i}' for i in range(n,0,-1)],'native numbering drift')
    require({o['occurrence_id'] for o in occ if o['sign_id'] is None}=={'PD-A-E24-S05'},'erased-slot identity')
    require(next(o for o in occ if o['occurrence_id']=='PD-B-E03-S05')['sign_id']=='PD-U101D6','B3 published figure reading drift')
    assertions=load('research/count-assertions.json')['assertions'];require(assertions[0]['total']==241 and assertions[-1]['total']==242,'source/project count conflation')
    if (root/'apparatus/claims.json').exists():
        claims=load('apparatus/claims.json');require(len(claims)==len({c['claim_id'] for c in claims})==7,'apparatus claim identities')
        for c in claims:
            require(c['source_id'] in source and c['locator'] and c['kind'] in {'reading','stroke','count','traversal'},'apparatus provenance/type')
            require(c['locus'] in gids|oids|{'PD-001'},'orphan apparatus locus')
        marks=load('apparatus/stroke-assertions.json');require(marks['statistical_use_allowed'] is False,'unresolved marks promoted to statistics')
        require(len(marks['marks'])==16 and sum(m['status']=='source_listed' for m in marks['marks'])==15,'source mark accounting')
        by_occ={o['occurrence_id']:o for o in occ}
        for m in marks['marks']:
            require(m['group_id'] in gids and m['source_id'] in source and m['locator'] and m['meaning'] is None and m['physical_position'] is None,'mark identity/provenance/meaning promotion')
            if m['target_occurrence_id'] is not None:
                require(m['target_occurrence_id'] in by_occ,'orphan mark target')
                target=by_occ[m['target_occurrence_id']]
                require(target['group_id']==m['group_id'] and target['sign_id']==f"PD-U{0x101CF+m['asserted_evans_sign']:X}",'mark/occurrence disagreement hidden')
        require([m['mark_id'] for m in marks['marks'] if m['target_occurrence_id'] is None]==marks['unresolved_target_assertions']==['PD-M002','PD-M004'],'unresolved mark target imputed')
    gates=load('research/experiment-gates.json')['experiments']
    for gate in gates:
        if gate['state']=='BLOCKED':require(gate['claim_allowed'] is False and gate['result_ref'] is None,'blocked gate leakage')
    for gid in ['cross-script-comparison','decipherment','external-critical-review']:
        gate=next(g for g in gates if g['id']==gid);require(gate['state']=='BLOCKED' and gate['claim_allowed'] is False,'unsupported scientific gate')
    state=load('analysis/current-status.json');require(state['repository_version']==version,'status version')
    counts={'physical_objects':1,'faces':2,'encoded_base_sign_types':45,'checked_graphical_witnesses':1,'source_checked_groups':len(groups),'source_checked_occurrence_slots':len(occ),'identified_slots':sum(o['sign_id'] is not None for o in occ),'unknown_slots':sum(o['sign_id'] is None for o in occ)}
    if (root/'reviews/photographic-comparison-v1.json').exists():
        from validate_witness_audit import validate as witness_validate
        witness_validate(root)
        counts['project_checked_photographic_witnesses']=1
    require(state['committed_evidence_counts']==counts,'evidence count drift')
    require(state['scientific_results']['decipherment_claim_allowed'] is False and state['scientific_results']['external_peer_review_completed'] is False,'scientific claim promotion')
    for item in state['evidence']:require(sha(item['path'])==item['sha256'],'evidence digest drift: '+item['path'])
    family=load('research/family-compatibility-v1.json');suite=load('research/family-compatibility-suite-v1.json')
    require(family['contract_version']==suite['required_contract_version']==suite['suite_version'] and family['contract_version'] in ['1.1.0','1.2.0'],'family version')
    require(set(family['members'])==set(suite['required_members'])==MEMBERS and len(family['members'])==5,'family membership')
    require(family['member_version']==version and family['member']=='Phaistos-Disc','family member version')
    require(family['membership_boundary']=='Native evidence only; membership implies no linguistic affinity, shared sign identities, or pooled analysis.','family boundary')
    for path in suite['required_artifacts']:require((root/path).is_file(),'missing family artifact '+path)
    v=Draft202012Validator(load('schemas/aegean-interop-v0.1.schema.json'))
    for member in MEMBERS:
        good={'project':member,'record_id':'fixture','assertions':[{'assertion_type':'metadata','value':None,'status':'published','provenance':[{'source_id':'fixture'}]}],'rights':{'record_license':'NOASSERTION'}};require(v.is_valid(good),'interchange member')
        for mutation in ['rights','provenance','unknown']:
            bad=json.loads(json.dumps(good))
            if mutation=='rights':del bad['rights']
            elif mutation=='provenance':bad['assertions'][0]['provenance']=[]
            else:bad['unknown']=True
            require(not v.is_valid(bad),'invalid interchange accepted')
    if (root/'spatial/group-anchors.json').exists():
        anchors=load('spatial/group-anchors.json');frames={f['frame_id']:f for f in load('spatial/frames.json')}
        require(len(anchors)==len({a['group_id'] for a in anchors})==61 and {a['group_id'] for a in anchors}==gids,'anchor coverage')
        for a in anchors:
            require(a['frame_id'] in frames and 0<=a['x']<=1 and 0<=a['y']<=1 and a['method']=='manual_group_region_anchor' and a['approximate'] is True and a['source_id']=='evans1909','anchor provenance/coordinate semantics')
            require(a['frame_id'].endswith('-'+a['group_id'][3]),'anchor face mismatch')
        for frame in frames.values():require(frame['source_sha256']==e['full_source_sha256'] and frame['coordinate_scope']=='historical_figure_page','spatial source identity')
    if (root/'analysis/descriptive-v1.json').exists():
        from analyze import analyze
        require(load('analysis/descriptive-v1.json')==analyze(root),'descriptive replay drift')
    if (root/'exports/aegean-interop.json').exists():
        records=load('exports/aegean-interop.json');require(len(records)==242,'export coverage')
        for record in records:v.validate(record);require(record['rights']['record_license']=='MIT' and len(record['rights']['third_party_material'])==2,'export rights lost')
        from export_corpus import export_records
        require(records==export_records(root),'export/native mismatch')
    if (root/'research/family-readiness-v1.json').exists():
        readiness=load('research/family-readiness-v1.json');require(readiness['target_versions']['Phaistos-Disc']==version,'readiness member version')
        require(readiness['pooled_analysis_allowed'] is False and readiness['linguistic_known_answer_control']['state']=='BLOCKED','family readiness promotion')
    if version=='1.0.0' and (root/'analysis/acceptance-1.0.json').exists():
        from acceptance import calculate
        acceptance=load('analysis/acceptance-1.0.json')
        require(acceptance==calculate(root) and acceptance['status']=='PASS' and version=='1.0.0','1.0 acceptance drift')
    if (root/'analysis/apparatus-sensitivity-v1.json').exists():
        from apparatus_sensitivity import calculate as sensitivity_calculate
        require(load('analysis/apparatus-sensitivity-v1.json')==sensitivity_calculate(root),'apparatus scenario replay drift')
    if (root/'reviews/occurrence-audit-v1.json').exists():
        from occurrence_audit import calculate as occurrence_calculate
        require(load('reviews/occurrence-audit-v1.json')==occurrence_calculate(root),'occurrence evidence replay drift')
    return {'status':'PASS','version':version,'evidence_counts':counts,'external_review':'BLOCKED','decipherment':'BLOCKED'}
if __name__=='__main__':
    try:print(json.dumps(validate()))
    except Exception as e:print('FAIL:',e,file=sys.stderr);sys.exit(1)
