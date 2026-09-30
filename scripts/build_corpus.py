#!/usr/bin/env python3
"""Deterministic project transcription from the checked public-domain group ledger."""
import csv,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def build(root=R):
    rows=list(csv.DictReader((root/'data/evans1909-groups.csv').open(newline='',encoding='utf-8')))
    groups=[];occurrences=[]
    for row in rows:
        face=row['face'];number=int(row['evans_group']);gid=f'PD-{face}-E{number:02d}';ids=[]
        for pos,token in enumerate(row['sign_numbers'].split(),1):
            oid=f'{gid}-S{pos:02d}';ids.append(oid)
            occurrences.append({'occurrence_id':oid,'group_id':gid,'index':pos,'sign_id':None if token=='?' else f'PD-U{0x101CF+int(token):X}','uncertainty':'unknown' if token=='?' else 'source_legible','position':None,'phonetic_value':None})
        groups.append({'group_id':gid,'face_id':f'PD-001-{face}','evans_label':f'{face}{number}','outer_index':int(row['outer_index']),'witness_id':'PD-W-EVANS1909-FIGURES','occurrence_ids':ids,'interpretation_as_word':None,'separator_status':'source_graphical_group','provenance':{'source_id':'evans1909','locator':f"p{280 if face=='A' else 282}, Figure{128 if face=='A' else 129}, native group {face}{number}",'verification_status':'project_source_checked'}})
    return {'schema_version':'1.0.0','object_id':'PD-001','physical_objects':1,'faces':[{'face_id':f'PD-001-{f}','label':f,'independent_document':False,'reading_direction':None,'starting_point':None} for f in 'AB'],'witnesses':[{'witness_id':'PD-W-EVANS1909-FIGURES','source_id':'evans1909','source_lineage':'Evans tracing based on earlier photographs; see p281. Not independent of the photographed object or of Pernier publication.','verification_status':'project_source_checked','external_peer_review_completed':False,'project_traversal':'outer_to_inner','source_numbering':'center_to_outer'}],'groups':groups,'occurrences':occurrences,'rights':{'record_license':'MIT','third_party_material':[{'source_id':'evans1909','rights':'Historical edition public domain; faithful source images retain attribution.'},{'source_id':'unicode17','rights':'Unicode-3.0'}]},'claim_boundary':'Project transcription of a published graphical witness, not a certified reading of the object or a decipherment.'}
def write(root=R):
    (root/'corpus/disc.json').write_text(json.dumps(build(root),ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
if __name__=='__main__':write()
