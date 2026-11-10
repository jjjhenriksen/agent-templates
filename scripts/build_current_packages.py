#!/usr/bin/env python3
"""Reproducible archives for current-format templates; offline, no installs or publishing."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import tarfile
R=Path(__file__).resolve().parents[1]
def build(p):
    meta=json.loads((p/'package.json').read_text());m=json.loads((p/'CLAW.md').read_text().split('---',2)[1])
    if set(m)&{'packages','cronJobs','profiles','extensions'}:raise ValueError('retired manifest fields')
    sources=[v['source'] for v in m['workspace']['bootstrapFiles'].values()]+[v['source'] for v in m['workspace']['files']]
    actual={f.relative_to(p).as_posix() for f in (p/'workspace').rglob('*') if f.is_file() and '__pycache__' not in f.parts}
    if set(sources)!=actual or len(sources)!=len(set(sources)):raise ValueError('asset coverage mismatch')
    names=set(sources)|{'package.json','CLAW.md','LICENSE','BOOTSTRAP.md','README.md'}
    names.update(n for n in ['SOURCES.md','ACCEPTANCE.md'] if (p/n).is_file())
    names.update(f.relative_to(p).as_posix() for f in (p/'profiles').glob('*.yml'))
    if (p/'bundled-skills.lock.json').exists():names.add('bundled-skills.lock.json')
    buf=io.BytesIO()
    with tarfile.open(fileobj=buf,mode='w',format=tarfile.USTAR_FORMAT) as t:
        for n in sorted(names):
            f=(p/n).resolve()
            if not f.is_relative_to(p.resolve()) or not f.is_file():raise ValueError('unsafe or missing file')
            data=f.read_bytes();i=tarfile.TarInfo('package/'+n);i.size=len(data);i.mode=0o644;i.mtime=0;t.addfile(i,io.BytesIO(data))
    return meta,gzip.compress(buf.getvalue(),mtime=0)
def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--out',type=Path,required=True);o=a.parse_args().out;o.mkdir(parents=True,exist_ok=True);receipts=[]
    for sub in ['releases/celebration-coordinator','templates/meal-planner']:
        p=R/sub;meta,data=build(p);_,again=build(p)
        if data!=again:raise ValueError('nondeterministic archive')
        name=meta['name'].replace('@','').replace('/','-')+'-'+meta['version']+'.tgz';f=o/name
        with f.open('xb') as h:h.write(data)
        receipts.append({'name':meta['name'],'version':meta['version'],'artifact':name,'sha256':hashlib.sha256(data).hexdigest(),'reproducible':True})
    (o/'build-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n');print(json.dumps(receipts,indent=2))
if __name__=='__main__':main()
