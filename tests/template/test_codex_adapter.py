"""Exercise the adapter as a maintainer would: generate, edit, check, regenerate."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/sync_codex.py"


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write(".claude/skills/start/SKILL.md", '''---
name: start
description: "Guide a new game project."
model: sonnet
agent: game-designer
---
Ask about the game.
''')
        self.write(".claude/agents/game-designer.md", '''---
name: game-designer
description: "Design the game's mechanics."
model: opus
---
Own the game design.
''')
        self.write(".claude/rules/gameplay-code.md", '''---
paths:
  - "src/gameplay/**"
---
Use data-driven tuning.
''')
        self.write("src/CLAUDE.md", "# Source\nDocument public APIs.\n")
        self.write("docs/codex/runtime.md", "# Runtime\nUse available tools.\n")

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def run_sync(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            capture_output=True, text=True, timeout=15,
        )

    def test_generation_produces_discoverable_entries_and_valid_references(self):
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        skill = self.root / ".agents/skills/studio-start/SKILL.md"
        body = skill.read_text(encoding="utf-8")
        header = body.split("---", 2)[1]
        fields = dict(line.split(": ", 1) for line in header.strip().splitlines())
        self.assertEqual(fields["name"], "studio-start")
        self.assertIn("Guide a new game project.", json.loads(fields["description"]))
        self.assertNotIn("model", fields)
        import re
        links = re.findall(r"\]\(([^)]+)\)", body)
        self.assertGreaterEqual(len(links), 2)
        for link in links:
            self.assertTrue((skill.parent / link).resolve().is_file(), link)
        role = self.root / ".codex/agents/studio-game-designer.toml"
        # The generator emits JSON-compatible TOML strings. Decode values here;
        # the actual Codex parser is also checked separately in a local smoke test.
        fields = dict(line.split(" = ", 1) for line in role.read_text().splitlines()
                      if " = " in line)
        self.assertEqual(json.loads(fields["name"]), "studio-game-designer")
        self.assertIn(".claude/agents/game-designer.md",
                      json.loads(fields["developer_instructions"]))
        self.assertNotIn("model", fields)
        self.assertTrue((self.root / "src/AGENTS.md").is_file())
        self.assertTrue((self.root / "src/gameplay/AGENTS.md").is_file())

    def test_check_detects_missing_and_changed_outputs_without_writing(self):
        self.assertNotEqual(self.run_sync("--check").returncode, 0)
        self.assertFalse((self.root / ".agents").exists())
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(self.run_sync("--check").returncode, 0)
        skill = self.root / ".agents/skills/studio-start/SKILL.md"
        skill.write_text(skill.read_text() + "\nA local edit.\n")
        before = skill.read_bytes()
        self.assertNotEqual(self.run_sync("--check").returncode, 0)
        self.assertEqual(skill.read_bytes(), before)
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(self.run_sync("--check").returncode, 0)

    def test_refresh_tracks_source_changes_and_keeps_custom_files(self):
        self.assertEqual(self.run_sync().returncode, 0)
        custom = self.write(".agents/skills/my-skill/SKILL.md", "User-owned content")
        source = self.root / ".claude/skills/start/SKILL.md"
        source.write_text(source.read_text().replace("new game", "existing game"))
        self.assertNotEqual(self.run_sync("--check").returncode, 0)
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(custom.read_text(), "User-owned content")
        self.assertIn("existing game", (self.root / ".agents/skills/studio-start/SKILL.md").read_text())

    def test_removed_source_removes_only_obsolete_generated_entry(self):
        self.assertEqual(self.run_sync().returncode, 0)
        self.write(".claude/skills/help/SKILL.md", "---\nname: help\ndescription: Help\n---\nHelp.\n")
        (self.root / ".claude/skills/start/SKILL.md").unlink()
        custom = self.write(".agents/skills/custom/SKILL.md", "My skill")
        self.assertNotEqual(self.run_sync("--check").returncode, 0)
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertFalse((self.root / ".agents/skills/studio-start/SKILL.md").exists())
        self.assertTrue(custom.exists())
        self.assertTrue((self.root / ".agents/skills/studio-help/SKILL.md").exists())

    def test_unmanaged_destination_is_not_overwritten(self):
        custom = self.write(".agents/skills/studio-start/SKILL.md", "My existing skill")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(custom.read_text(), "My existing skill")
        self.assertIn("unmanaged", result.stderr.lower())

    def test_missing_description_and_unsafe_names_fail_before_writes(self):
        for metadata in ["name: start", "name: ../../escape\ndescription: Bad",
                         "name: start\ndescription:\nmodel: sonnet"]:
            with self.subTest(metadata=metadata):
                self.write(".claude/skills/start/SKILL.md", f"---\n{metadata}\n---\nBody.\n")
                self.assertNotEqual(self.run_sync().returncode, 0)
                self.assertFalse((self.root / ".agents").exists())

    def test_manifest_cannot_target_paths_outside_repository(self):
        self.assertEqual(self.run_sync().returncode, 0)
        manifest = self.root / "docs/codex/generated-files.json"
        original = json.loads(manifest.read_text())
        for path in ["../outside.md", "/tmp/outside.md", "C:/outside.md"]:
            with self.subTest(path=path):
                manifest.write_text(json.dumps(dict(original, files=[path])))
                result = self.run_sync()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Unsafe", result.stderr)

    def test_symlinked_output_is_rejected(self):
        external = self.root / "external"
        external.mkdir()
        try:
            (self.root / ".agents").symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest("Symlinks unavailable on this host")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(external.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
