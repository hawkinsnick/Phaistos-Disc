#!/usr/bin/env python3
"""Source-conditional descriptions. No population inference or phonetic output."""
import collections,hashlib,json,math,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def summarize(sequences):
    frequencies=collections.Counter(s for seq in sequences for s in seq if s is not None)
    known=sum(frequencies.values());slots=sum(map(len,sequences))
    pairs=collections.Counter((a,b) for seq in sequences for a,b in zip(seq,seq[1:]) if a is not None and b is not None)
    exact=collections.Counter(tuple(seq) for seq in sequences if all(s is not None for s in seq))
    return {'groups':len(sequences),'slots':slots,'identified_slots':known,'unknown_slots':slots-known,'frequency_denominator':'identified_slots_only','sign_frequencies':dict(sorted(frequencies.items())),'identified_sign_types':len(frequencies),'shannon_bits':round(-sum((n/known)*math.log2(n/known) for n in frequencies.values()),12) if known else None,'group_length_histogram':{str(k):v for k,v in sorted(collections.Counter(map(len,sequences)).items())},'within_group_possible_pairs':sum(max(0,len(seq)-1) for seq in sequences),'within_group_identified_pairs':sum(pairs.values()),'adjacent_pair_frequencies':{' > '.join(k):v for k,v in sorted(pairs.items())},'repeated_identified_groups':[{'sequence':list(seq),'occurrences':n} for seq,n in sorted(exact.items()) if n>1]}
def analyze(root=R):
    raw=(root/'corpus/disc.json').read_bytes();corpus=json.loads(raw);occ={o['occurrence_id']:o for o in corpus['occurrences']}
    by_face={f:[[occ[oid]['sign_id'] for oid in g['occurrence_ids']] for g in corpus['groups'] if g['face_id']==f'PD-001-{f}'] for f in 'AB'}
    directions=[]
    for da in ['outer_to_inner','inner_to_outer']:
        for db in ['outer_to_inner','inner_to_outer']:
            views={}
            for face,direction in [('A',da),('B',db)]:
                seqs=by_face[face]
                if direction=='inner_to_outer':seqs=[list(reversed(seq)) for seq in reversed(seqs)]
                views[face]=summarize(seqs)
            directions.append({'directions':{'A':da,'B':db},'faces':views,'physical_objects':1,'interpretation':'Alternative project traversal, not independent data or linguistic reading.'})
    signs=[s['sign_id'] for s in json.loads((root/'signs/unicode-registry.json').read_text()) if s['kind']=='base_sign']
    assignments=[]
    for sign in signs:
        seqs=[[sign if s is None else s for s in seq] for seq in by_face['A']];summary=summarize(seqs);assignments.append({'hypothetical_sign_id':sign,'A_shannon_bits':summary['shannon_bits'],'A_identified_slots':summary['identified_slots']})
    return {'analysis_id':'PD-DESCRIPTIVE-V1','corpus_sha256':hashlib.sha256(raw).hexdigest(),'policy_sha256':hashlib.sha256((root/'research/transcription-policy-v1.json').read_bytes()).hexdigest(),'sampling_unit':'one physical object; faces and groups are nested descriptive partitions','statistical_inference_allowed':False,'linguistic_claim_allowed':False,'group_semantics':'source-delimited graphical groups, not established words','baseline_faces':{f:summarize(by_face[f]) for f in 'AB'},'directional_sensitivity':directions,'unknown_slot_sensitivity':{'method':'Enumerate all45 encoded base signs as unweighted hypothetical completions of the one unknown slot; none is adopted as evidence.','assignments':assignments,'A_entropy_complete_hypotheses_min':min(x['A_shannon_bits'] for x in assignments),'A_entropy_complete_hypotheses_max':max(x['A_shannon_bits'] for x in assignments),'missing_slot_baseline_entropy':summarize(by_face['A'])['shannon_bits']},'boundaries':['Stroke assertions excluded: coverage and source targets unresolved.','No transitions across graphical-group boundaries.','No p-values, bootstrap faces-as-documents, population generalization or cross-script pooling.']}
if __name__=='__main__':
    (R/'analysis/descriptive-v1.json').write_text(json.dumps(analyze(),ensure_ascii=False,indent=2)+'\n')
    print('PASS: descriptive artifact written; stronger claims remain blocked')
