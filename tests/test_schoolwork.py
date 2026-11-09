import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT / 'templates/schoolwork-copilot/workspace'
spec = importlib.util.spec_from_file_location('schoolwork', WS / 'scripts/plan.py')
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
EX = json.loads((WS / 'examples/example.json').read_text())

class SchoolworkTests(unittest.TestCase):
    def setUp(self): self.r = copy.deepcopy(EX)
    def test_order_and_unknown(self):
        result = S.plan(self.r)
        self.assertEqual(result['deadline_order'], ['task-a'])
        self.assertEqual(result['unknown_deadline_ids'], ['task-b'])
        self.assertFalse(result['submissions_made'])
    def test_offsets_are_instants(self):
        self.r['assignments'][1]['due_at'] = '2030-04-12T18:00:00+02:00'
        self.assertEqual(S.plan(self.r)['deadline_order'], ['task-b', 'task-a'])
    def test_naive_date_rejected(self):
        self.r['assignments'][0]['due_at'] = '2030-04-12T17:00:00'
        with self.assertRaises(ValueError): S.plan(self.r)
    def test_invalid_date_rejected(self):
        self.r['assignments'][0]['due_at'] = 'not-a-date'
        with self.assertRaises(ValueError): S.plan(self.r)
    def test_duplicate_rejected(self):
        self.r['assignments'].append(self.r['assignments'][0])
        with self.assertRaises(ValueError): S.plan(self.r)
    def test_boolean_version_rejected(self):
        self.r['schema_version'] = True
        with self.assertRaises(ValueError): S.plan(self.r)
    def test_unknown_status_rejected(self):
        self.r['assignments'][0]['status'] = 'finished-maybe'
        with self.assertRaises(ValueError): S.plan(self.r)
    def test_private_notes_not_projected(self):
        out = json.dumps(S.plan(self.r))
        self.assertNotIn('DO-NOT-SHARE', out)
        self.assertNotIn('private_notes', out)
    def test_no_mutation(self):
        before = copy.deepcopy(self.r)
        self.assertEqual(S.plan(self.r), S.plan(self.r))
        self.assertEqual(self.r, before)
    def test_cli_read_only(self):
        path = WS / 'examples/example.json'; before = path.read_bytes()
        proc = subprocess.run([sys.executable, str(WS/'scripts/plan.py'), str(path)],capture_output=True,text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), S.plan(self.r))
        self.assertEqual(path.read_bytes(), before)
    def test_cli_error_redacted(self):
        proc = subprocess.run([sys.executable,str(WS/'scripts/plan.py'),'PRIVATE-MISSING'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2)
        self.assertNotIn('PRIVATE-MISSING',proc.stderr)
    def test_empty(self):
        self.r['assignments']=[]
        self.assertEqual(S.plan(self.r)['deadline_order'],[])
    def test_anonymized_assets(self):
        for path in WS.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                text = path.read_text().lower()
                for marker in ('jacqueline', 'henriksen', 'chapman', 'canvas.chapman.edu'):
                    self.assertNotIn(marker,text,str(path))

if __name__ == '__main__': unittest.main()
