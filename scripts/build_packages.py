#!/usr/bin/env python3
"""Validate, offline-preview, and reproducibly build. Never installs or publishes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if out.exists():
        parser.error('output directory must not exist; preserve old artifacts')
    out.mkdir(parents=True)
    receipts, sums = {}, []
    for template in sorted((ROOT / 'templates').iterdir()):
        meta = json.loads((template / 'package.json').read_text())
        name = template.name + '-' + meta['version']
        result = {}
        for action in ('validate', 'dev'):
            proc = subprocess.run(['openclaw', 'templates', action, str(template), '--json'], capture_output=True, text=True, check=True)
            result[action] = json.loads(proc.stdout)
        if result['dev']['plan'].get('blockers'):
            raise RuntimeError('offline preview has blockers: ' + template.name)
        artifacts = [out / (name + suffix + '.tgz') for suffix in ('', '-repeat')]
        for artifact in artifacts:
            subprocess.run(['openclaw', 'templates', 'build', str(template), '--out', str(artifact), '--json'], capture_output=True, text=True, check=True)
        first, second = [p.read_bytes() for p in artifacts]
        if first != second:
            raise RuntimeError('nondeterministic build: ' + template.name)
        digest = hashlib.sha256(first).hexdigest()
        sums.append(digest + '  ' + artifacts[0].name)
        result.update(sha256=digest, reproducible=True)
        receipts[template.name] = result
        print(template.name + ': validate/dev/build/rebuild passed; ' + digest)
    (out / 'SHA256SUMS').write_text('\n'.join(sums) + '\n')
    (out / 'receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')

if __name__ == '__main__':
    main()
