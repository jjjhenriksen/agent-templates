"""Static service packaging regression, not a model behavior test."""
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
class ServiceAssets(unittest.TestCase):
    def test_services_are_mapped_and_reachable(self):
        p = ROOT / 'templates/celebration-coordinator'
        text = (p/'workspace/reference/event-studio.md').read_text()
        self.assertIn('Fictional worked', text)
        self.assertIn('not executed model tests', text)
        self.assertIn('reference/event-studio.md', (p/'workspace/AGENTS.md').read_text())
        sources = re.findall(r'^    - source: (workspace/\S+)$', (p/'CLAW.md').read_text(), re.M)
        self.assertIn('workspace/reference/event-studio.md', sources)
        for source in sources:
            self.assertTrue((p/source).is_file(), source)
