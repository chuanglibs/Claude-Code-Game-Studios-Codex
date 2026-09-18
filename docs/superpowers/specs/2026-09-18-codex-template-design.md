# Claude Code and Codex template compatibility

## Goal

A fresh clone works in either Claude Code or Codex without installing the other
client or copying files into a user's home directory. Retain upstream attribution,
game workflows, engine references, templates, and Claude integration.

## Architecture

Keep `.claude/skills`, `.claude/agents`, `.claude/rules`, and `.claude/docs` as
the shared source. Add a small Codex runtime guide that translates client-specific
instructions. Generate thin, checked-in `.agents/skills/studio-*/SKILL.md` entry
points and `.codex/agents/studio-*.toml` role configurations from source metadata.
Use `studio-` names to avoid collisions with personal skills and built-in commands.
No duplicate workflow bodies, symlinks, external Python packages, model pins, or
global configuration changes are necessary.

The root `AGENTS.md` provides bootstrap instructions, shared preferences, rule
routing, and validation commands. Nested `AGENTS.md` files refer to the existing
directory instructions and path rules. Codex explicitly reads those documents;
Claude's `@` imports and glob rules are not assumed to load in Codex.

## Runtime behavior

- Map `/name` to `$studio-name`, using arguments from the user's invocation.
- Map Claude tool labels to available Codex tools, without inventing tool APIs.
- Use native role configuration where supported; otherwise pass the role document
  to an available subagent or perform clearly labeled sequential role passes.
- Keep user decisions and approval boundaries; an explicit request authorizes its
  implementation. Do not repeatedly ask permission for already authorized edits.
- Keep engine settings in `.claude/docs/technical-preferences.md`. Codex onboarding
  must update shared settings so either client sees the same project configuration.
- Keep Claude hook registration and behavior, excluding instruction files from
  game-content checks. Do not register them as Codex hooks; expose commit/push
  validators through an explicit portable runner.
- Retain engine neutrality; no game or engine is selected by the adaptation.

## Verification

Use Python 3.9+ standard-library integration tests for generation, drift detection,
preservation of custom files, unsafe path rejection, and the hook runner. Check
every generated entry point against its source and use Codex's local app server
to verify skill discovery and role configuration where supported. CI runs the
portable checks on Linux, macOS, and Windows. Live game and model behavior tests
are documented separately from structural validation.
