from pathlib import Path
from copy import deepcopy
import importlib.util
import json
import subprocess
import sys
import unittest
R=Path(__file__).resolve().parents[1]
P=R/'templates/meal-planner'
s=importlib.util.spec_from_file_location('shopping', P/'workspace/scripts/shopping.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class MealTests(unittest.TestCase):
    def setUp(self): self.r=json.loads((P/'workspace/examples/week.json').read_text())
    def test_reserved_pantry_subtracted_once(self):
        rice=next(x for x in m.shopping(self.r)['items'] if x['id']=='rice-dry');self.assertEqual(rice['buy'],'200')
    def test_unknown_is_not_zero(self): self.assertFalse(m.shopping(self.r)['complete'])
    def test_unknown_mixed_group_stays_incomplete(self):
        self.r['ingredients'] += [{'id':'rice-dry','unit':'g','need':None}];a=next(x for x in m.shopping(self.r)['items'] if x['id']=='rice-dry');self.assertIsNone(a['buy']);self.assertEqual(a['buy_lower_bound'],'200')
    def test_units_do_not_convert(self):
        self.r['ingredients'] += [{'id':'rice-dry','unit':'cup','need':'2'}];self.assertEqual(len(m.shopping(self.r)['items']),4)
    def test_no_negative_purchase(self):
        self.r['pantry'][0]['available']='900';self.assertEqual(next(x for x in m.shopping(self.r)['items'] if x['id']=='rice-dry')['buy'],'0')
    def test_decimal_exact(self):
        a={'ingredients':[{'id':'a','unit':'g','need':'0.1'},{'id':'a','unit':'g','need':'0.2'}],'pantry':[]};self.assertEqual(m.shopping(a)['items'][0]['buy'],'0.3')
    def test_bad_quantities(self):
        for v in [True,1,'NaN','Infinity','-1','1e100','0.0000001','']:
            with self.subTest(v=v),self.assertRaises(ValueError):m.amount(v)
    def test_duplicate_pantry_rejected(self):
        self.r['pantry']*=2
        with self.assertRaises(ValueError):m.shopping(self.r)
    def test_over_reserved_rejected(self):
        self.r['pantry'][0]['reserved']='999'
        with self.assertRaises(ValueError):m.shopping(self.r)
    def test_missing_need_rejected(self):
        del self.r['ingredients'][0]['need']
        with self.assertRaises(ValueError):m.shopping(self.r)
    def test_input_unchanged(self):
        before=deepcopy(self.r);m.shopping(self.r);self.assertEqual(before,self.r)
    def test_cli_readonly(self):
        f=P/'workspace/examples/week.json';before=f.read_bytes();p=subprocess.run([sys.executable,str(P/'workspace/scripts/shopping.py'),str(f)],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);json.loads(p.stdout);self.assertEqual(before,f.read_bytes())
    def test_cli_errors_do_not_echo_private_input(self):
        p=subprocess.run([sys.executable,str(P/'workspace/scripts/shopping.py'),'PRIVATE-DO-NOT-ECHO'],capture_output=True,text=True);self.assertEqual(p.returncode,2);self.assertNotIn('PRIVATE-DO-NOT-ECHO',p.stderr)
class CurrentManifestTests(unittest.TestCase):
    def test_current_contract_and_mappings(self):
        for p in [P,R/'releases/celebration-coordinator']:
            text=(p/'CLAW.md').read_text();a=json.loads(text.split('---',2)[1]);self.assertFalse(set(a)&{'packages','cronJobs','profiles','extensions'});self.assertEqual(a['automations'],[])
            declared=[v['source'] for v in a['workspace']['bootstrapFiles'].values()]+[v['source'] for v in a['workspace']['files']]
            actual={f.relative_to(p).as_posix() for f in (p/'workspace').rglob('*') if f.is_file() and '__pycache__' not in f.parts};self.assertEqual(set(declared),actual);self.assertEqual(len(declared),len(set(declared)))
            c=a['mcpServers']['instacart'];self.assertIn('mcp-remote@0.16.5',c['args']);self.assertEqual(c['env'],{'INSTACART_API_KEY':'${INSTACART_API_KEY}'});self.assertEqual(c['toolFilter']['include'],['create-recipe','create-shopping-list'])
            self.assertFalse((p/'profiles').exists())
    def test_themes_only_on_celebration(self):
        a=json.loads((R/'releases/celebration-coordinator/CLAW.md').read_text().split('---',2)[1]);b=json.loads((P/'CLAW.md').read_text().split('---',2)[1]);self.assertEqual(a['plugins'],[{'ref':'openclaw-christmas-themes','version':'0.1.0'}]);self.assertEqual(len(a['skills']),6);self.assertEqual(b['plugins'],[])
if __name__=='__main__': unittest.main()
