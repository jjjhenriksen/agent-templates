"""Offline capability-contract checks; no provider calls or installs."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'templates/travel-copilot'
spec = importlib.util.spec_from_file_location('check_repo', ROOT / 'scripts/check_repo.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class TravelProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / 'travel-copilot'
        shutil.copytree(PACKAGE, self.package, ignore=shutil.ignore_patterns('__pycache__'))

    def mutate(self, path, old, new):
        f = self.package / path
        self.assertIn(old, f.read_text())
        f.write_text(f.read_text().replace(old, new))
        self.assertTrue(checker.check_capabilities(self.package))

    def test_reviewed_capabilities(self):
        self.assertEqual(checker.check_capabilities(self.package), [])

    def test_skill_version_drift_rejected(self):
        self.mutate('CLAW.md', 'version: 1.0.0', 'version: 9.9.9')

    def test_plugin_version_drift_rejected(self):
        self.mutate('profiles/openclaw.yml', 'version: 1.0.4', 'version: 9.9.9')

    def test_added_tool_rejected(self):
        self.mutate('profiles/openclaw.yml', '      - exec', '      - exec\n      - message')

    def test_removed_workspace_bound_rejected(self):
        self.mutate('profiles/openclaw.yml', 'workspaceOnly: true', 'workspaceOnly: false')

    def test_automatic_job_rejected(self):
        self.mutate('CLAW.md', 'cronJobs: []', 'cronJobs:\n  - name: automatic')

    def test_second_automation_key_rejected(self):
        self.mutate('CLAW.md', 'cronJobs: []', 'cronJobs: []\nautomations: []')

    def test_missing_profile_rejected(self):
        (self.package / 'profiles/openclaw.yml').unlink()
        self.assertTrue(checker.check_capabilities(self.package))

    def test_extra_profile_rejected(self):
        (self.package / 'profiles/other.yml').write_text('unexpected: true\n')
        self.assertTrue(checker.check_capabilities(self.package))

    def test_other_packages_stay_dependency_free(self):
        for name in ('celebration-coordinator', 'good-company-coordinator', 'schoolwork-copilot'):
            self.assertEqual(checker.check_capabilities(ROOT / 'templates' / name), [])

    def test_workspace_mappings_and_license_notice(self):
        manifest = (PACKAGE / 'CLAW.md').read_text()
        for path in ('reference/goplaces.md', 'reference/provider-research.md',
                     'reference/provider-notices.md', 'templates/provider-shortlist.md', 'templates/trip-plan.md'):
            self.assertIn('source: workspace/' + path, manifest)
            self.assertTrue((PACKAGE / 'workspace' / path).is_file())
        notice = (PACKAGE / 'workspace/reference/provider-notices.md').read_text()
        self.assertIn('Copyright (c) 2026 OpenClaw Foundation', notice)
        self.assertIn('Permission is hereby granted', notice)

    def test_safety_and_fallback_instructions(self):
        guide = (PACKAGE / 'workspace/reference/provider-research.md').read_text()
        for phrase in ('fresh confirmation', 'a cached email address is not permission',
                       'not empty inventory', 'No scheduled jobs', 'not a market-wide',
                       'do not', 'not provider payloads', 'not scoped authority'):
            self.assertIn(phrase, guide)
        google = (PACKAGE / 'workspace/reference/goplaces.md').read_text()
        for phrase in ('No unattended Google polling', 'not future availability',
                       'billing and quotas', 'literal argument', 'No automatic retries'):
            self.assertIn(phrase, google)


if __name__ == '__main__':
    unittest.main()
