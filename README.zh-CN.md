# Game Studios：Claude Code / Codex 双平台模版

基于 [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)，
保留原有 Claude Code 工作流，同时提供可以直接被 Codex 发现的入口。

包含 **73 个工作流技能、49 个专业角色、11 组目录规则**，覆盖游戏构思、
设计、架构、开发、测试和发布。新建项目尚未选择引擎，也不包含可运行的游戏。

## 来源与本仓库改动

- **上游源仓库**：[Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)，原作者为 Donchitos。
- **当前适配仓库**：[chuanglibs/Claude-Code-Game-Studios-Codex](https://github.com/chuanglibs/Claude-Code-Game-Studios-Codex)。
- **许可证**：保留原作者版权声明及 [MIT 许可证](LICENSE)。

游戏开发流程、专业角色、设计方法和文档模版来自上游。本仓库在这些共享内容之上
增加 Codex 适配。**73 个 Codex 入口对应原有 73 个工作流，不是额外新增的 73 套流程。**
本文数量以本仓库包含的源文件为准，不代表上游最新版本的数量。

| 来源 | 内容或路径 | 本仓库如何处理 |
| --- | --- | --- |
| 继承上游 | `.claude/skills/`、`.claude/agents/` | 共用工作流正文和 49 个角色说明，保留 Claude 原命令名 |
| 继承上游 | `.claude/rules/`、`.claude/docs/`、`docs/engine-reference/`、`CCGS Skill Testing Framework/` | 共用规范、文档模版、引擎参考和行为测试规格 |
| 基于上游修改 | `CLAUDE.md`、`start`、`project-stage-detect`、4 个 hooks | 识别双平台说明文件，避免把它们当成游戏设计文档、资产或已实现系统 |
| 本仓库新增 | 根目录及各目录 `AGENTS.md`、`docs/codex/runtime.md` | Codex 说明入口，以及工具、参数、角色和协作行为的适配规则 |
| 本仓库新增 | `.agents/skills/studio-*/`、`.codex/agents/studio-*.toml` | 生成 Codex 技能与角色入口，引用上游衍生的共享正文 |
| 本仓库新增 | `scripts/sync_codex.py`、`scripts/studio_check.py` | 同步和检查适配文件，手动调用原有提交/推送检查脚本 |
| 本仓库新增 | `tests/template/`、`.github/workflows/template-check.yml`、`.gitattributes` | 适配回归测试、跨平台 CI、Bash hooks 的 LF 换行约定 |
| 本仓库更新或新增 | 中英文 README、`docs/codex/`、`CONTRIBUTING.md`、`UPGRADING.md`、`.gitignore` | 双平台使用、来源标注、维护说明和本地配置忽略规则 |

调整的 4 个 hooks 是 `detect-gaps.sh`、`pre-compact.sh`、`validate-assets.sh` 和
`validate-commit.sh`。它们仍由 `.claude/settings.json` 在 Claude Code 中注册，
本次适配没有将它们注册成 Codex hooks。

## 使用 Codex

```bash
git clone https://github.com/chuanglibs/Claude-Code-Game-Studios-Codex.git my-game
cd my-game
codex
```

也可以在 Codex 桌面端或 IDE 扩展里直接打开该目录，按提示确认项目信任。
然后在 **Codex 对话框**输入：

```text
$studio-start
```

查看工作流导航：`$studio-help`。继续某项工作时，例如：

```text
$studio-brainstorm 一款小体量的探索游戏
$studio-setup-engine godot 4.6
$studio-design-system 玩家移动系统
$studio-team-combat 近战弹反机制 --review lean
```

引擎版本只是参数示例，请根据项目选择并核对。使用模版不需要安装 Claude Code，
也不需要复制文件到用户目录或运行初始化脚本。Codex 沿用你当前的模型设置。

## 使用 Claude Code

在同一目录运行 `claude`，然后输入 `/start`。原有 `.claude/` 配置和技能路径保留。
两端共用 `.claude/docs/technical-preferences.md` 中的引擎、平台和开发偏好。

## 原用法与当前用法如何对应

| 内容 | 原来的 Claude Code 用法（本仓库仍支持） | 当前 Codex 用法 |
| --- | --- | --- |
| 启动客户端 | 在项目根目录运行 `claude` | 运行 `codex`，或在桌面端/IDE 打开同一目录 |
| 项目说明入口 | `CLAUDE.md` 和 `@path` 导入 | `AGENTS.md` 显式读取关联文件 |
| 开始引导 | `/start` | `$studio-start` |
| 工作流正文 | `.claude/skills/<name>/SKILL.md` | `.agents/skills/studio-<name>/SKILL.md` 读取同一份正文 |
| 角色定义 | `.claude/agents/<role>.md`，例如 `technical-director` | `.codex/agents/studio-<role>.toml`，例如 `studio-technical-director`，引用同一角色说明 |
| 目录规则 | `.claude/rules/` 和目录 `CLAUDE.md` | 15 个生成的目录 `AGENTS.md` 显式读取同一规则 |
| 模型选择 | 原有 Haiku / Sonnet / Opus 分层 | 沿用用户的 Codex 模型和推理设置，不直接转换 Claude 模型名 |
| 引擎、平台、审查模式 | `technical-preferences.md`、`production/review-mode.txt` | 继续读写同一文件 |
| GDD、ADR、Epic、Story 和游戏文件 | 原有 `design/`、`docs/architecture/`、`production/` 等路径 | 路径与内容不变，切换客户端不需要迁移游戏资料 |
| 工具调用 | `Task`、`AskUserQuestion` 等 Claude 工具 | 映射到当前可用的 Codex 工具，不照搬工具 API |
| 写入审批 | 原有逐步问答、草稿、确认流程 | 已明确授权的实现不逐文件重复确认；保留用户选择的审查节点 |
| 提交/推送检查 | 原 hooks 自动触发 | 手动运行 `python3 scripts/studio_check.py commit` 或 `push` |
| 其他 hooks 与权限 | Claude 会话、通知、资产、压缩恢复 hooks 和权限规则 | 没有自动安装等价 hooks；使用 Codex 当前权限及显式检查、交接说明 |

`studio-` 前缀用于避免与个人技能或内置命令重名。角色按工作流需要调用，不会同时
启动 49 个代理。如果当前 Codex 不支持原生角色选择，会把角色说明交给可用子代理；
没有子代理能力时，明确标注为单代理顺序审查。

## 命令与参数对照

所有工作流遵循同一个入口映射规则：

```text
原 Claude Code：/<name> <arguments>
当前 Codex：    $studio-<name> <arguments>
```

在**客户端对话框**输入这些命令，不是在终端中执行。只改变命令前缀，参数、文件路径
和该技能支持的选项保持不变。原工作流里的 `/help` 对应 `$studio-help`，不要与
Codex 自身的 `/help` 混用。

| 要做的事 | 原 Claude Code 命令 | Codex 对应命令 |
| --- | --- | --- |
| 首次引导 | `/start` | `$studio-start` |
| 查看下一步工作流 | `/help` | `$studio-help` |
| 开放式构思 | `/brainstorm open` | `$studio-brainstorm open` |
| 配置引擎 | `/setup-engine godot 4.6` | `$studio-setup-engine godot 4.6` |
| 设计系统 | `/design-system player-movement --review lean` | `$studio-design-system player-movement --review lean` |
| 拆分 Epic | `/create-stories combat` | `$studio-create-stories combat` |
| 实现已有 Story | `/dev-story <story-path>` | `$studio-dev-story <story-path>` |
| 协作开发战斗功能 | `/team-combat 近战弹反 --review lean` | `$studio-team-combat 近战弹反 --review lean` |
| 静态检查 start 技能 | `/skill-test static start` | `$studio-skill-test static start` |

将 `<story-path>` 替换为已有故事文件路径；引擎和版本只是参数示例。
`--review lean` 等选项仅用于支持它们的技能。在 `skill-test static start` 中，
作为参数的 `start` 是共享技能名，不需要再加 `studio-` 前缀。

### 全部 73 个工作流映射

第一列链接到**共享工作流源文件**，包含具体参数、前置条件和输出路径。
对应的 Codex 入口位于 `.agents/skills/studio-<name>/SKILL.md`，会读取这份源文件，
并应用 [Codex 运行时适配说明](docs/codex/runtime.md)。

<details>
<summary>展开全部 73 个工作流：原 Claude Code 命令 → Codex 命令</summary>

| 共享工作流源文件 | 原 Claude Code | 当前 Codex |
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

从构思、原型、系统设计、架构、Epic/Story，到实现、验证和发布，仍沿用原工作流的
阶段关系和项目资料。切换客户端时选择对应入口即可，不需要重命名游戏文档或跳过前置步骤。

## 维护模版

工作流正文只维护一份。修改 `.claude/` 下的技能、角色或规则后，用 **Python 3.9+** 运行：

```bash
python3 scripts/sync_codex.py
python3 scripts/sync_codex.py --check
python3 -m unittest discover -s tests/template -v
```

生成器只更新带标记的文件，保留其他自定义技能和角色。不要直接编辑生成文件。
不需要安装 Python 第三方依赖；Windows 可以使用 `py -3` 替代 `python3`。
修改命令、来源归属、目录结构、安装步骤或兼容行为时，**在同一次改动中同步更新
`README.md` 和 `README.zh-CN.md`**，并核对本页的完整命令映射与源文件、生成入口一致。

需要提交或推送检查时：

```bash
python3 scripts/studio_check.py commit
python3 scripts/studio_check.py push
```

这些命令需要 Git 和 Bash，**只做检查，不会提交或推送**。提交检查使用暂存文件列表
但读取工作区内容；推送检查只提醒受保护分支。它们不会运行游戏测试，不能替代引擎构建。
Claude 的会话记录、通知、资产检查和权限配置也不会自动转移到 Codex。

完整兼容说明、升级办法与手动验证步骤见 [Codex 使用指南](docs/codex/README.md)。

## 致谢

感谢 **Donchitos** 及
[Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
的贡献者创建并开源这套游戏工作室模版。原项目提供的专业角色、开发工作流和文档体系，
是本仓库进行 Codex 适配的基础。

本仓库在原项目的工作之上扩展，保留原作者署名及 [MIT 许可证](LICENSE)。如果这个
模版对你有帮助，欢迎访问原仓库、点亮 Star，或通过
[GitHub Sponsors](https://github.com/sponsors/Donchitos) 支持原作者。
