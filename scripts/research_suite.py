"""Retrospective, conditional descriptions of one object; no linguistic tests."""
import collections,hashlib,json,math,pathlib,random
R=pathlib.Path(__file__).resolve().parents[1]
def metrics(groups):
    complete=[tuple(g) for g in groups if None not in g]
    counts=collections.Counter(complete)
    adjacent=[(a,b) for g in groups for a,b in zip(g,g[1:]) if a is not None and b is not None]
    return {'groups':len(groups),'complete_groups':len(complete),'incomplete_groups':len(groups)-len(complete),
            'eligible_adjacent_pairs':len(adjacent),'identical_adjacent_pairs':sum(a==b for a,b in adjacent),
            'identical_complete_group_pairs':sum(n*(n-1)//2 for n in counts.values()),
            'distinct_complete_group_sequences':len(counts)}
def calculate(root=R):
    spec=json.loads((root/'research/descriptive-protocol-v2.json').read_text())
    if spec['seed']!=20261001 or spec['replicates']!=1000 or spec['unknown_policy']!='keep_unknown_slots_fixed':raise ValueError('frozen diagnostic policy drift')
    if spec['registration_scope']!='retrospective_before_suite_execution_not_before_corpus_inspection':raise ValueError('exposure history misrepresented')
    if hashlib.sha256((root/'scripts/research_suite.py').read_bytes()).hexdigest()!=spec['implementation_sha256']:raise ValueError('frozen implementation drift')
    raw=(root/'corpus/disc.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=spec['native_corpus_sha256']:raise ValueError('native bytes drift')
    corpus=json.loads(raw);occ={o['occurrence_id']:o['sign_id'] for o in corpus['occurrences']}
    rng=random.Random(spec['seed']);faces={}
    for face in ['A','B']:
        groups=[[occ[k] for k in g['occurrence_ids']] for g in corpus['groups'] if g['face_id']=='PD-001-'+face]
        observed=metrics(groups);values=[s for g in groups for s in g if s is not None]
        samples={k:[] for k in spec['diagnostic_statistics']}
        for _ in range(spec['replicates']):
            shuffled=values.copy();rng.shuffle(shuffled);it=iter(shuffled)
            synthetic=[[next(it) if s is not None else None for s in g] for g in groups]
            m=metrics(synthetic)
            for k in samples:samples[k].append(m[k])
        summaries={}
        for k,x in samples.items():
            ordered=sorted(x);n=len(x)
            summaries[k]={'mean':math.fsum(x)/n,'minimum':ordered[0],'maximum':ordered[-1],
                          'q025':ordered[math.floor(.025*(n-1))],'q975':ordered[math.floor(.975*(n-1))]}
        faces[face]={'observed':observed,'reversed_group_sequences':metrics([list(reversed(g)) for g in groups]),'shuffle_reference':summaries}
    return {'format':'descriptive-research-suite-v2','protocol_sha256':hashlib.sha256((root/'research/descriptive-protocol-v2.json').read_bytes()).hexdigest(),
            'implementation_sha256':hashlib.sha256((root/'scripts/research_suite.py').read_bytes()).hexdigest(),
            'native_corpus_sha256':spec['native_corpus_sha256'],'physical_objects':1,'faces':faces,
            'seed':spec['seed'],'replicates_per_face':spec['replicates'],
            'reference_distribution':'Within each face, shuffle identified glyph labels among identified slots; hold unknown positions, per-face label counts and graphical group lengths fixed.',
            'quantiles':'Sorted empirical reference values at floor(p*(n-1)); not population confidence intervals.',
            'p_values':None,'linguistic_inference_allowed':False,'independent_replication':False,
            'interpretation':'Diagnostic departures from this particular exchangeability model cannot establish words, morphology, language, reading direction or decipherment. A/B are parts of one object and are not independent replications.'}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,indent=2)+'\n',end='')
