import copy
import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1] / 'templates/event-operations/workspace/scripts/readiness.py'
spec = importlib.util.spec_from_file_location('readiness', P)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class EventOperationsTests(unittest.TestCase):
    def setUp(self):
        self.cue = dict(id='setup', start='08:00', end='09:00', owner='Mira', accepted=True, ready=True, requires=[])
    def check(self, *cues):
        return module.check({'cues': list(cues)})
    def test_ready(self):
        self.assertEqual(self.check(self.cue), [])
    def test_acceptance_not_inferred(self):
        self.cue['accepted'] = False
        self.assertIn('setup: no accepted owner', self.check(self.cue))
    def test_missing_dependency(self):
        self.cue['requires'] = ['absent']
        self.assertIn('setup: missing dependency absent', self.check(self.cue))
    def test_cycle(self):
        self.cue['requires'] = ['setup']
        with self.assertRaises(ValueError): self.check(self.cue)
    def test_duplicate(self):
        with self.assertRaises(ValueError): self.check(self.cue, copy.deepcopy(self.cue))
    def test_invalid_times(self):
        for value in ['25:00', '8:00', 'today', None]:
            self.cue['start'] = value
            with self.assertRaises(ValueError): self.check(self.cue)
    def test_overnight_rejected(self):
        self.cue.update(start='23:00', end='01:00')
        with self.assertRaises(ValueError): self.check(self.cue)
    def test_late_unready_prerequisite(self):
        other = dict(self.cue, id='doors', start='08:45', end='09:30', requires=['setup'])
        self.cue['ready'] = False
        warnings = self.check(self.cue, other)
        self.assertIn('doors: prerequisite finishes too late: setup', warnings)
        self.assertIn('doors: prerequisite not ready: setup', warnings)
    def test_string_boolean_rejected(self):
        self.cue['accepted'] = 'false'
        with self.assertRaises(ValueError): self.check(self.cue)
