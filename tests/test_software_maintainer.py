"""Exercise checks, not receiving-agent behavior tests."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

FIXTURE = Path(__file__).resolve().parents[1] / 'templates/software-maintainer/workspace/examples/repair-repo'
SOLUTION = '''import re

def parse_count(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]+", value.strip()):
        raise ValueError("expected nonnegative integer text")
    return int(value.strip())
'''

class MaintainerExerciseTests(unittest.TestCase):
    def test_baseline_fails_and_minimal_repair_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / 'repo'
            shutil.copytree(FIXTURE, repo, ignore=shutil.ignore_patterns('__pycache__'))
            before = {p.name: p.read_bytes() for p in repo.iterdir() if p.is_file()}
            cmd = [sys.executable, '-m', 'unittest', 'discover', '-s', '.', '-p', 'test_*.py', '-v']
            broken = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
            self.assertEqual(broken.returncode, 1, broken.stdout + broken.stderr)
            self.assertIn('test_invalid', broken.stderr)
            (repo / 'counts.py').write_text(SOLUTION)
            fixed = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
            self.assertEqual(fixed.returncode, 0, fixed.stdout + fixed.stderr)
            for name, content in before.items():
                if name != 'counts.py':
                    self.assertEqual((repo / name).read_bytes(), content)
