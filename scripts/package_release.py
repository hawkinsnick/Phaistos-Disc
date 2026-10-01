#!/usr/bin/env python3
"""Package tracked release files and authenticated public-domain source renders."""
import argparse,pathlib,subprocess,zipfile
R=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=pathlib.Path);a=p.parse_args()
version=(R/'VERSION').read_text().strip();prefix=f'Phaistos-Disc-{version}/'
paths=subprocess.check_output(['git','-C',str(R),'ls-files','-z']).decode().split('\0')
with zipfile.ZipFile(a.out,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in paths:
        if rel:z.write(R/rel,prefix+rel)
    for name in ['signary','figure128','figure129','plate12','plate13']:
        image=R/'sources/images'/('evans1909-'+name+'.png')
        if not image.is_file():raise ValueError('missing authenticated public-domain release image: '+name)
        z.write(image,prefix+str(image.relative_to(R)))
print(a.out)
