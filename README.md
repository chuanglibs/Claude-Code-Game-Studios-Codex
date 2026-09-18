<p align="center">
  <h1 align="center">Game Studios for Claude Code &amp; Codex</h1>
  <p align="center">
    Bring structured game development workflows to Claude Code and Codex.
    <br />
    49 agents. 73 skills. One coordinated AI team.
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href=".claude/agents"><img src="https://img.shields.io/badge/agents-49-blueviolet" alt="49 Agents"></a>
  <a href=".claude/skills"><img src="https://img.shields.io/badge/skills-73-green" alt="73 Skills"></a>
  <a href=".claude/hooks"><img src="https://img.shields.io/badge/hooks-12-orange" alt="12 Hooks"></a>
  <a href=".claude/rules"><img src="https://img.shields.io/badge/rules-11-red" alt="11 Rules"></a>
  <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/built%20for-Claude%20Code-f5f5f5?logo=anthropic" alt="Built for Claude Code"></a>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20this%20project-FFDD00?logo=buymeacoffee&logoColor=black" alt="Buy Me a Coffee"></a>
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-Support%20this%20project-ea4aaa?logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

---

[中文说明](README.zh-CN.md) · [Codex guide](docs/codex/README.md)

This is a dual-client fork of
[Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios).
It preserves the original studio workflows and Claude integration, and adds
checked-in Codex skills, native role configurations, and directory instructions.
In **Codex**, open this folder and enter **`$studio-start`**. In **Claude Code**,
run **`/start`**. Both clients share the same workflow sources; using Codex does
not require installing Claude Code. No engine is selected in a fresh clone.

## Why This Exists

Building a game solo with AI is powerful — but a single chat session has no structure. No one stops you from hardcoding magic numbers, skipping design docs, or writing spaghetti code. There's no QA pass, no design review, no one asking "does this actually fit the game's vision?"

**Claude Code Game Studios** solves this by giving your AI session the structure of a real studio. Instead of one general-purpose assistant, you get 49 specialized agents organized into a studio hierarchy — directors who guard the vision, department leads who own their domains, and specialists who do the hands-on work. Each agent has defined responsibilities, escalation paths, and quality gates.

The result: you still make every decision, but now you have a team that asks the right questions, catches mistakes early, and keeps your project organized from first brainstorm to launch.

---

## Table of Contents

- [Source and Fork Changes](#source-and-fork-changes)
- [What's Included](#whats-included)
- [Studio Hierarchy](#studio-hierarchy)
- [Slash Commands](#slash-commands)
- [Getting Started](#getting-started)
- [Codex Compatibility](#codex-compatibility)
- [Upgrading](#upgrading)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Design Philosophy](#design-philosophy)
- [Customization](#customization)
- [Platform Support](#platform-support)
- [Community](#community)
- [Acknowledgements](#acknowledgements)
- [Supporting This Project](#supporting-this-project)
- [License](#license)

---

## Source and Fork Changes

**Upstream source:** [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios),
created by Donchitos. **This fork:**
[chuanglibs/Claude-Code-Game-Studios-Codex](https://github.com/chuanglibs/Claude-Code-Game-Studios-Codex).
The original copyright notice and [MIT license](LICENSE) are retained.

The game-development workflows and role expertise come from the upstream
template. This fork adds a Codex integration around those shared sources;
the 73 Codex skill entries are adapters for the 73 existing workflows, not 73
additional workflows. Counts on this page describe the sources included here,
not necessarily the latest upstream release.

| Origin | Content / paths | Treatment in this fork |
| --- | --- | --- |
| Inherited from upstream | `.claude/skills/`, `.claude/agents/` | Shared workflow bodies and 49 role briefs; Claude entry names remain available |
| Inherited from upstream | `.claude/rules/`, `.claude/docs/`, `docs/engine-reference/`, `CCGS Skill Testing Framework/` | Shared standards, document templates, engine references, and behavioral test specifications |
| Adapted from upstream | `CLAUDE.md`, `start`, `project-stage-detect`, four hooks | Recognize dual-client instruction files; exclude them from game-content counts, asset checks, and design warnings |
| Added by this fork | Root and scoped `AGENTS.md`, `docs/codex/runtime.md` | Codex instruction entry points and translations for tools, roles, arguments, and collaboration |
| Added by this fork | `.agents/skills/studio-*/`, `.codex/agents/studio-*.toml` | Generated Codex entries pointing to shared upstream-derived workflow and role documents |
| Added by this fork | `scripts/sync_codex.py`, `scripts/studio_check.py` | Regenerate/check adapters and explicitly invoke the existing commit/push validators |
| Added by this fork | `tests/template/`, `.github/workflows/template-check.yml`, `.gitattributes` | Adapter regression tests, cross-platform CI, and LF checkout for Bash hooks |
| Updated / added by this fork | This README, `README.zh-CN.md`, `docs/codex/`, `CONTRIBUTING.md`, `UPGRADING.md`, `.gitignore` | Dual-client usage, provenance, maintenance instructions, and local configuration exclusions |

The four adjusted hooks are `detect-gaps.sh`, `pre-compact.sh`,
`validate-assets.sh`, and `validate-commit.sh`. Their Claude event registrations
remain in `.claude/settings.json`; this fork does not register them in Codex.

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| **Agents** | 49 | Specialized subagents across design, programming, art, audio, narrative, QA, and production |
| **Skills** | 73 | Shared workflows: `/name` in Claude Code, `$studio-name` in Codex |
| **Hooks** | 12 | Claude Code automation for commits, pushes, assets, sessions, and agent audit trails; explicit validators available in Codex |
| **Rules** | 11 | Shared directory guidance, loaded by Claude path rules or Codex `AGENTS.md` instructions |
| **Templates** | 41 | Document templates for GDDs, UX specs, ADRs, sprint plans, HUD design, accessibility, and more |

## Studio Hierarchy

Agents are organized into three tiers, matching how real studios operate.
The model tiers below apply to Claude Code; Codex roles inherit your selected
model and reasoning settings:

```
Tier 1 — Directors (Opus)
  creative-director    technical-director    producer

Tier 2 — Department Leads (Sonnet)
  game-designer        lead-programmer       art-director
  audio-director       narrative-director    qa-lead
  release-manager      localization-lead

Tier 3 — Specialists (Sonnet/Haiku)
  gameplay-programmer  engine-programmer     ai-programmer
  network-programmer   tools-programmer      ui-programmer
  systems-designer     level-designer        economy-designer
  technical-artist     sound-designer        writer
  world-builder        ux-designer           prototyper
  performance-analyst  devops-engineer       analytics-engineer
  security-engineer    qa-tester             accessibility-specialist
  live-ops-designer    community-manager
```

### Engine Specialists

The template includes agent sets for all three major engines. Use the set that matches your project:

| Engine | Lead Agent | Sub-Specialists |
|--------|-----------|-----------------|
| **Godot 4** | `godot-specialist` | GDScript, Shaders, GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS, Shaders/VFX, Addressables, UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS, Blueprints, Replication, UMG/CommonUI |

## Slash Commands

Every original studio command maps to one Codex skill:

```text
Claude Code: /<name> <arguments>
Codex:       $studio-<name> <arguments>
```

Enter these in the client's conversation, **not in a shell**. Change the command
prefix; keep its arguments, file paths, and supported flags. `studio-` avoids
collisions with personal skills and built-in commands. In particular, the
studio's `/help` becomes `$studio-help`, not Codex's built-in `/help`.

### Examples with arguments

| Task | Original Claude Code command | Codex equivalent |
| --- | --- | --- |
| First session | `/start` | `$studio-start` |
| Find the next workflow | `/help` | `$studio-help` |
| Explore a game concept | `/brainstorm open` | `$studio-brainstorm open` |
| Configure an engine | `/setup-engine godot 4.6` | `$studio-setup-engine godot 4.6` |
| Design a system | `/design-system player-movement --review lean` | `$studio-design-system player-movement --review lean` |
| Break down an epic | `/create-stories combat` | `$studio-create-stories combat` |
| Implement an existing story | `/dev-story <story-path>` | `$studio-dev-story <story-path>` |
| Coordinate a combat feature | `/team-combat melee parry --review lean` | `$studio-team-combat melee parry --review lean` |
| Validate the start skill | `/skill-test static start` | `$studio-skill-test static start` |

The engine/version is an example, not a selected project setting. Replace
`<story-path>` with an existing story file. Flags such as `--review lean` apply
only to workflows that support them. In `skill-test static start`, `start` is
the shared skill name used as an argument; it does not need a `studio-` prefix.

### Complete workflow mapping

Each first-column link opens the **shared workflow source**. Its corresponding
Codex entry lives at `.agents/skills/studio-<name>/SKILL.md` and reads that source
with the [runtime translations](docs/codex/runtime.md). The workflow's arguments,
prerequisites, and output paths are defined in the linked source.

<details>
<summary>All 73 workflows: original Claude Code command → Codex command</summary>

| Shared workflow source | Original Claude Code | Codex in this fork |
| --- | --- | --- |
| [adopt](.claude/skills/adopt/SKILL.md) | `/adopt` | `$studio-adopt` |
| [architecture-decision](.claude/skills/architecture-decision/SKILL.md) | `/architecture-decision` | `$studio-architecture-decision` |
| [architecture-review](.claude/skills/architecture-review/SKILL.md) | `/architecture-review` | `$studio-architecture-review` |
| [art-bible](.claude/skills/art-bible/SKILL.md) | `/art-bible` | `$studio-art-bible` |
| [asset-audit](.claude/skills/asset-audit/SKILL.md) | `/asset-audit` | `$studio-asset-audit` |
| [asset-spec](.claude/skills/asset-spec/SKILL.md) | `/asset-spec` | `$studio-asset-spec` |
| [balance-check](.claude/skills/balance-check/SKILL.md) | `/balance-check` | `$studio-balance-check` |
| [brainstorm](.claude/skills/brainstorm/SKILL.md) | `/brainstorm` | `$studio-brainstorm` |
| [bug-report](.claude/skills/bug-report/SKILL.md) | `/bug-report` | `$studio-bug-report` |
| [bug-triage](.claude/skills/bug-triage/SKILL.md) | `/bug-triage` | `$studio-bug-triage` |
| [changelog](.claude/skills/changelog/SKILL.md) | `/changelog` | `$studio-changelog` |
| [code-review](.claude/skills/code-review/SKILL.md) | `/code-review` | `$studio-code-review` |
| [consistency-check](.claude/skills/consistency-check/SKILL.md) | `/consistency-check` | `$studio-consistency-check` |
| [content-audit](.claude/skills/content-audit/SKILL.md) | `/content-audit` | `$studio-content-audit` |
| [create-architecture](.claude/skills/create-architecture/SKILL.md) | `/create-architecture` | `$studio-create-architecture` |
| [create-control-manifest](.claude/skills/create-control-manifest/SKILL.md) | `/create-control-manifest` | `$studio-create-control-manifest` |
| [create-epics](.claude/skills/create-epics/SKILL.md) | `/create-epics` | `$studio-create-epics` |
| [create-stories](.claude/skills/create-stories/SKILL.md) | `/create-stories` | `$studio-create-stories` |
| [day-one-patch](.claude/skills/day-one-patch/SKILL.md) | `/day-one-patch` | `$studio-day-one-patch` |
| [design-review](.claude/skills/design-review/SKILL.md) | `/design-review` | `$studio-design-review` |
| [design-system](.claude/skills/design-system/SKILL.md) | `/design-system` | `$studio-design-system` |
| [dev-story](.claude/skills/dev-story/SKILL.md) | `/dev-story` | `$studio-dev-story` |
| [estimate](.claude/skills/estimate/SKILL.md) | `/estimate` | `$studio-estimate` |
| [gate-check](.claude/skills/gate-check/SKILL.md) | `/gate-check` | `$studio-gate-check` |
| [help](.claude/skills/help/SKILL.md) | `/help` | `$studio-help` |
| [hotfix](.claude/skills/hotfix/SKILL.md) | `/hotfix` | `$studio-hotfix` |
| [launch-checklist](.claude/skills/launch-checklist/SKILL.md) | `/launch-checklist` | `$studio-launch-checklist` |
| [localize](.claude/skills/localize/SKILL.md) | `/localize` | `$studio-localize` |
| [map-systems](.claude/skills/map-systems/SKILL.md) | `/map-systems` | `$studio-map-systems` |
| [milestone-review](.claude/skills/milestone-review/SKILL.md) | `/milestone-review` | `$studio-milestone-review` |
| [onboard](.claude/skills/onboard/SKILL.md) | `/onboard` | `$studio-onboard` |
| [patch-notes](.claude/skills/patch-notes/SKILL.md) | `/patch-notes` | `$studio-patch-notes` |
| [perf-profile](.claude/skills/perf-profile/SKILL.md) | `/perf-profile` | `$studio-perf-profile` |
| [playtest-report](.claude/skills/playtest-report/SKILL.md) | `/playtest-report` | `$studio-playtest-report` |
| [project-stage-detect](.claude/skills/project-stage-detect/SKILL.md) | `/project-stage-detect` | `$studio-project-stage-detect` |
| [propagate-design-change](.claude/skills/propagate-design-change/SKILL.md) | `/propagate-design-change` | `$studio-propagate-design-change` |
| [prototype](.claude/skills/prototype/SKILL.md) | `/prototype` | `$studio-prototype` |
| [qa-plan](.claude/skills/qa-plan/SKILL.md) | `/qa-plan` | `$studio-qa-plan` |
| [quick-design](.claude/skills/quick-design/SKILL.md) | `/quick-design` | `$studio-quick-design` |
| [regression-suite](.claude/skills/regression-suite/SKILL.md) | `/regression-suite` | `$studio-regression-suite` |
| [release-checklist](.claude/skills/release-checklist/SKILL.md) | `/release-checklist` | `$studio-release-checklist` |
| [retrospective](.claude/skills/retrospective/SKILL.md) | `/retrospective` | `$studio-retrospective` |
| [reverse-document](.claude/skills/reverse-document/SKILL.md) | `/reverse-document` | `$studio-reverse-document` |
| [review-all-gdds](.claude/skills/review-all-gdds/SKILL.md) | `/review-all-gdds` | `$studio-review-all-gdds` |
| [scope-check](.claude/skills/scope-check/SKILL.md) | `/scope-check` | `$studio-scope-check` |
| [security-audit](.claude/skills/security-audit/SKILL.md) | `/security-audit` | `$studio-security-audit` |
| [setup-engine](.claude/skills/setup-engine/SKILL.md) | `/setup-engine` | `$studio-setup-engine` |
| [skill-improve](.claude/skills/skill-improve/SKILL.md) | `/skill-improve` | `$studio-skill-improve` |
| [skill-test](.claude/skills/skill-test/SKILL.md) | `/skill-test` | `$studio-skill-test` |
| [smoke-check](.claude/skills/smoke-check/SKILL.md) | `/smoke-check` | `$studio-smoke-check` |
| [soak-test](.claude/skills/soak-test/SKILL.md) | `/soak-test` | `$studio-soak-test` |
| [sprint-plan](.claude/skills/sprint-plan/SKILL.md) | `/sprint-plan` | `$studio-sprint-plan` |
| [sprint-status](.claude/skills/sprint-status/SKILL.md) | `/sprint-status` | `$studio-sprint-status` |
| [start](.claude/skills/start/SKILL.md) | `/start` | `$studio-start` |
| [story-done](.claude/skills/story-done/SKILL.md) | `/story-done` | `$studio-story-done` |
| [story-readiness](.claude/skills/story-readiness/SKILL.md) | `/story-readiness` | `$studio-story-readiness` |
| [team-audio](.claude/skills/team-audio/SKILL.md) | `/team-audio` | `$studio-team-audio` |
| [team-combat](.claude/skills/team-combat/SKILL.md) | `/team-combat` | `$studio-team-combat` |
| [team-level](.claude/skills/team-level/SKILL.md) | `/team-level` | `$studio-team-level` |
| [team-live-ops](.claude/skills/team-live-ops/SKILL.md) | `/team-live-ops` | `$studio-team-live-ops` |
| [team-narrative](.claude/skills/team-narrative/SKILL.md) | `/team-narrative` | `$studio-team-narrative` |
| [team-polish](.claude/skills/team-polish/SKILL.md) | `/team-polish` | `$studio-team-polish` |
| [team-qa](.claude/skills/team-qa/SKILL.md) | `/team-qa` | `$studio-team-qa` |
| [team-release](.claude/skills/team-release/SKILL.md) | `/team-release` | `$studio-team-release` |
| [team-ui](.claude/skills/team-ui/SKILL.md) | `/team-ui` | `$studio-team-ui` |
| [tech-debt](.claude/skills/tech-debt/SKILL.md) | `/tech-debt` | `$studio-tech-debt` |
| [test-evidence-review](.claude/skills/test-evidence-review/SKILL.md) | `/test-evidence-review` | `$studio-test-evidence-review` |
| [test-flakiness](.claude/skills/test-flakiness/SKILL.md) | `/test-flakiness` | `$studio-test-flakiness` |
| [test-helpers](.claude/skills/test-helpers/SKILL.md) | `/test-helpers` | `$studio-test-helpers` |
| [test-setup](.claude/skills/test-setup/SKILL.md) | `/test-setup` | `$studio-test-setup` |
| [ux-design](.claude/skills/ux-design/SKILL.md) | `/ux-design` | `$studio-ux-design` |
| [ux-review](.claude/skills/ux-review/SKILL.md) | `/ux-review` | `$studio-ux-review` |
| [vertical-slice](.claude/skills/vertical-slice/SKILL.md) | `/vertical-slice` | `$studio-vertical-slice` |

</details>

Switching clients preserves the same progression and project artifacts: concept,
prototype, system design, architecture, epics/stories, implementation, validation,
and release. Use the client's corresponding entry at each step; the mapping
changes the entry point, not the game-document paths or workflow prerequisites.

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/)
- Either [Codex](https://developers.openai.com/codex/quickstart) or [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- **For template maintenance**: Python 3.9+ (standard library only)
- **For hooks/explicit validators**: Bash (Git Bash on Windows); [jq](https://jqlang.github.io/jq/) and Python are recommended for validation

All hooks fail gracefully if optional tools are missing — nothing breaks, you just lose validation.

### Setup

1. **Clone or use as template**:
   ```bash
   git clone https://github.com/chuanglibs/Claude-Code-Game-Studios-Codex.git my-game
   cd my-game
   ```

2. **Open your client** from the repository root:
   ```bash
   codex
   ```
   Or open the folder in Codex desktop/IDE. For Claude Code, run `claude`.

3. **Enter `$studio-start` in Codex, or `/start` in Claude Code** — the system asks where you are (no idea, vague concept,
   clear design, existing work) and guides you to the right workflow. No assumptions.

   Or jump directly to a specific skill if you already know what you need:
   - `/brainstorm` — explore game ideas from scratch
   - `/setup-engine godot 4.6` — configure your engine if you already know
   - `/project-stage-detect` — analyze an existing project

   In Codex, those are `$studio-brainstorm`, `$studio-setup-engine godot 4.6`,
   and `$studio-project-stage-detect`. The version is an example; verify the
   version chosen for your project.

## Codex Compatibility

### Original usage and current equivalents

The original Claude Code entry points remain usable in this fork. Codex uses
the corresponding adapter entry points:

| Original Claude Code usage | Codex usage in this fork | Shared behavior / difference |
| --- | --- | --- |
| Run `claude` in the project | Run `codex`, or open the same folder in Codex desktop/IDE | Choose either client; no global template installation |
| `CLAUDE.md` and `@path` imports | `AGENTS.md` and explicit linked-file reads | Same project guidance, different loading mechanism |
| `.claude/skills/<name>/SKILL.md` via `/<name>` | `.agents/skills/studio-<name>/SKILL.md` via `$studio-<name>` | The wrapper reads the same workflow body; see the complete command mapping above |
| `.claude/agents/<role>.md`, e.g. `technical-director` | `.codex/agents/studio-<role>.toml`, e.g. `studio-technical-director` | Same role brief; unsupported clients use the documented role fallback |
| `.claude/rules/` and directory `CLAUDE.md` | 15 generated scoped `AGENTS.md` files | Read the same directory rules; do not assume Claude glob rules load automatically |
| Claude model tiers: Haiku / Sonnet / Opus | Current Codex model and reasoning settings | No automatic model-name conversion or hardcoded Codex model |
| `.claude/docs/technical-preferences.md`, `production/review-mode.txt` | The same files | Engine, platform, and review mode stay shared |
| Existing GDDs, ADRs, epics, stories, and game files | The same paths and documents | Switching clients does not require renaming or migrating game content |
| `Task`, `AskUserQuestion`, and other Claude tool labels | Available Codex delegation, user-input, and file tools | Runtime instructions translate intent, not literal tool API calls |
| Guided approvals at each write | Reuse authorization for explicitly requested implementation; retain chosen review gates | User control remains; Codex avoids repeating permission requests for authorized edits |
| Automatic pre-commit/pre-push hooks | `python3 scripts/studio_check.py commit` / `push` | Explicit validation only; never commits, pushes, or runs the game test suite |
| Asset/session/notification/compaction hooks and Claude permission rules | Current Codex permissions plus explicit checks and handoff notes | No automatic one-to-one replacement is installed |

Codex reads the root and scoped `AGENTS.md` instructions and discovers the 73
`.agents/skills/studio-*` wrappers. The 49 `.codex/agents/studio-*.toml` files
configure native roles on supported clients. Workflows fall back to explicit
role briefs when the client doesn't expose native role selection or subagents.
See the [Codex guide](docs/codex/README.md) for behavior and limitations.

The `.claude/` directory remains the shared source for both clients. After
changing skills, roles, or rules, regenerate and validate:

```bash
python3 scripts/sync_codex.py
python3 scripts/sync_codex.py --check
python3 -m unittest discover -s tests/template -v
```

This adapter does not register the Claude hooks or permission rules in Codex.
Use `python3 scripts/studio_check.py commit` or `python3 scripts/studio_check.py push`
for explicit validation; neither command commits, pushes, or runs game tests.

## Upgrading

Already using an older version of this template? See [UPGRADING.md](UPGRADING.md)
for step-by-step migration instructions, a breakdown of what changed between
versions, and which files are safe to overwrite vs. which need a manual merge.

## Project Structure

```
AGENTS.md                           # Codex project entry point
CLAUDE.md                           # Claude Code project entry point
.agents/skills/studio-*/             # 73 generated Codex skill entry points
.codex/agents/studio-*.toml          # 49 generated native Codex role configurations
scripts/                            # Adapter generation and explicit validation
.claude/
  settings.json                     # Hooks, permissions, safety rules
  agents/                           # 49 agent definitions (markdown + YAML frontmatter)
  skills/                           # 73 slash commands (subdirectory per skill)
  hooks/                            # 12 hook scripts (bash, cross-platform)
  rules/                            # 11 path-scoped coding standards
  statusline.sh                     # Status line script (context%, model, stage, epic breadcrumb)
  docs/
    workflow-catalog.yaml           # 7-phase pipeline definition (read by /help)
    templates/                      # 41 document templates
src/                                # Game source code
assets/                             # Art, audio, VFX, shaders, data files
design/                             # GDDs, narrative docs, level designs
docs/                               # Technical documentation, ADRs, and codex/ guide
tests/                              # Test suites (unit, integration, performance, playtest)
tools/                              # Build and pipeline tools
prototypes/                         # Throwaway prototypes (isolated from src/)
production/                         # Sprint plans, milestones, release tracking
```

## How It Works

### Agent Coordination

Agents follow a structured delegation model:

1. **Vertical delegation** — directors delegate to leads, leads delegate to specialists
2. **Horizontal consultation** — same-tier agents can consult each other but can't make binding cross-domain decisions
3. **Conflict resolution** — disagreements escalate up to the shared parent (`creative-director` for design, `technical-director` for technical)
4. **Change propagation** — cross-department changes are coordinated by `producer`
5. **Domain boundaries** — agents don't modify files outside their domain without explicit delegation

### Collaborative, Not Autonomous

The studio keeps game direction and important design choices with the user.
The shared workflows offer a guided collaboration protocol:

1. **Ask** — agents ask questions before proposing solutions
2. **Present options** — agents show 2-4 options with pros/cons
3. **You decide** — the user always makes the call
4. **Draft** — agents show work before finalizing
5. **Approve** — nothing gets written without your sign-off

For Codex, an explicit request to implement a task authorizes the edits needed
for that task. It does not repeat file-by-file permission requests for already
authorized work. Explicit draft/review checkpoints still apply, and sandbox
permissions remain controlled by the client.

### Automated Safety

In **Claude Code**, hooks run automatically on configured events:

| Hook | Trigger | What It Does |
|------|---------|--------------|
| `validate-commit.sh` | PreToolUse (Bash) | Checks for hardcoded values, TODO format, JSON validity, design doc sections — exits early if the command is not `git commit` |
| `validate-push.sh` | PreToolUse (Bash) | Warns on pushes to protected branches — exits early if the command is not `git push` |
| `validate-assets.sh` | PostToolUse (Write/Edit) | Validates naming conventions and JSON structure — exits early if the file is not in `assets/` |
| `session-start.sh` | Session open | Shows current branch and recent commits for orientation |
| `detect-gaps.sh` | Session open | Detects fresh projects (suggests `/start`) and missing design docs when code or prototypes exist |
| `pre-compact.sh` | Before compaction | Preserves session progress notes |
| `post-compact.sh` | After compaction | Reminds Claude to restore session state from `active.md` |
| `notify.sh` | Notification event | Shows Windows toast notification via PowerShell |
| `session-stop.sh` | Session close | Archives `active.md` to session log and records git activity |
| `log-agent.sh` | Agent spawned | Audit trail start — logs subagent invocation |
| `log-agent-stop.sh` | Agent stops | Audit trail stop — completes subagent record |
| `validate-skill-change.sh` | PostToolUse (Write/Edit) | Advises running `/skill-test` after any `.claude/skills/` change |

> **Note**: `validate-commit.sh`, `validate-assets.sh`, and `validate-skill-change.sh` fire on every Bash/Write tool call and exit immediately (exit 0) when the command or file path is not relevant. This is normal hook behavior — not a performance concern.

**Claude permission rules** in `.claude/settings.json` auto-allow configured
operations and deny matching command/file patterns. Codex uses its own sandbox
and approval settings; this adapter does not copy those permissions.

### Path-Scoped Rules

Coding guidance is scoped by file location. Claude loads path rules; Codex reads
the corresponding nested `AGENTS.md` and linked shared rules:

| Path | Enforces |
|------|----------|
| `src/gameplay/**` | Data-driven values, delta time usage, no UI references |
| `src/core/**` | Zero allocations in hot paths, thread safety, API stability |
| `src/ai/**` | Performance budgets, debuggability, data-driven parameters |
| `src/networking/**` | Server-authoritative, versioned messages, security |
| `src/ui/**` | No game state ownership, localization-ready, accessibility |
| `design/gdd/**` | Required 8 sections, formula format, edge cases |
| `design/narrative/**` | Lore consistency, character voice, canon levels |
| `assets/data/**` | Valid data, naming conventions, schema requirements |
| `assets/shaders/**` | Shader naming, performance, cross-platform constraints |
| `tests/**` | Test naming, coverage requirements, fixture patterns |
| `prototypes/**` | Relaxed standards, README required, hypothesis documented |

## Design Philosophy

This template is grounded in professional game development practices:

- **MDA Framework** — Mechanics, Dynamics, Aesthetics analysis for game design
- **Self-Determination Theory** — Autonomy, Competence, Relatedness for player motivation
- **Flow State Design** — Challenge-skill balance for player engagement
- **Bartle Player Types** — Audience targeting and validation
- **Verification-Driven Development** — Tests first, then implementation

## Customization

This is a **template**, not a locked framework. Everything is meant to be customized:

For Codex, regenerate after editing shared sources. Keep custom adapter changes
in the generator/runtime guide, or add uniquely named custom skills and roles.
When changing commands, source attribution, directory layout, setup, or compatibility
behavior, update **both `README.md` and `README.zh-CN.md`** in the same changeset.
Keep their command tables aligned with the shared sources and generated entries.

- **Add/remove agents** — delete agent files you don't need, add new ones for your domains
- **Edit agent prompts** — tune agent behavior, add project-specific knowledge
- **Modify skills** — adjust workflows to match your team's process
- **Add rules** — create new path-scoped rules for your project's directory structure
- **Tune hooks** — adjust validation strictness, add new checks
- **Pick your engine** — use the Godot, Unity, or Unreal agent set (or none)
- **Set review intensity** — `full` (all director gates), `lean` (phase gates only), or `solo` (no director gates). Set during `/start` or `$studio-start`, or edit `production/review-mode.txt`. Override per-run with `--review solo` on workflows that support the flag.

## Platform Support

The Codex adapter uses ordinary files (no symlinks) and Python 3.9+ without
third-party dependencies. Its GitHub Actions workflow checks generation and
tooling tests on Linux, macOS, and Windows. Local validation results do not
imply that those hosted CI jobs have already run.

The upstream template reports primary development and testing on **Windows 10**
with Git Bash. Its hooks use `grep -E` rather than `grep -P` and include optional
tool fallbacks. The inherited `notify.sh` uses PowerShell for Windows toast
notifications and is a no-op elsewhere. For this fork's local Codex validation
and remaining manual checks, see the [Codex guide](docs/codex/README.md).

## Community

- **Discussions** — [GitHub Discussions](https://github.com/Donchitos/Claude-Code-Game-Studios/discussions) for questions, ideas, and showcasing what you've built
- **Fork issues** — [Codex compatibility bugs and feature requests](https://github.com/chuanglibs/Claude-Code-Game-Studios-Codex/issues)
- **Upstream issues** — [Original studio framework](https://github.com/Donchitos/Claude-Code-Game-Studios/issues)

---

## Acknowledgements

Thank you to **Donchitos** and the contributors to
[Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
for creating and sharing the original game studio template. Its specialized
roles, development workflows, and documentation provide the foundation for this
project's Codex adaptation.

This fork builds on their work and retains the original attribution and MIT
license. If you find this template useful, please visit the upstream repository,
give it a star, or support its author through the links below.

## Supporting This Project

The original Claude Code Game Studios is free and open source. The following
links support the upstream author:

<p>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"></a>
  &nbsp;
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

- **[Buy Me a Coffee](https://www.buymeacoffee.com/donchitos3)** — one-time support
- **[GitHub Sponsors](https://github.com/sponsors/Donchitos)** — recurring support through GitHub

Sponsorships help fund time spent maintaining skills, adding new agents, keeping up with Claude Code and engine API changes, and responding to community issues.

---

*Originally built for Claude Code by Donchitos; this fork adds Codex compatibility.*

## License

MIT License. See [LICENSE](LICENSE) for details.
