# Codex Template Implementation Plan

**Goal:** Make the existing studio template directly usable in Claude Code and Codex.

**Architecture:** Keep one shared workflow source and generate Codex entry points.
Put client translation in `docs/codex/runtime.md`; document capability differences.

**Tech Stack:** Markdown, TOML, Python 3.9+ standard library, existing Bash hooks.

**Spec:** `docs/superpowers/specs/2026-09-18-codex-template-design.md`

## Constraints

Preserve Claude integration and upstream attribution. No global installation,
hardcoded models, external Python packages, or game engine selection. Do not
commit or push without instruction. Execute in the current workspace.

## Tasks

- [x] Add integration tests in `tests/template/test_codex_adapter.py` for the
  generator CLI: output discovery, read-only drift checks, regeneration, invalid
  metadata, stale generated files, and preservation of custom files.
- [x] Implement `scripts/sync_codex.py`. Read source metadata, generate 73 skill
  wrappers and 49 native role files, and generate scoped instructions. Support
  `python3 scripts/sync_codex.py --check` without writing any file.
- [x] Add root `AGENTS.md` and `docs/codex/runtime.md` for source loading, argument
  and tool translation, role fallback, engine setup, authorization, and rule routing.
- [x] Add and test `scripts/studio_check.py` to invoke existing commit/push
  validators explicitly, preserve their exit status, and report missing Bash.
- [x] Update README, add Chinese quick start, and update contributing/upgrading
  guidance with regeneration, client differences, and manual smoke prompts.
- [x] Add `.github/workflows/template-check.yml`, run all template tests and
  generation checks, verify local Codex discovery, and inspect the final diff.

## Completion evidence

- 16 integration tests pass on Python 3.9.6.
- The generated adapter check passes: 73 skills, 49 roles, 15 scoped instructions.
- Codex CLI 0.142.5 `skills/list` discovers all 73 skills without repository errors;
  `config/read` succeeds. All 49 role TOML files parse successfully.
- Local Markdown links resolve; `git diff --check` passes.
- A disposable `core.autocrlf=true` checkout preserves LF for Bash hooks.
- Instruction files are excluded from game-content checks, covered by regressions.
- No game engine/build or live model workflow was run; hosted CI awaits a push.
- All changes remain uncommitted in the working tree.

## Verification commands

```bash
python3 -m unittest discover -s tests/template -v
python3 scripts/sync_codex.py --check
python3 scripts/studio_check.py commit
python3 scripts/studio_check.py push
git diff --check
```
