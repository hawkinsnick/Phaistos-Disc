#!/usr/bin/env python3
"""Fetch only declared primary sources; reject changed bytes before use."""
import argparse,hashlib,json,pathlib,subprocess,time,urllib.request
R=pathlib.Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--cache',type=pathlib.Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args();a.cache.mkdir(parents=True,exist_ok=True)
s=next(s for s in json.loads((R/'sources/sources.json').read_text()) if s['source_id']=='evans1909');dest=a.cache/'evans1909.pdf'
if not dest.exists():
    for attempt in range(3):
        try:
            with urllib.request.urlopen(s['download_url'],timeout=45) as response:data=response.read(32*1024*1024+1)
            if len(data)>32*1024*1024:raise ValueError('source exceeds declared maximum')
            dest.write_bytes(data);break
        except Exception:
            if attempt==2:raise
            time.sleep(2)
if hashlib.sha256(dest.read_bytes()).hexdigest()!=s['full_source_sha256'] or dest.stat().st_size!=s['bytes']:raise SystemExit('FAIL: primary source bytes differ; do not overwrite pins automatically')
if a.render:
    images=R/'sources/images';images.mkdir(exist_ok=True)
    for page,name in [(294,'signary'),(298,'figure128'),(300,'figure129'),(347,'plate12'),(351,'plate13')]:
        prefix=a.cache/('render-'+name)
        subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1200','-png',str(dest),str(prefix)],check=True)
        result=next(a.cache.glob('render-'+name+'-*.png'));(images/('evans1909-'+name+'.png')).write_bytes(result.read_bytes())
print(json.dumps({'status':'PASS','source_id':'evans1909','sha256':s['full_source_sha256'],'rendered':a.render}))
