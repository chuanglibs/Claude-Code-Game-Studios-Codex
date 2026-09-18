# Codex runtime for shared studio workflows

The shared source lives under `.claude/` to preserve upstream compatibility.
Reading those files does not require Claude Code. Apply the following translations
whenever a Codex skill or role reads shared instructions. User instructions and
the current runtime's permissions take precedence over all template guidance.

## Loading instructions

Codex starts from `AGENTS.md` and discovers skills in `.agents/skills/`. It does
not gain this template's behavior merely from the presence of `CLAUDE.md`, Claude
`@path` imports, `.claude/settings.json`, or `.claude/rules/` path metadata.
Explicitly read the shared documents linked by the applicable instructions.
When you encounter an `@path` import, read that repository-relative file if it
is relevant to the current task. Do not load all workflows or engine references.

Exclude `AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, and `CLAUDE.local.md`
from game-content scans, GDD/ADR counts, and asset audits. Directories containing
only these files or `.gitkeep` are scaffolding, not implemented game systems.
Template tooling under `scripts/` and `tests/template/` is not game test evidence.

Read a shared skill's Markdown body. Its `allowed-tools`, `model`, `context`,
`agent`, `memory`, `maxTurns`, and other Claude frontmatter are **not** Codex
configuration or permission grants. A wrapper that names a role links its brief.
The `context` field may describe prerequisites: preserve that intent by checking
the body and referenced project artifacts rather than executing a Claude fork.

## Commands and arguments

- Translate studio `/name` references into `$studio-name`. Example:
  `/setup-engine godot 4.6` becomes `$studio-setup-engine godot 4.6`.
- `/help` in a shared workflow means `$studio-help`, not Codex's built-in help.
- Use the current invocation's trailing text wherever the source says
  `$ARGUMENTS`, argument, or input. There is no automatic Claude argument macro.
- For natural-language invocation, infer supplied arguments from the request and
  clarify required missing values. Do not invent a game idea or engine version.
- When a workflow recommends another command, present its Codex name. Continue
  into another workflow only when the user's task authorizes it.
- For skill discovery/status workflows, combine `.claude/docs/workflow-catalog.yaml`
  with `.claude/skills/*/SKILL.md`; present Codex entry names. The catalog can lag
  the source, so existing workflows outside the catalog must remain visible.
- Workflow arguments naming a skill or role (such as `$studio-skill-test static start`
  or `$studio-skill-improve start`) refer to the unprefixed shared source name.
  Normalize `studio-start` to `start` for source/catalog lookups.

## Tool translation

| Source term | Codex behavior |
| --- | --- |
| `Read`, `Glob`, `Grep` | Available file/search tools; shell reads and `rg` are suitable |
| `Write`, `Edit` | Available patch/file tools, within the authorized scope |
| `Bash` | Available shell execution tool; obey its sandbox and approval controls |
| `AskUserQuestion` | Available user-input tool; if unavailable in this mode, ask in conversation and wait when the answer is required |
| `TodoWrite` | Available plan tool, or a concise task checklist |
| `WebSearch`, `WebFetch` | Available browsing/retrieval tools; report if unavailable |
| `Task`, `subagent_type` | Available Codex subagent tools and role briefs, as described below |
| `Skill` | Read the corresponding `$studio-*` skill and follow its instructions |
| Claude agent teams | Use supported Codex delegation; do not set Claude environment variables |

Use the tool names and argument schemas actually exposed in this session. Do
not issue a tool call just because a shared document names it.

## Roles and delegation

The 49 `.codex/agents/studio-*.toml` files are project-scoped native Codex role
configurations for clients that support standalone custom agents. Each loads the
corresponding `.claude/agents/<role>.md` brief. They intentionally omit model,
reasoning effort, sandbox, and tool overrides so the current user's settings apply.
Claude's Haiku/Sonnet/Opus tiers do not select Codex models.

Delegate when the user requests it or the invoked workflow calls for it. Choose
only roles needed for the task, respect current concurrency limits, give each a
bounded responsibility, and avoid overlapping write ownership. Collect required
results before starting dependent stages. Ask the parent to resolve user decisions.

1. If the spawn tool exposes registered custom roles, select `studio-<role>`
   using that tool's supported field.
2. If it has no custom-role selector, use an available general subagent. Its task
   must explicitly say to read this runtime guide, the shared role brief, relevant
   directory instructions, and required input artifacts. Include scope, file
   ownership, and the expected output. A task name alone does not load a role.
3. If subagents are unavailable, perform sequential passes using the role briefs.
   Label the result as a single-agent role review. Do not claim an independent
   review occurred. If an independent reviewer is an explicit requirement, report
   that limitation and request an actual reviewer before declaring the gate passed.

Respect `full`, `lean`, and `solo` review mode semantics in the invoked workflow.
`solo` skips director gates; it does not by itself disable all specialist work.
Do not assume Claude agent-memory directories provide persistent Codex memory.
Record needed handoff state in project documents when authorized.

## Shared settings and collaboration

`.claude/docs/technical-preferences.md` is the shared engine/platform configuration.
No engine is selected in a fresh clone. Bundled Godot documentation is a reference,
not evidence that the project uses Godot.

`$studio-setup-engine` may update shared preferences, the engine/language summary
in root `CLAUDE.md`, reference docs, and other files the source workflow requires.
Root `AGENTS.md` reads the shared preferences and does not need duplicate engine
fields. Where a workflow says to read `CLAUDE.md` for project settings, also read
the shared preferences. Select the configured engine's references, not the default
Godot reference link in an unconfigured template.

Keep user control over material design and scope decisions. Ask only for missing
decisions or authorization. Treat an explicit implementation request as approval
for its necessary file edits; do not repeat “May I write?” for every file or phase
already authorized. An explicitly chosen interactive draft/review flow still has
its requested checkpoints. User permission never bypasses runtime sandbox controls.
Never treat a workflow's release/commit instructions as permission to publish,
push, send messages, or perform external actions outside the user's request.

## Hooks, checks, and session continuity

This adapter leaves `.claude/settings.json` and its 12 hooks in the Claude runtime;
it does **not** register equivalent Codex lifecycle/tool hooks. Do not claim its
notifications, session logging, compaction recovery, asset checks, or permission
deny patterns automatically apply to Codex. A client supporting Codex hooks would
need a separately reviewed event/schema integration.

Before an authorized commit, run `python3 scripts/studio_check.py commit`. Before
an authorized push, run `python3 scripts/studio_check.py push` and actual project
tests. These commands invoke the existing validators without committing/pushing.
The commit validator examines staged paths and reads working-tree content; it
does not validate an isolated index snapshot. The push validator warns about
protected branches; it does not execute the game test suite. Warnings are not
passing build/test evidence. For asset edits, validate the affected formats and
references using the selected engine's tools.

At the start of resumed work, read relevant project state under `production/`.
At handoff, report completed work, tests actually run, and outstanding blockers.
Persist necessary state in `production/session-state/` only when useful and within
the authorized task. Never assume Claude's session hooks wrote it for you.
