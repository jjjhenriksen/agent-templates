"""Registry projection contract tests; synthetic refs never published/resolved."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('registry',ROOT/'scripts/celebration_registry_plan.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
PACKAGE=ROOT/'templates/celebration-coordinator'

class RegistryPlanTests(unittest.TestCase):
    def setUp(self):self.pins={name:{'ref':'@test-publisher/'+name,'version':'0.1.0'} for name in m.SKILLS}
    def test_six_exact_registry_dependencies_no_bundled_mappings(self):
        out=m.plan(PACKAGE,self.pins);manifest=out['manifest']
        self.assertEqual(manifest.count('    source: clawhub\n'),6)
        self.assertNotIn('source: workspace/skills/',manifest)
        self.assertEqual(manifest.count('    version: 0.1.0\n'),6)
        self.assertFalse(out['registry_existence_verified'])
    def test_routing_uses_discovery_not_bundled_relative_paths(self):
        routing=m.plan(PACKAGE,self.pins)['replacement_routing']
        self.assertNotIn('../skills/',routing)
        for name in m.SKILLS:self.assertIn(name,routing)
    def test_source_unchanged(self):
        before=(PACKAGE/'CLAW.md').read_bytes();m.plan(PACKAGE,self.pins);self.assertEqual((PACKAGE/'CLAW.md').read_bytes(),before)
    def test_missing_or_extra_skill_rejected(self):
        for kind in ['missing','extra']:
            with self.subTest(kind=kind),self.assertRaises(ValueError):
                pins=deepcopy(self.pins)
                if kind=='missing':pins.pop(m.SKILLS[0])
                else:pins['extra']={'ref':'extra','version':'0.1.0'}
                m.plan(PACKAGE,pins)
    def test_floating_or_injected_version_rejected(self):
        for version in ['latest','^0.1.0','0.1','0.1.0\ncronJobs: []','01.1.0']:
            with self.subTest(version=version),self.assertRaises(ValueError):
                pins=deepcopy(self.pins);pins[m.SKILLS[0]]['version']=version;m.plan(PACKAGE,pins)
    def test_wrong_skill_reference_rejected(self):
        self.pins[m.SKILLS[0]]['ref']='@test-publisher/wrong'
        with self.assertRaises(ValueError):m.plan(PACKAGE,self.pins)
    def test_exact_excluded_file_list(self):
        out=m.plan(PACKAGE,self.pins)
        locked=json.loads((PACKAGE/'bundled-skills.lock.json').read_text())
        self.assertEqual(set(out['excluded_workspace_files']),{'workspace/'+p for p in locked['files']})
    def test_projection_staging_has_no_skill_copies(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp)/'package'
            # Build a new staging copy; preserve review source and do not execute any Add/install.
            shutil.copytree(PACKAGE,dest,ignore=shutil.ignore_patterns('skills','__pycache__'))
            out=m.plan(PACKAGE,self.pins)
            (dest/'CLAW.md').write_text(out['manifest'])
            (dest/'workspace/reference/hosting-skills.md').write_text(out['replacement_routing'])
            self.assertFalse((dest/'workspace/skills').exists())
            self.assertNotIn('workspace/skills/',(dest/'CLAW.md').read_text())

if __name__=='__main__':unittest.main()
