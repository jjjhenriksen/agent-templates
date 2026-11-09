#!/usr/bin/env python3
"""Public-package hygiene, asset coverage, syntax and local-link checks."""
import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def check(root=ROOT):
    errors = []
    for package in sorted((root / 'templates').iterdir()):
        meta = json.loads((package / 'package.json').read_text())
        manifest = (package / 'CLAW.md').read_text()
        if meta.get('scripts') or meta['openclaw'] != {'template': 'CLAW.md'}:
            errors.append(str(package) + ': unsafe metadata')
        sources = re.findall(r'^\s+(?:- )?source: (\S+)$', manifest, re.M)
        actual = {p.relative_to(package).as_posix() for p in (package / 'workspace').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        if set(sources) != actual or len(sources) != len(set(sources)):
            errors.append(package.name + ': asset coverage mismatch')
        if not all(x in manifest for x in ('packages: []', 'mcpServers: {}', 'cronJobs: []')):
            errors.append(package.name + ': unexpected dependencies/jobs')
        for required in ('BOOTSTRAP.md', 'LICENSE', 'README.md', 'ACCEPTANCE.md', 'SOURCES.md'):
            if not (package / required).is_file():
                errors.append(package.name + ': missing ' + required)
    for p in root.rglob('*'):
        if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts:
            continue
        if p.suffix == '.py':
            ast.parse(p.read_text(), filename=str(p))
        if p.suffix == '.json':
            json.loads(p.read_text())
        text = p.read_text(encoding='utf-8')
        # Synthetic token/private-path patterns, not a substitute for human review.
        private_home = '/' + 'Users/'
        forbidden = [private_home, '/' + 'home/', 'gh' + 'p_', 'gh' + 'o_', 'BEGIN ' + 'PRIVATE KEY', '<@' + '478686']
        if any(marker in text for marker in forbidden):
            errors.append(str(p.relative_to(root)) + ': private path/token marker')
        if p.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if re.match(r'^[a-z]+:', target) or target.startswith('#'):
                    continue
                target = target.split('#', 1)[0]
                if target and not (p.parent / target).exists():
                    errors.append(str(p.relative_to(root)) + ': broken local link ' + target)
    return errors

if __name__ == '__main__':
    errors = check()
    if errors:
        raise SystemExit('\n'.join(errors))
    print('Repository hygiene, local links, Python/JSON syntax and asset coverage passed.')
