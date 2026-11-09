import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

P = Path(__file__).resolve().parents[1] / 'templates/schoolwork-copilot/workspace/scripts/refresh.py'
spec = importlib.util.spec_from_file_location('refresh', P)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = dict(timezone='Europe/London', brief_time='08:30', stale_hours=24, reminders=True, reminder_hours=24,
                           sources=[dict(id='a', authorized=True, path='a.json')])
        self.raw = dict(observed_at='2030-04-11T08:00:00Z', assignments=[dict(id='x', due_at='2030-04-11T17:00:00Z', status='draft')])
        self.save()
    def save(self): (self.root/'a.json').write_text(json.dumps(self.raw))
    def run_refresh(self, state=None, now='2030-04-11T08:30:00Z'):
        return R.refresh(self.config, state or {}, R.instant(now), self.root)
    def test_refresh_daily_reminder_and_dedup(self):
        first=self.run_refresh(); self.assertIsNotNone(first['daily_brief'])
        self.assertEqual(len(first['notifications']),2)
        again=self.run_refresh(first['next_state']); self.assertIsNone(again['daily_brief']); self.assertEqual(again['notifications'],[])
    def test_changed_deadline_and_removed_export(self):
        state=self.run_refresh()['next_state']; self.raw['assignments'][0]['due_at']=None; self.save()
        changed=self.run_refresh(state); self.assertIsNone(changed['notifications'][0]['evidence']['after']['due_at'])
        self.raw['assignments']=[]; self.save()
        self.assertIsNone(self.run_refresh(changed['next_state'])['notifications'][0]['evidence']['after'])
    def test_failure_retains_snapshot_not_fresh(self):
        state=self.run_refresh()['next_state']; (self.root/'a.json').unlink()
        result=self.run_refresh(state, '2030-04-12T08:30:00Z')
        self.assertEqual(result['coverage'][0]['status'],'missing-or-invalid')
        self.assertEqual(result['next_state']['sources'],state['sources'])
        self.assertEqual(result['daily_brief']['priorities'][0]['coverage'],'missing-or-invalid')
    def test_stale_and_future(self):
        self.assertEqual(self.run_refresh(now='2030-04-13T08:30:00Z')['coverage'][0]['status'],'stale')
        self.assertEqual(self.run_refresh(now='2030-04-10T08:30:00Z')['coverage'][0]['status'],'missing-or-invalid')
    def test_unknown_and_completed(self):
        self.raw['assignments'][0]['due_at']=None; self.save()
        self.assertEqual(len(self.run_refresh()['daily_brief']['unknown_deadlines']),1)
        self.raw['assignments'][0]['status']='submitted'; self.save()
        self.assertEqual(self.run_refresh()['daily_brief']['priorities'],[])
    def test_authority_and_path_escape(self):
        self.config['sources'][0]['authorized']=False
        with self.assertRaises(ValueError): self.run_refresh()
        self.config['sources'][0].update(authorized=True,path='../outside.json')
        with self.assertRaises(ValueError): self.run_refresh()
    def test_bad_source_and_no_mutation(self):
        before=json.loads(json.dumps(self.config)); self.raw['assignments']*=2; self.save()
        self.assertEqual(self.run_refresh()['coverage'][0]['status'],'missing-or-invalid')
        self.assertEqual(self.config,before)
    def test_time_gate_and_next_day(self):
        self.assertIsNone(self.run_refresh(now='2030-04-11T06:00:00Z')['daily_brief'])
        state=self.run_refresh()['next_state']
        self.assertIsNotNone(self.run_refresh(state,'2030-04-12T08:30:00Z')['daily_brief'])
    def test_reminders_opt_out(self):
        self.config['reminders']=False
        self.assertEqual(len(self.run_refresh()['notifications']),1)
    def test_dst_repeat_same_local_day(self):
        self.config.update(brief_time='01:00')
        first=self.run_refresh(now='2030-10-27T00:30:00Z')
        self.assertIsNotNone(first['daily_brief'])
        self.assertIsNone(self.run_refresh(first['next_state'],'2030-10-27T01:30:00Z')['daily_brief'])
    def test_regressing_and_naive_export(self):
        state=self.run_refresh()['next_state']
        for observed in ('2030-04-11T07:00:00Z','2030-04-11T08:00:00'):
            self.raw['observed_at']=observed; self.save()
            self.assertEqual(self.run_refresh(state)['coverage'][0]['status'],'missing-or-invalid')
    def test_cli_readonly_and_redacted_error(self):
        import subprocess
        import sys
        path=self.root/'config.json'; path.write_text(json.dumps(self.config))
        before={p.name:p.read_bytes() for p in self.root.iterdir()}
        proc=subprocess.run([sys.executable,str(P),str(path),'--now','2030-04-11T08:30:00Z'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['delivery'],'not-sent')
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})
        proc=subprocess.run([sys.executable,str(P),'SECRET-MISSING','--now','bad'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2); self.assertNotIn('SECRET-MISSING',proc.stderr)
