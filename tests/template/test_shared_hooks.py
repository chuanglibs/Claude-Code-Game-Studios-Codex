"""Instruction files must not become game content when both clients coexist."""

from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which("git") and shutil.which("bash"), "Git and Bash required")
class SharedHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def write(self, path, text="Instructions\n"):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def run_hook(self, name, payload=None):
        return subprocess.run(
            ["bash", str(ROOT / ".claude/hooks" / name)], cwd=self.root,
            input=json.dumps(payload or {}), text=True, capture_output=True, timeout=15,
        )

    def test_commit_ignores_instruction_documents_as_gdds(self):
        self.write("design/gdd/AGENTS.md")
        subprocess.run(["git", "add", "design/gdd/AGENTS.md"], cwd=self.root, check=True)
        result = self.run_hook("validate-commit.sh", {"tool_input": {"command": "git commit"}})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("missing required section", result.stderr)

    def test_gap_detection_counts_only_game_documents_and_real_core_code(self):
        for index in range(51):
            self.write(f"src/sample_{index}.gd", "extends Node\n")
        self.write("src/core/AGENTS.md")
        self.write("design/gdd/AGENTS.md")
        self.write("design/gdd/CLAUDE.md")
        self.write("design/gdd/movement.md", "# Movement\n")
        result = self.run_hook("detect-gaps.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sparse design docs (1 files)", result.stdout)
        self.assertNotIn("Core engine/systems exist", result.stdout)

    def test_asset_hook_ignores_instruction_filename_conventions(self):
        self.write("assets/data/AGENTS.md")
        result = self.run_hook("validate-assets.sh", {
            "tool_input": {"file_path": "assets/data/AGENTS.md"},
        })
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("NAMING", result.stderr)

    def test_compaction_does_not_report_instruction_todos_as_game_design(self):
        self.write("design/gdd/AGENTS.md", "TODO: maintain instructions\n")
        result = self.run_hook("pre-compact.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no WIP markers found in design docs", result.stdout)


if __name__ == "__main__":
    unittest.main()
