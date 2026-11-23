"""Check exact reviewed skill copies in the portable template."""
import hashlib
import json
from pathlib import Path
import unittest

PACKAGE=Path(__file__).resolve().parents[1]/'templates/celebration-coordinator'

class BundledSkillsTests(unittest.TestCase):
    def test_exact_locked_files(self):
        lock=json.loads((PACKAGE/'bundled-skills.lock.json').read_text())
        actual={p.relative_to(PACKAGE/'workspace').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (PACKAGE/'workspace/skills').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        self.assertEqual(actual,lock['files'])
    def test_six_discoverable_skills(self):
        self.assertEqual(len(list((PACKAGE/'workspace/skills').glob('*/SKILL.md'))),6)
    def test_all_skill_files_explicitly_mapped(self):
        lock=json.loads((PACKAGE/'bundled-skills.lock.json').read_text());manifest=(PACKAGE/'CLAW.md').read_text()
        for path in lock['files']:
            self.assertEqual(manifest.count('source: workspace/'+path+'\n'),1)
            self.assertEqual(manifest.count('path: '+path+'\n'),1)

if __name__=='__main__':unittest.main()
