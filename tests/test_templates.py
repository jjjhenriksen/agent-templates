import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SLUGS = ['celebration-coordinator', 'travel-copilot', 'good-company-coordinator']

def load(slug):
    p = ROOT / 'templates' / slug / 'workspace'
    spec = importlib.util.spec_from_file_location(slug, p / 'scripts/plan.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, json.loads((p / 'examples/example.json').read_text())

C, CE = load(SLUGS[0])
T, TE = load(SLUGS[1])
G, GE = load(SLUGS[2])

class CommonTests(unittest.TestCase):
    def test_examples_run(self):
        for slug in SLUGS:
            m, r = load(slug)
            self.assertEqual(m.plan(r)['edition'], 'planning-only')
    def test_projection_excludes_private(self):
        for slug in SLUGS:
            m, r = load(slug)
            out = json.dumps(m.projection(r))
            self.assertNotIn('private_notes', out)
            self.assertNotIn('DO-NOT-SHARE', out)
            self.assertEqual(set(m.projection(r)), set(r['approved_public_fields']))
    def test_no_approval_no_share(self):
        for slug in SLUGS:
            m,r = load(slug); r['approved_public_fields'] = []
            self.assertEqual(m.projection(r), {})
    def test_unknown_public_field_rejected(self):
        for slug in SLUGS:
            m,r = load(slug); r['public_summary']['private_notes'] = 'leak'
            with self.assertRaises(ValueError): m.projection(r)
    def test_nested_public_value_rejected(self):
        r=copy.deepcopy(CE); r['public_summary']['title']={'private':'secret'}
        with self.assertRaises(ValueError): C.projection(r)
    def test_unavailable_approval_rejected(self):
        r=copy.deepcopy(CE);r['approved_public_fields']=['absent']
        with self.assertRaises(ValueError): C.projection(r)
    def test_duplicate_approval_rejected(self):
        r=copy.deepcopy(CE);r['approved_public_fields']=['title','title']
        with self.assertRaises(ValueError): C.projection(r)
    def test_invalid_timezone_rejected(self):
        r=copy.deepcopy(TE);r['timezone']='Not/AZone'
        with self.assertRaises(ValueError): T.plan(r)
    def test_schema_boolean_not_version(self):
        r=copy.deepcopy(TE);r['schema_version']=True
        with self.assertRaises(ValueError): T.plan(r)
    def test_empty_title_rejected(self):
        r=copy.deepcopy(TE);r['title']=''
        with self.assertRaises(ValueError): T.plan(r)
    def test_negative_nan_infinite_money_rejected(self):
        for value in ('-1','NaN','Infinity','1.001',True,2.5):
            with self.assertRaises(ValueError): C.money(value,'value')
    def test_naive_timestamps_rejected(self):
        with self.assertRaises(ValueError): G.instant('2030-01-01T12:00:00')
    def test_reversed_interval_rejected(self):
        with self.assertRaises(ValueError): G.interval({'start':'2030-01-01T12:00:00Z','end':'2030-01-01T11:00:00Z'})
    def test_cli_read_only(self):
        for slug in SLUGS:
            ws=ROOT/'templates'/slug/'workspace'; example=ws/'examples/example.json'
            before=example.read_bytes()
            p=subprocess.run([sys.executable,str(ws/'scripts/plan.py'),str(example)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr);json.loads(p.stdout)
            self.assertEqual(example.read_bytes(),before)
    def test_cli_invalid_input_no_private_echo(self):
        slug=SLUGS[0]
        p=subprocess.run([sys.executable,str(ROOT/'templates'/slug/'workspace/scripts/plan.py'),'PRIVATE-NONEXISTENT-PATH'],capture_output=True,text=True)
        self.assertEqual(p.returncode,2);self.assertNotIn('PRIVATE-NONEXISTENT',p.stderr)
    def test_repo_hygiene(self):
        p=subprocess.run([sys.executable,str(ROOT/'scripts/check_repo.py')],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

class CelebrationTests(unittest.TestCase):
    def setUp(self): self.r=copy.deepcopy(CE)
    def test_no_double_count(self):
        out=C.plan(self.r)
        self.assertEqual(out['known_forecast'],'240.00');self.assertEqual(out['headroom_against_known_costs'],'60.00')
        self.assertEqual(out['unpaid_commitments'],'70.00')
    def test_estimate_ignored_after_commitment(self):
        self.r['costs'][0]['estimate']='999'
        self.assertEqual(C.plan(self.r)['known_forecast'],'240.00')
    def test_unknown_not_zero(self):
        self.r['costs'][1]['estimate']=None
        out=C.plan(self.r);self.assertFalse(out['forecast_complete']);self.assertEqual(out['unknown_cost_ids'],['supplies'])
    def test_overspend(self):
        self.r['budget']='100';self.assertTrue(C.plan(self.r)['over_budget_on_known_costs'])
    def test_decimal_exact(self):
        self.r['costs']=[{'id':'a','currency':'GBP','actual':'0','committed':None,'estimate':'0.10'},{'id':'b','currency':'GBP','actual':'0','committed':None,'estimate':'0.20'}]
        self.assertEqual(C.plan(self.r)['known_forecast'],'0.30')
    def test_duplicate_cost_rejected(self):
        self.r['costs'].append(self.r['costs'][0])
        with self.assertRaises(ValueError):C.plan(self.r)
    def test_currency_mismatch(self):
        self.r['costs'][0]['currency']='USD'
        with self.assertRaises(ValueError):C.plan(self.r)
    def test_paid_without_commitment(self):
        self.r['costs'][0]['committed']=None
        with self.assertRaises(ValueError):C.plan(self.r)
    def test_paid_exceeds_committed(self):
        self.r['costs'][0]['committed']='50'
        with self.assertRaises(ValueError):C.plan(self.r)
    def test_acceptance_not_invented(self):
        self.assertEqual(C.plan(self.r)['unaccepted_task_ids'],['cleanup'])
        self.r['tasks'][0].update(status='completed',accepted=False)
        with self.assertRaises(ValueError):C.plan(self.r)
    def test_dependency_cycle(self):
        self.r['tasks']=[dict(self.r['tasks'][0],id='a',dependencies=['b']),dict(self.r['tasks'][0],id='b',dependencies=['a'])]
        with self.assertRaises(ValueError):C.plan(self.r)
    def test_missing_dependency(self):
        self.r['tasks'][0]['dependencies']=['absent']
        with self.assertRaises(ValueError):C.plan(self.r)

class TravelTests(unittest.TestCase):
    def setUp(self): self.r=copy.deepcopy(TE)
    def test_party_math(self):self.assertEqual(T.plan(self.r)['known_party_cost'],'460.00')
    def test_unknown_cost(self):self.assertFalse(T.plan(self.r)['budget_complete'])
    def test_hard_unknown_blocks(self):self.assertEqual(T.plan(self.r)['readiness'],'blocked')
    def test_verified_requires_evidence(self):
        self.r['constraints'][0]['status']='verified'
        with self.assertRaises(ValueError):T.plan(self.r)
    def test_verified_not_booking_ready(self):
        self.r['constraints'][0].update(status='verified',evidence='fictional reference; human must review')
        self.assertEqual(T.plan(self.r)['readiness'],'human-source-review-required')
    def test_party_quantity_not_multiplied_twice(self):
        self.r['costs'][1]['quantity']=2
        with self.assertRaises(ValueError):T.plan(self.r)
    def test_bool_quantity_rejected(self):
        self.r['costs'][0]['quantity']=True
        with self.assertRaises(ValueError):T.plan(self.r)
    def test_mixed_currency_rejected(self):
        self.r['costs'][0]['currency']='USD'
        with self.assertRaises(ValueError):T.plan(self.r)
    def test_no_monitor_or_booking(self):
        out=T.plan(self.r);self.assertFalse(out['bookings_made']);self.assertFalse(out['live_monitoring_enabled'])

class GoodCompanyTests(unittest.TestCase):
    def setUp(self):self.r=copy.deepcopy(GE)
    def chosen(self):return G.plan(self.r)['proposals'][0]['suggested_person_id']
    def test_qualified_proposal_not_assignment(self):
        self.assertEqual(self.chosen(),'p1');self.assertFalse(G.plan(self.r)['assignments_accepted'])
    def test_optout(self):self.r['people'][0]['opt_in']=False;self.assertIsNone(self.chosen())
    def test_missing_role(self):self.r['people'][0]['roles']=[];self.assertIsNone(self.chosen())
    def test_unknown_skill(self):self.r['people'][0]['skills']={};self.assertIsNone(self.chosen())
    def test_unavailable(self):self.r['people'][0]['availability']=[];self.assertIsNone(self.chosen())
    def test_full_workload(self):self.r['people'][0]['open_tasks']=2;self.assertIsNone(self.chosen())
    def test_avoid_category(self):self.r['people'][0]['avoid_categories']=['welcome'];self.assertIsNone(self.chosen())
    def test_overlap_proposals(self):
        self.r['tasks'].append(dict(self.r['tasks'][0],id='second'))
        self.assertIsNone(G.plan(self.r)['proposals'][1]['suggested_person_id'])
    def test_existing_busy(self):
        self.r['people'][0]['busy']=[{'start':'2030-06-10T09:30:00+01:00','end':'2030-06-10T10:30:00+01:00'}]
        self.assertIsNone(self.chosen())
    def test_equal_instants_different_offsets(self):
        self.r['tasks'][0].update(start='2030-06-10T09:00:00Z',end='2030-06-10T10:00:00Z')
        self.assertEqual(self.chosen(),'p1')
    def test_repeated_reports_no_mutation(self):
        before=copy.deepcopy(self.r);self.assertEqual(G.plan(self.r),G.plan(self.r));self.assertEqual(self.r,before)
    def test_duplicate_people(self):
        self.r['people'].append(self.r['people'][0])
        with self.assertRaises(ValueError):G.plan(self.r)
    def test_invalid_level(self):
        self.r['people'][0]['skills']['welcome']=4
        with self.assertRaises(ValueError):G.plan(self.r)
    def test_no_acceptance_sneaked_in(self):
        self.r['tasks'][0]['status']='accepted'
        with self.assertRaises(ValueError):G.plan(self.r)

if __name__=='__main__':unittest.main()
