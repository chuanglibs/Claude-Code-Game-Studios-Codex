# Codex guide

This fork supports Codex and Claude Code from the same repository. The checked-in
Codex adapter exposes all **73 workflows**, **49 role briefs**, and **11 path rules**.
Claude Code does not need to be installed to use any shared document.

## Start a project

1. Use this GitHub repository as a template, or clone it:

   ```bash
   git clone https://github.com/chuanglibs/Claude-Code-Game-Studios-Codex.git my-game
   cd my-game
   ```

2. Open the folder in Codex desktop/IDE, or run `codex` in the project root.
   Use a current Codex version with repository skills support. Review the folder
   and grant project trust when prompted; this template does not change global
   configuration or permissions.

3. Enter **`$studio-start`**. It asks about your starting point and guides you
   through concept, engine, prototype, and production workflows. For navigation,
   use **`$studio-help`**.

No install script or symlink setup is needed. Python is only required to regenerate
or check the adapter and run the optional hook bridge. Use Python **3.9+**; no pip
packages are needed. On Windows, `py -3` may replace `python3`.

Example prompts (enter these in Codex, not your shell):

```text
$studio-brainstorm cozy exploration game
$studio-setup-engine godot 4.6
$studio-design-system player movement
$studio-team-combat melee parry system --review lean
$studio-skill-test static start
```

The engine version above is an invocation example, not a recommendation. Choose
and verify the version needed by your game. The template does not choose an engine.
You can also ask in natural language, for example “Use the studio onboarding
workflow to help me plan a small game.”

## What differs between clients

| Feature | Claude Code | Codex |
| --- | --- | --- |
| Root instructions | `CLAUDE.md` with `@` imports | `AGENTS.md` with explicit reads |
| Workflow entry | `/start`, `/team-combat` | `$studio-start`, `$studio-team-combat` |
| Skill location | `.claude/skills/` | Generated `.agents/skills/studio-*/` wrappers |
| Roles | `.claude/agents/*.md` | Generated `.codex/agents/studio-*.toml` plus shared briefs |
| Models | Source Claude tier configuration | Inherits your Codex model and effort settings |
| Directory guidance | `.claude/rules/` and nested `CLAUDE.md` | Nested `AGENTS.md` links to the same sources |
| Hook automation | 12 hooks in `.claude/settings.json` | Not registered by this adapter; explicit checks below |
| Permissions | Claude settings | Your current Codex sandbox and approval settings |
| Session state | Claude lifecycle hooks | Explicit project state reads and handoff notes |

Standalone custom role support depends on the Codex client/version. If native
roles aren't exposed by its tools, the workflow passes the shared role brief to
an available subagent. If delegation is unavailable, it uses labeled sequential
role passes and reports the lack of independent review. A fresh clone does not
start 49 agents. Only the roles needed by a requested workflow are used.

The shared workflow and role bodies still use Claude terms. The
[runtime guide](runtime.md) translates tool names, arguments, role routing, and
user decision checkpoints. **`studio-` avoids collisions** with personal skills
such as `code-review`, `prototype`, and Codex's own `/help`.

## Checks

From the repository root:

```bash
python3 scripts/sync_codex.py --check
python3 -m unittest discover -s tests/template -v
```

Run existing validators explicitly when needed:

```bash
python3 scripts/studio_check.py commit
python3 scripts/studio_check.py push
```

These commands require Git and Bash and **never commit or push**. The commit
validator uses staged paths but reads current working files; avoid interpreting
it as validation of a partially staged snapshot. It blocks malformed JSON and
warns on some design/code issues. The push validator only warns about protected
branches. Neither replaces engine builds, game tests, or review.

Claude's notifications, session hooks, compaction hooks, asset hooks, and deny
rules do not automatically run in Codex. Codex hooks need their own event/schema
integration; this version uses explicit checks rather than configuring them.

## Customize and update

1. Edit `.claude/skills`, `.claude/agents`, `.claude/rules`, or shared docs.
2. Run `python3 scripts/sync_codex.py` to refresh checked-in entry points.
3. Run the checks above and review the diff.

The generator changes only marked generated files recorded in
`generated-files.json`. It refuses unmanaged destination collisions and output
symlinks; it preserves unrelated custom files. Removed source entries are removed
from the generated manifest and adapter. Its supported metadata is deliberately
small: one-line `name`, `description`, optional `agent`, and quoted `directory/**`
rule paths. Unsupported upstream syntax fails clearly rather than being guessed.
Extend the parser and tests if upstream adopts more complex metadata.

Keep personal skills and roles under distinct names. For per-project engine and
platform settings, edit `.claude/docs/technical-preferences.md` or use
`$studio-setup-engine`. Both clients read that shared source. Don't remove `.claude/`
even if you only use Codex. Root `AGENTS.md` is maintained by hand; nested generated
instruction files should be changed through their linked sources.

## Manual smoke checks

Structural tests cannot prove live model behavior. After a Codex upgrade or a
workflow change, check these scenarios in a disposable copy:

1. `$studio-start`: asks where you are; does not invent an engine or game concept.
2. `$studio-help`: lists studio commands with `$studio-` names and includes workflows
   found in the source even when the shared catalog is incomplete.
3. `$studio-team-combat` with no feature: returns usage without delegating or writing.
4. Ask for a technical-director review: the native role or fallback reads the
   correct brief and reports whether review was independent.
5. From `src/gameplay/`, ask for applicable rules: Codex reads root, source, and
   gameplay instructions and identifies data-driven tuning requirements.
6. In Claude Code, `/start` and `/help` retain their existing workflow paths.

## Official references

Adapter format checked against official documentation on 2026-09-18:

- [Codex project instructions](https://developers.openai.com/codex/guides/agents-md)
- [Repository skills and invocation](https://developers.openai.com/codex/skills)
- [Custom agents and delegation](https://developers.openai.com/codex/subagents)

The local CLI available while developing this adapter is **0.142.5**. This is
not a claimed minimum version; capability differences use the fallbacks above.

Local validation on 2026-09-18: the CLI app server's `skills/list` discovered all
73 studio skills without repository skill errors; `config/read` succeeded. All
49 generated role files passed TOML parsing. This does not establish native role
spawning or live workflow behavior; those remain the manual smoke checks above.
