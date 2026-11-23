"""Static service packaging regression, not a model behavior test."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
class ServiceAssets(unittest.TestCase):
    def test_services_are_mapped_and_reachable(self):
        p = ROOT / 'templates/good-company-coordinator'
        text = (p/'workspace/reference/coordination-desk.md').read_text()
        self.assertIn('Fictional worked', text)
        self.assertIn('not executed model tests', text)
        self.assertIn('reference/coordination-desk.md', (p/'workspace/AGENTS.md').read_text())
        sources = re.findall(r'^    - source: (workspace/\S+)$', (p/'CLAW.md').read_text(), re.M)
        self.assertIn('workspace/reference/coordination-desk.md', sources)
        for source in sources:
            self.assertTrue((p/source).is_file(), source)
