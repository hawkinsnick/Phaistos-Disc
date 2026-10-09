#!/usr/bin/env python3
"""Validate JSON contract and CSV round trip, including the unknown slot and rights."""
import csv,json
from jsonschema import Draft202012Validator
from export_corpus import export_records,R
native=json.loads((R/'corpus/disc.json').read_text());export=json.loads((R/'exports/aegean-interop.json').read_text());v=Draft202012Validator(json.loads((R/'schemas/aegean-interop-v0.1.schema.json').read_text()))
assert export==export_records() and len(export)==242
for r in export:v.validate(r)
with (R/'exports/occurrences.csv').open(newline='') as f:rows=list(csv.DictReader(f))
assert [r['occurrence_id'] for r in rows]==[o['occurrence_id'] for o in native['occurrences']]
for row,o in zip(rows,native['occurrences']):
    assert (row['sign_id'] or None)==o['sign_id']
    assert row['record_license']=='CC-BY-NC-4.0' and row['source_rights_profile']=='evans1909-public-domain+Unicode-3.0'
    assert row['source_id']=='evans1909' and row['source_locator']
unknown=next(r for r in export if r['record_id']=='PD-A-E24-S05')
assert unknown['assertions'][0]['value']=={'native_sign_id':None,'evans_number':None}
assert unknown['assertions'][0]['uncertainty']=='unknown'
assert all(r['extensions']['phonetic_value'] is None and r['extensions']['physical_objects']==1 for r in export)
for mutation in ['rights','provenance','extra']:
    r=json.loads(json.dumps(export[0]))
    if mutation=='rights':del r['rights']
    elif mutation=='provenance':r['assertions'][0]['provenance']=[]
    else:r['invented']=True
    assert not v.is_valid(r)
with (R/'exports/groups.csv').open(newline='') as f:groups=list(csv.DictReader(f))
assert len(groups)==61 and sum(int(g['occurrence_slots']) for g in groups)==242
print(json.dumps({'status':'PASS','interop_records':242,'group_records':61,'unknown_round_trip':'PASS','rights_and_provenance':'PASS'}))
