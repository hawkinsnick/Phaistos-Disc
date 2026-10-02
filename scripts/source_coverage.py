"""Typed source coverage and lineage, with absence of review preserved."""
import hashlib,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
ROLES={'unicode17':'encoding_standard','unicode-proposal2006':'encoding_proposal','heraklion-catalogue':'institutional_object_metadata','heraklion-exhibit':'institutional_exhibit_assertions','evans1909':'native_graphical_baseline','hmu-codification':'limited_competing_assertions','olivier1975':'bounded_photographic_comparison','pernier1908':'historical_identity_and_context'}
def calculate(root=R):
    load=lambda p:json.loads((root/p).read_text())
    sources=load('sources/sources.json');ids=[s['source_id'] for s in sources]
    if len(set(ids))!=len(ids) or set(ids)!=set(ROLES):raise ValueError('source coverage classification requires explicit review')
    pages=load('sources/olivier1975-page-manifest.json')
    photos=load('reviews/photographic-comparison-v1.json')['groups']
    entries=load('signs/olivier1975-exemplar-crosswalk.json')
    ledger=load('reviews/occurrence-audit-v1.json')
    rows=[]
    for s in sources:
        row={'source_id':s['source_id'],'role':ROLES[s['source_id']],
             'record_license':s['record_license'],'recorded_access_status':s['acquisition_status'],
             'full_source_sha256':s.get('full_source_sha256'),
             'coverage_units':None,'complete_object_autopsy':False,'independent_review_completed':False}
        if s['source_id']=='evans1909':row['coverage_units']={'graphical_groups':61,'project_slots':242}
        elif s['source_id']=='olivier1975':row['coverage_units']={'group_photo_comparisons':len(photos),'labeled_exemplars':len(entries['entries'])+1,'individual_ordinal_pending':ledger['coverage']['ordinal_not_individually_certified']}
        elif s['source_id']=='unicode17':row['coverage_units']={'encoded_base_signs':45,'separate_combining_marks':1}
        rows.append(row)
    return {'format':'source-coverage-v1','source_registry_sha256':hashlib.sha256((root/'sources/sources.json').read_bytes()).hexdigest(),
            'physical_objects':1,'sources':rows,
            'lineage_sha256':hashlib.sha256((root/'apparatus/witness-lineage.json').read_bytes()).hexdigest(),
            'pernier_dates':{'volume_year':1908,'imprint_year':1909,'archive_metadata_year':'1906','archive_date_adopted':False},
            'rights_boundary':'Acquisition and citation do not license redistribution. Only the five authenticated historical Evans renders are packaged; modern source images and PDFs remain excluded.',
            'comparison_boundary':'Source publications are not additional independent objects. Pernier/Evans photographic overlap is unresolved. An encoding, duplicate drawing or dependent edition is not an independent epigraphic witness.'}
if __name__=='__main__':print(json.dumps(calculate(),ensure_ascii=False,indent=2)+'\n',end='')
