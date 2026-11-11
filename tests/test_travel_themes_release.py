import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
class TravelThemesRelease(unittest.TestCase):
    def test_pinned_theme_and_existing_providers(self):
        root=ROOT/'releases/travel-copilot'
        manifest=(root/'CLAW.md').read_text()
        for requirement in ['ref: "openclaw-travel-themes"\n    version: 0.1.0','ref: "@expediagroup/expedia-openclaw"\n    version: 1.0.4','ref: "@steipete/goplaces"\n    version: 1.0.0']:
            self.assertIn(requirement,manifest)
        self.assertIn('profile: minimal',manifest)
        self.assertIn('workspaceOnly: true',manifest)
        self.assertIn('automations: []',manifest)
        self.assertEqual(json.loads((root/'package.json').read_text())['version'],'0.2.5')
        readme=(root/'README.md').read_text()
        self.assertIn('does not change your selected theme',readme)
        self.assertIn('Existing agents are not automatically upgraded',readme)
