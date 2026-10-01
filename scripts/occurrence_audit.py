"""Materialize occurrence evidence without extrapolating exemplar certification."""
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def calculate(root=R):
    load=lambda p:json.loads((root/p).read_text())
    corpus=load('corpus/disc.json');photo={g['group_id']:g for g in load('reviews/photographic-comparison-v1.json')['groups']}
    cross=load('signs/olivier1975-exemplar-crosswalk.json')
    exemplars=cross['entries']+[cross['unknown_exemplar']]
    refs={e['native_occurrence_id']:e for e in exemplars}
    if len(refs)!=len(exemplars):raise ValueError('duplicate exemplar target')
    groups={g['group_id']:g for g in corpus['groups']}
    rows=[]
    for o in corpus['occurrences']:
        g=groups[o['group_id']];p=photo[g['group_id']];e=refs.get(o['occurrence_id'])
        if e and e.get('native_sign_id')!=o['sign_id']:raise ValueError('exemplar sign mismatch')
        rows.append({'occurrence_id':o['occurrence_id'],'group_id':o['group_id'],'native_sign_id':o['sign_id'],
                     'native_figure_locator':g['provenance']['locator'],
                     'photo_group_locator':p['locator'],'photo_group_sha256':p['source_page_sha256'],
                     'source_exemplar':e['source_exemplar'] if e else None,
                     'source_exemplar_page':e['source_page'] if e else None,
                     'ordinal_evidence':'published_exemplar_crosswalk' if e else 'not_individually_certified',
                     'fine_stamp_detail_certified':False,'physical_position':None,
                     'external_review_completed':False})
    return {'format':'occurrence-audit-v1','native_corpus_sha256':hashlib.sha256((root/'corpus/disc.json').read_bytes()).hexdigest(),
            'coverage':{'slots':len(rows),'source_labeled_exemplars':len(refs),'ordinal_not_individually_certified':len(rows)-len(refs),'fine_detail_certified':0,'external_reviews':0},
            'scope':'Evidence ledger for every native slot. Group-level compatibility does not certify individual stamp detail or every source ordinal. Exemplar mappings are inherited from the bounded project source check, not a new independent review.',
            'rows':rows}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,separators=(',',':'))+'\n',end='')
