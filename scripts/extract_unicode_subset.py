#!/usr/bin/env python3
"""Reproduce the committed subset from externally acquired Unicode 17 bytes."""
import argparse,hashlib,pathlib
p=argparse.ArgumentParser();p.add_argument('--source',required=True,type=pathlib.Path);p.add_argument('--out',required=True,type=pathlib.Path);a=p.parse_args()
raw=a.source.read_bytes()
if hashlib.sha256(raw).hexdigest()!='2e1efc1dcb59c575eedf5ccae60f95229f706ee6d031835247d843c11d96470c':raise SystemExit('FAIL: source bytes differ from pinned Unicode 17')
subset=b'\n'.join(row for row in raw.splitlines() if 0x101D0<=int(row.split(b';')[0],16)<=0x101FD)+b'\n'
if hashlib.sha256(subset).hexdigest()!='3cbbc1b6112208b4269bb7d01afc67d9cdaeaf1fe31c3a9359b6179194a7afb6':raise SystemExit('FAIL: extracted subset differs')
a.out.write_bytes(subset)
print('PASS: 46 Unicode entries extracted from pinned source bytes')
