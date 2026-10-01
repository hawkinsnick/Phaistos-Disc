"""Exercise actual Git history, byte changes, JSON types and dangerous-looking paths."""
import json, pathlib, subprocess, tempfile, unittest
from release_change_ledger import calculate, semantic, commit, markdown, parse_json
class LedgerTests(unittest.TestCase):
    def test_history(self):
        with tempfile.TemporaryDirectory() as d:
            r=pathlib.Path(d)
            def g(*args): return subprocess.check_output(['git','-C',d,*args],stderr=subprocess.DEVNULL).decode().strip()
            g('init');g('config','user.email','fixture@example.invalid');g('config','user.name','Synthetic fixture')
            (r/'corpus').mkdir();(r/'corpus/a.json').write_text('{"reading":"07","a/b~c":false,"list":[1,2]}')
            (r/'gone').write_bytes(b'old');g('add','.');g('commit','-m','baseline');base=g('rev-parse','HEAD')
            (r/'corpus/a.json').write_text('{"reading":"25","a/b~c":0,"list":[2,1]}')
            (r/'gone').unlink();(r/'binary').write_bytes(b'\x00\xff');(r/'x|y').write_text('added')
            g('add','.');g('commit','-m','target');target=g('rev-parse','HEAD')
            v=calculate(r,base,target);self.assertEqual(v['changed_files'],4)
            changes={x['path']:x for x in v['changes']};self.assertEqual(changes['gone']['operation'],'remove')
            self.assertEqual(changes['binary']['operation'],'add')
            pointers={x['pointer']:x for x in changes['corpus/a.json']['json_changes']}
            self.assertEqual(pointers['/reading']['after'],'25');self.assertEqual(pointers['/a~1b~0c']['operation'],'replace')
            self.assertEqual(pointers['/list']['operation'],'replace_array')
            self.assertIn('x&#124;y',markdown(v));self.assertEqual(calculate(r,base,base)['changed_files'],0)
            # Working-tree corruption must not affect an immutable comparison.
            (r/'corpus/a.json').write_text('uncommitted corruption');self.assertEqual(calculate(r,base,target),v)
            with self.assertRaises(ValueError):commit(r,'--help')
    def test_array_types_and_invalid_json(self):
        self.assertEqual(len(semantic([{'x':False}], [{'x':0}])),1)
        self.assertEqual(semantic([{'a':1,'b':2}], [{'b':2,'a':1}]),[])
        for raw in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}']:
            with self.assertRaises(ValueError):parse_json(raw)
    def test_add_null_and_type(self):
        self.assertEqual(semantic({}, {'x':None}),[{'pointer':'/x','operation':'add','after':None}])
        self.assertEqual(len(semantic(True,1)),1)
        self.assertEqual(semantic({'x':1,'y':2},{'y':2,'x':1}),[])
if __name__=='__main__':unittest.main()
