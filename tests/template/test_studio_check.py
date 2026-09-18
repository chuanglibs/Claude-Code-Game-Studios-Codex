"""Check the actual hook bridge against a disposable Git repository."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "Git and Bash required")
class StudioCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        hooks = self.root / ".claude/hooks"
        hooks.mkdir(parents=True)
        for name in ("validate-commit.sh", "validate-push.sh"):
            shutil.copyfile(ROOT / ".claude/hooks" / name, hooks / name)

    def check(self, kind):
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/studio_check.py"), kind,
             "--root", str(self.root)], capture_output=True, text=True, timeout=15,
        )

    def test_invalid_staged_json_blocks_without_committing(self):
        data = self.root / "assets/data/enemy.json"
        data.parent.mkdir(parents=True)
        data.write_text('{"health": broken}')
        subprocess.run(["git", "add", "assets/data/enemy.json"], cwd=self.root, check=True)
        result = self.check("commit")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("not valid JSON", result.stderr)
        self.assertNotEqual(subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"], cwd=self.root,
            capture_output=True,
        ).returncode, 0)

    def test_valid_staged_json_passes_without_changing_index(self):
        data = self.root / "assets/data/enemy.json"
        data.parent.mkdir(parents=True)
        data.write_text('{"health": 100}')
        subprocess.run(["git", "add", "assets/data/enemy.json"], cwd=self.root, check=True)
        result = self.check("commit")
        self.assertEqual(result.returncode, 0, result.stderr)
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.root, text=True)
        self.assertIn("A  assets/data/enemy.json", status)

    def test_push_runs_validator_without_pushing(self):
        hook = self.root / ".claude/hooks/validate-push.sh"
        hook.write_text('''#!/bin/bash
input=$(cat)
case "$input" in
  *'"command": "git push"'*) echo 'Validator called'; exit 7 ;;
  *) exit 8 ;;
esac
''')
        result = self.check("push")
        self.assertEqual(result.returncode, 7, result.stderr)
        self.assertIn("Validator called", result.stdout)

    def test_missing_hook_is_a_clear_failure(self):
        (self.root / ".claude/hooks/validate-commit.sh").unlink()
        result = self.check("commit")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Missing hook", result.stderr)


if __name__ == "__main__":
    unittest.main()
