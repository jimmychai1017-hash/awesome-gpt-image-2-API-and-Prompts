# CLAUDE.md

本文件是 AI 助手在这个仓库里的工作宪法，每个会话自动加载。详细规则的权威来源是 `docs/maintenance.md`、`CONTRIBUTING.md` 和 `.github/PULL_REQUEST_TEMPLATE.md`；本文件与它们冲突时，以它们为准，并顺手修正本文件。

## 仓库是什么

GPT Image 2 的 prompt 案例库（prompt-first），不是可运行的 API 或 Skill 仓库。内容面：

- `README.md` —— 英文主页，结构与编号的唯一真实来源。
- `README_<locale>.md` —— 10 个本地化版本：`de es fr ja ko pt ru tr zh-CN zh-TW`。
- `cases/<category>.md` 与 `cases/<category>_<locale>.md` —— 分类归档页，类别：`ecommerce ad-creative portrait poster character ui comparison`。
- `data/ingested_tweets.json` —— 来源 URL 登记表（`{"records": [...]}`），用于去重和溯源。
- `docs/update-log.md` —— 每批发布与维护变更的记录。
- `images/<category>_case<N>/` —— 媒体文件。

## 铁律（不可违反）

1. **不编造。** prompt 文本、作者、来源 URL、日期、模型声明、效果，一律逐字取自公开来源或所有者提供的材料。缺什么就标缺，不补写。
2. **编号命名空间。** 英文 README 的显示顺序就是权威顺序：`Case 1` 到 `Case N` 按出现顺序全局唯一、连续、不跳号（当前 N = 462，写死在 `scripts/verify_prompt_repo.py` 的 `EXPECTED_CASE_COUNT`）。本地化文件保持同样的顺序和编号。因为编号跟着显示顺序走，**插入到中间分类的新案例会让其后所有编号后移**：必须在 11 个 README 的标题与 `<!-- Case N -->` 注释、对应 `cases/*.md` 条目、登记表的 `case_anchor` 里一起重编号，并同步更新 `EXPECTED_CASE_COUNT`。重编号用脚本做，不手改；动手前先向所有者确认。
3. **英文先行。** 先改 `README.md`，过了英文验证门，再动本地化文件。
4. **十国同步。** 可见结构或公开文案变了，10 个本地化 README 和对应 `cases/*_<locale>.md` 必须一起更新，并且是真翻译。prompt 代码块、URL、模型 ID、命令、环境变量一字不改。不得留下 TODO、待翻译标记或未翻译的脚手架。
5. **去重。** 来源 URL 是去重键；已在 `data/ingested_tweets.json` 里的，不得再收。新收的案例要在登记表里补记录。
6. **准入门槛。** 只有语义审查结论为 selected / high confidence、且具备来源 URL、作者、完整 prompt、类别、标题、媒体形态决定、可验证媒体的候选，才能进入公开区。deferred / unsure / dropped / duplicate / showcase-only 一律不进。
7. **结构不动。** README 顺序固定：Introduction → Quick Start → What is GPT Image 2 → News → Menu → 各分类 → How to Contribute → Related Repositories → Acknowledge，各节的 `<a id="...">` 锚点不改。保持现有的 case 形态（`<!-- Case N: ... -->` 注释 + `### Case N: [标题](来源) (by [@作者](主页))` + Output 表格 + `**Prompt:**` + 无语言标注的代码块）。分类节首的 `> **K curated cases**` 计数要跟着改。本地化 README 里案例标题保持英文原样。
8. **媒体规则。** 图片要有描述性 alt；不得把原始视频作为可见媒体（用海报帧链接到可播放视频）；不得新增超过 25 MB 的文件；公开媒体按仓库约定迁移到 R2，例外要记录。
9. **仓库边界。** 这里只放 prompt 和指南内容，只*链接*相关的 API / Skill 仓库。改动可运行的 API 或 Skill 发布材料，需要单独批准的范围和兄弟 agent 审计。
10. **不提交本地产物。** `.codex/`、`tmp/`、`result/`、`AGENTS.md`、`.env`、`.skill/` 等已在 `.gitignore`；候选队列、语义审查记录、审计证据都不是公开内容。不提交密钥或私人导出。
11. **记账。** 每次发布批次或维护变更，在 `docs/update-log.md` 加一条。
12. **验证通过才提交。** 提交前必须全部通过下面的验证命令（`.claude/settings.json` 里的 hook 会在 `git commit` 前自动跑验证器，失败会拦截）。

## 验证命令

```bash
python3 scripts/verify_prompt_repo.py
python3 -m json.tool data/ingested_tweets.json >/dev/null
git diff --check
find . \( -name .DS_Store -o -name __pycache__ -o -name '*.pyc' \) -print   # 应无输出
```

验证器的范围比完整发布门窄。正式发布还需要：模板审计、公开链接与 UTM 审计、本地化语义审查、媒体与 R2 证据、GitHub 渲染检查，见 `docs/maintenance.md`。

## 工作习惯

- 开工前先看当前分支、远端、工作区是否干净；有无关改动时用独立 worktree。
- 文件很大（每个 README 约 1.1 MB）：用 `grep -n` 定位、按行号读片段，不要整文件读入。
- `script/sync_multilingual_readmes.py` 会从英文 README 重新生成所有本地化 README（默认保留人工维护的 News/Menu）。只有所有者明确要求时才运行，运行后逐个检查 `git diff`；绝不加 `--rewrite-protected-sections`，除非所有者点名要求。
- 提交信息沿用历史风格，例如 `Add June 30 GPT Image 2 prompt batch`、`docs: ...`。

## 项目 Skills（`.claude/skills/`）

| Skill | 用途 |
|---|---|
| `add-prompt-cases` | 收录一批新的 prompt 案例：去重 → 编号 → 改英文 README / cases / 登记表 / 更新日志 → 验证 → 本地化 |
| `sync-localized-readmes` | 让 10 个本地化 README 和 cases 页与英文源对齐，并检查一致性 |
| `impeccable` | 第三方前端设计技能（Apache-2.0，pbakaus/impeccable）。只在做网页 / UI 时用，与本仓库的 Markdown 内容维护无关 |
| `ui-ux-pro-max` | 第三方 UI/UX 设计知识库（MIT，nextlevelbuilder/ui-ux-pro-max-skill）。同上，只用于 UI 工作 |

第三方 skill 的来源版本和改动记录见 `.claude/VENDORED.md`。
