"""Rights/provenance audit regression tests."""
import json,pathlib,subprocess,sys,tempfile,shutil,unittest
R=pathlib.Path(__file__).resolve().parents[1]
class RightsAuditTests(unittest.TestCase):
    def run_audit(self,root):
        script=(root/"scripts/audit_rights_provenance.py")
        return subprocess.run([sys.executable,str(script)],cwd=root,text=True,capture_output=True)
    def copy(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);root=pathlib.Path(t.name)/"repo";shutil.copytree(R,root,ignore=shutil.ignore_patterns(".git","__pycache__","output"));return root
    def test_current_rights_state_passes(self):
        q=self.run_audit(R);self.assertEqual(q.returncode,0,q.stdout+q.stderr)
    def test_noassertion_does_not_require_invented_license(self):
        root=self.copy();sources=json.loads((root/"sources/sources.json").read_text());s=next(x for x in sources if x["source_id"]=="unicode-proposal2006");s["record_license"]="NOASSERTION";s["acquisition_status"]="authenticated_bytes";s["scope"]="Reference only; no redistribution rights asserted."; (root/"sources/sources.json").write_text(json.dumps(sources));q=self.run_audit(root);self.assertEqual(q.returncode,0,q.stdout+q.stderr)
    def test_noassertion_cannot_claim_redistribution(self):
        root=self.copy();sources=json.loads((root/"sources/sources.json").read_text());s=next(x for x in sources if x["source_id"]=="unicode-proposal2006");s["record_license"]="NOASSERTION";s["scope"]="Redistribution permitted."; (root/"sources/sources.json").write_text(json.dumps(sources));q=self.run_audit(root);self.assertNotEqual(q.returncode,0);self.assertIn("unresolved rights conflict",q.stdout)
if __name__=="__main__":unittest.main()
