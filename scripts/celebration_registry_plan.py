#!/usr/bin/env python3
"""Print a registry-backed release projection; offline/read-only, never installs or publishes."""
import argparse
import json
from pathlib import Path
import re
import sys

SKILLS=('hosting-run-of-show','menu-prep-planner','potluck-signup-coordinator',
        'gift-season-manager','event-change-control','event-reminder-lifecycle')
SEMVER=re.compile(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z')
REF=re.compile(r'(?:@[a-z0-9][a-z0-9-]*/)?[a-z0-9]+(?:-[a-z0-9]+)*\Z')

def plan(package,pins):
    if not isinstance(pins,dict) or set(pins)!=set(SKILLS):
        raise ValueError('pins must map exactly the six skill names to their actual published ref/version')
    entries=[];seen=set()
    for name in SKILLS:
        pin=pins[name]
        if not isinstance(pin,dict) or set(pin)!={'ref','version'}:
            raise ValueError('each pin requires only ref and version')
        ref,version=pin['ref'],pin['version']
        if not isinstance(ref,str) or not REF.fullmatch(ref) or ref.split('/')[-1]!=name:
            raise ValueError('ref must be the exact skill name, optionally scoped to its actual publisher')
        if not isinstance(version,str) or not SEMVER.fullmatch(version):
            raise ValueError('exact semantic version required; no latest/ranges')
        if ref in seen:raise ValueError('duplicate skill reference')
        seen.add(ref)
        entries.append('  - kind: skill\n    source: clawhub\n    ref: '+json.dumps(ref)+'\n    version: '+version)
    source=(package/'CLAW.md').read_text()
    if source.count('\npackages: []\n')!=1:
        raise ValueError('expected review manifest with no existing package requirements; inspect before merging')
    # Remove only the explicitly paired bundled-skill workspace mappings.
    pattern=r'^    - source: workspace/(skills/[^\n]+)\n      path: \1\n'
    manifest,count=re.subn(pattern,'',source,flags=re.M)
    if not count:raise ValueError('no bundled skill mappings found; inspect existing release state')
    manifest=manifest.replace('\npackages: []\n','\npackages:\n'+'\n'.join(entries)+'\n')
    manifest=manifest.replace('load only the matching bundled skill','load only the matching installed skill')
    # Skill paths are resolved by discovery in registry mode, not relative links into bundled files.
    routing='''# Registry-installed hosting skills

Use skill discovery/read by exact name for the requested workflow:
- hosting-run-of-show: hosting timeline and guest/run sheet
- menu-prep-planner: quantities, shopping and kitchen conflicts
- potluck-signup-coordinator: Google Sheets-first contributions and reconciliation
- gift-season-manager: private gift research and follow-through
- event-change-control: changed event constraints
- event-reminder-lifecycle: finite reminders and retirement

Load the installed skill's own input contract before using its helper; resolve resources from its actual installed location. Don't assume a workspace/skills path or load every skill. Respect host policy and scoped authority. Existing scripts/plan.py still owns the main event record; do not replace it with a skill-specific example. Avoid duplicate event/gift costs.

The template pins exact ClawHub versions. Installation, trust consent and host policy still apply. Theme plugins are independent appearance extras, not behavior selectors.
'''
    excluded=sorted(p.relative_to(package).as_posix() for p in (package/'workspace/skills').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    return {'manifest':manifest,'replacement_routing':routing,'excluded_workspace_files':excluded,
            'registry_existence_verified':False,'note':'Projection only. Verify publisher/version/artifact receipts before release; omit bundled files in a NEW staging package, never delete the review source.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('package',type=Path);p.add_argument('pins',type=Path);a=p.parse_args()
    try:r=plan(a.package,json.loads(a.pins.read_text()))
    except (OSError,ValueError,TypeError,KeyError) as e:
        print('Invalid release input: '+str(e),file=sys.stderr);return 2
    print(json.dumps(r,indent=2));return 0

if __name__=='__main__':sys.exit(main())
