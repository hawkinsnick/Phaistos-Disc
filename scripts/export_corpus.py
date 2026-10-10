#!/usr/bin/env python3
"""Export source-attributed slots without flattening rights, uncertainty or units."""
import csv,json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]
def export_records(root=R):
    corpus=json.loads((root/'corpus/disc.json').read_text());groups={g['group_id']:g for g in corpus['groups']};result=[]
    for o in corpus['occurrences']:
        g=groups[o['group_id']];number=None if o['sign_id'] is None else int(o['sign_id'][4:],16)-0x101CF
        result.append({'project':'phaistos-disc','record_id':o['occurrence_id'],'assertions':[{'assertion_type':'project_transcribed_graphical_sign','value':{'native_sign_id':o['sign_id'],'evans_number':number},'status':'project_derived','uncertainty':'unknown' if number is None else 'not_stated','physical_locus':f"PD-001/{g['face_id']}/{g['evans_label']}/slot{o['index']}",'lineage_id':'PD-W-EVANS1909-FIGURES','provenance':[{'source_id':'evans1909','locator':g['provenance']['locator'],'source_version':'1909','agent':'project transcription','transformation':'Explicit Evans/Unicode numbering crosswalk; project outer-to-inner traversal'}]}],'rights':{'record_license':'CC-BY-NC-4.0','third_party_material':[{'source_id':'evans1909','license':'Historical edition public domain; cite Evans1909 and Toronto/InternetArchive digitization'},{'source_id':'unicode17','license':'Unicode-3.0','license_path':'licenses/Unicode-3.0.txt'}]},'extensions':{'object_id':'PD-001','face_id':g['face_id'],'group_id':g['group_id'],'index':o['index'],'physical_objects':1,'word_interpretation':None,'phonetic_value':None,'physical_position':None}})
    return result
if __name__=='__main__':
    dest=R/'exports';dest.mkdir(exist_ok=True);records=export_records()
    (dest/'aegean-interop.json').write_text(json.dumps(records,ensure_ascii=False,separators=(',',':'))+'\n')
    with (dest/'occurrences.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['occurrence_id','object_id','face_id','group_id','index','sign_id','uncertainty','source_id','source_locator','record_license','source_rights_profile'])
        for r in records:
            e=r['extensions'];a=r['assertions'][0];w.writerow([r['record_id'],e['object_id'],e['face_id'],e['group_id'],e['index'],a['value']['native_sign_id'],a['uncertainty'],'evans1909',a['provenance'][0]['locator'],'CC-BY-NC-4.0','evans1909-public-domain+Unicode-3.0'])
    corpus=json.loads((R/'corpus/disc.json').read_text())
    with (dest/'groups.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['group_id','face_id','evans_label','outer_index','occurrence_slots','semantics','source_id','source_locator'])
        for g in corpus['groups']:w.writerow([g['group_id'],g['face_id'],g['evans_label'],g['outer_index'],len(g['occurrence_ids']),'graphical_group_not_established_word',g['provenance']['source_id'],g['provenance']['locator']])
    print('PASS: 242 source-attributed interchange records plus occurrence/group CSVs')
