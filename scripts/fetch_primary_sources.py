#!/usr/bin/env python3
"""Acquire pinned sources; modern publisher pages stay in the private cache."""
import argparse,concurrent.futures,hashlib,json,pathlib,subprocess,time,urllib.request
R=pathlib.Path(__file__).resolve().parents[1]
def acquire(url,dest,digest,size):
 if not dest.exists():
  for attempt in range(3):
   try:
    request=urllib.request.Request(url,headers={'User-Agent':'Phaistos-Disc-source-verification/1.1'})
    with urllib.request.urlopen(request,timeout=45) as response:data=response.read(32*1024*1024+1)
    if len(data)>32*1024*1024:raise ValueError('source exceeds maximum')
    if len(data)!=size or hashlib.sha256(data).hexdigest()!=digest:raise ValueError('source bytes differ; pins cannot update automatically')
    dest.write_bytes(data);break
   except Exception:
    if attempt==2:raise
    time.sleep(2)
 if dest.stat().st_size!=size or hashlib.sha256(dest.read_bytes()).hexdigest()!=digest:raise ValueError('cached source differs')
 return dest
def run(cache,render=False):
 cache.mkdir(parents=True,exist_ok=True);sources={s['source_id']:s for s in json.loads((R/'sources/sources.json').read_text())}
 evans=sources['evans1909'];dest=acquire(evans['download_url'],cache/'evans1909.pdf',evans['full_source_sha256'],evans['bytes'])
 if 'pernier1908' in sources:
  s=sources['pernier1908'];acquire(s['download_url'],cache/'pernier1908.pdf',s['full_source_sha256'],s['bytes'])
 if 'olivier1975' in sources:
  s=sources['olivier1975'];raw=(R/s['manifest_path']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=s['manifest_sha256']:raise ValueError('publisher page manifest differs')
  pages=json.loads(raw)['pages'];private=cache/'olivier1975';private.mkdir(exist_ok=True)
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
   list(pool.map(lambda e:acquire(e['url'],private/f"p{e['page']:02d}.jpg",e['sha256'],e['bytes']),pages))
 if render:
  images=R/'sources/images';images.mkdir(exist_ok=True)
  for page,name in [(294,'signary'),(298,'figure128'),(300,'figure129'),(347,'plate12'),(351,'plate13')]:
   prefix=cache/('render-'+name)
   subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-scale-to','1200','-png',str(dest),str(prefix)],check=True)
   result=next(cache.glob('render-'+name+'-*.png'));(images/('evans1909-'+name+'.png')).write_bytes(result.read_bytes())
 return {'status':'PASS','primary_pdfs':2 if 'pernier1908' in sources else 1,'publisher_pages_checked':30 if 'olivier1975' in sources else 0,'modern_page_redistribution':False,'rendered':render}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cache',type=pathlib.Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args();print(json.dumps(run(a.cache,a.render)))
