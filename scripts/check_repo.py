#!/usr/bin/env python3
"""Public-package hygiene, asset coverage, syntax and local-link checks."""
import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

TRAVEL_PACKAGES = '\n'.join((
    'packages:', '  - kind: skill', '    source: clawhub',
    '    ref: "@steipete/goplaces"', '    version: 1.0.0',
))
TRAVEL_PROFILE = """schemaVersion: 1
agent:
  tools:
    profile: minimal
    alsoAllow:
      - read
      - write
      - edit
      - search_stays
      - search_flights
      - eg_travel_signup
      - eg_travel_verify
      - exec
    fs:
      workspaceOnly: true
extensions:
  - id: expedia-openclaw
    kind: plugin
    format: openclaw
    source: clawhub
    ref: "@expediagroup/expedia-openclaw"
    version: 1.0.4
"""

def check_capabilities(package):
    """Pin reviewed capability surfaces; reject accidental widening."""
    manifest = (package / 'CLAW.md').read_text()
    if package.name == 'meal-planner':
        try:
            current = json.loads(manifest.split('---', 2)[1])
            assert not any(k in current for k in ('packages', 'cronJobs', 'profiles', 'extensions'))
            assert current['skills'] == [] and current['plugins'] == [] and current['automations'] == []
            assert list(current['mcpServers']) == ['instacart']
        except (ValueError, KeyError, AssertionError):
            return ['meal-planner: unexpected current-format requirements']
        return []
    expected = TRAVEL_PACKAGES if package.name == 'travel-copilot' else 'packages: []'
    blocks = re.findall(r'^packages:[^\n]*(?:\n[ \t]+[^\n]*)*', manifest, re.M)
    errors = []
    if blocks != [expected] or not all(manifest.count(x) == 1 for x in ('mcpServers: {}', 'cronJobs: []')) or re.search(r'^automations:', manifest, re.M):
        errors.append(package.name + ': unexpected dependencies/jobs')
    profiles = sorted(p.relative_to(package).as_posix() for p in (package / 'profiles').rglob('*') if p.is_file())
    if package.name == 'travel-copilot':
        if profiles != ['profiles/openclaw.yml'] or (package / 'profiles/openclaw.yml').read_text() != TRAVEL_PROFILE:
            errors.append(package.name + ': unexpected provider profile')
    elif profiles:
        errors.append(package.name + ': unexpected provider profile')
    return errors

def check(root=ROOT):
    errors = []
    for package in sorted((root / 'templates').iterdir()):
        meta = json.loads((package / 'package.json').read_text())
        manifest = (package / 'CLAW.md').read_text()
        if meta.get('scripts') or meta['openclaw'] != {'template': 'CLAW.md'}:
            errors.append(str(package) + ': unsafe metadata')
        sources = re.findall(r'^\s+(?:- )?source: (workspace/\S+)$', manifest, re.M)
        if package.name == 'meal-planner':
            current = json.loads(manifest.split('---', 2)[1])
            sources = [v['source'] for v in current['workspace']['bootstrapFiles'].values()] + [v['source'] for v in current['workspace']['files']]
        actual = {p.relative_to(package).as_posix() for p in (package / 'workspace').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        if set(sources) != actual or len(sources) != len(set(sources)):
            errors.append(package.name + ': asset coverage mismatch')
        errors.extend(check_capabilities(package))
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
