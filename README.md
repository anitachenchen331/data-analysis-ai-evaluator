# Data Analysis AI Evaluator（数据分析 AI 产品评测器）

你想知道一个数据分析类 AI 产品到底好不好用吗？

比如它能不能稳定理解业务指标、生成正确 SQL、做出靠谱图表、解释数据异动、遵守权限边界，或者在完整产品链路里从连接数据到生成报告都跑通。这个 Codex 技能就是为这类评测准备的。

它不是简单帮你列一张题目清单，而是帮你把一次评测拆成可复核、可对比、可复用的完整流程：先确认要测什么，再设计公平实验组，然后生成公开题集、内部答案、运行提示词、结果模板和评分报告。

## 适合谁用

- 你正在选型数据分析 AI 产品，想比较两个或多个工具。
- 你在验收一个内部 AI 数据助手，想知道它是否真的能处理业务问题。
- 你在做模型或产品版本复测，想看新版本有没有变好。
- 你要评估 SQL 生成、语义层、图表、看板、异动诊断、归因分析或自动报告能力。
- 你担心评测被答案泄漏、历史结果、人工提示污染，想把实验运行和评分材料隔离。
- 你希望把一次评测沉淀成以后还能复用的题集、评分规则和报告模板。

## 你可以拿它评测什么

| 能力方向 | 可以评测的问题 |
|---|---|
| 数据问答 | 能不能把自然语言问题转成正确的数据分析任务 |
| SQL 或查询生成 | 查询能不能执行，口径、关联、过滤、排序是否正确 |
| 语义层和指标口径 | 是否能识别业务别名、指标版本、分子分母和排除规则 |
| 图表和看板 | 图表类型、字段映射、聚合粒度、布局和可读性是否合理 |
| 异动诊断 | 是否能解释环比、同比变化，并验证候选原因 |
| 归因分析 | 是否能区分相关和因果，避免过度归因 |
| 自动报告 | 是否能结论先行、引用证据、说明限制和建议动作 |
| 权限治理 | 是否能拒绝敏感明细、提示注入和越权请求 |
| 完整产品链路 | 数据连接、上下文构建、查询执行、图表报告和错误修复是否跑通 |

## 它的特色

**先调研产品，再设计评测。**  
如果你只给一个产品名或链接，它会先看公开资料，整理产品声称支持的能力，再让你确认本轮到底测哪些能力，避免凭一句“帮我测一下”就乱出题。

**公开题集和内部答案隔离。**  
实验运行组只能看公开题集和允许材料；内部评分 key、标准 SQL、答案 JSON、历史结果和最终评分报告只在评分阶段读取，减少评测污染。

**人在回路确认关键节点。**  
产品画像、实验组、数据场景、指标口径、问题矩阵、评分体系和经验沉淀都需要人确认。这个设计适合严肃评测，不适合靠猜。

**不绑定行业或产品。**  
它不会默认你在测电商、金融、SaaS 或某个历史案例。每轮评测都围绕当前产品、当前数据、当前目标重新设计。

**结果可复核。**  
它鼓励记录实际读取文件、工具证据、耗时、错误、失败类型和扣分原因，最后不只给总分，还解释为什么赢、为什么输、哪里不能落地。

## 你应该怎么开始

在 Codex 里使用这个技能时，可以直接这样说：

```text
使用 data-analysis-ai-evaluator，帮我评测一个数据分析 AI 产品。
产品是：<产品名称或链接>
我的目的：<选型 / 验收 / 对比 / 复测 / 风险审计 / 产品改进>
我重点关心：<SQL 生成 / 语义层 / 图表 / 看板 / 异动诊断 / 权限治理 / 完整链路>
可用材料：<文档、截图、数据库、样例问题、演示环境等>
```

如果你还没想清楚，也可以更简单：

```text
使用 data-analysis-ai-evaluator，帮我设计一套评测方案。我想测一个能做数据问答和图表生成的 AI 产品，但还不知道题目和评分标准怎么定。
```

## 你需要准备什么

最少准备其中一种：

- 产品名称、官网、文档或 GitHub 仓库。
- 你想评测的能力范围。
- 数据库、脱敏数据、合成数据或数据字典。
- 已有业务问题、历史问答、客户场景或验收标准。
- 被测产品的账号、截图、演示环境或运行方式。

如果资料不完整，技能会把缺口标成 `待确认`，而不是假装知道。

## 一次评测通常会产出什么

推荐产物结构如下：

```text
eval-pack/
├── product_eval_brief.md
├── experiment_and_scoring_plan.md
├── evaluation_blueprint.md
├── questions/
│   ├── common_questions.yaml
│   └── scoring_key_internal.yaml
├── standard_sql/
├── answers/
├── prompts/
├── templates/
├── scoring_rubric.md
└── results/
```

其中：

- `product_eval_brief.md`：产品能力画像和本轮建议评测目标。
- `experiment_and_scoring_plan.md`：实验组、隔离规则和评分方案。
- `evaluation_blueprint.md`：数据场景、指标口径、陷阱设计和问题矩阵。
- `questions/common_questions.yaml`：公开题集，实验运行组可以读取。
- `questions/scoring_key_internal.yaml`：内部评分键，只能评分阶段读取。
- `standard_sql/` 和 `answers/`：标准查询和标准答案。
- `prompts/`：不同实验组的隔离运行提示词。
- `results/final_scoring_report.md`：最终评分报告。

## 辅助脚本

这些脚本是轻量护栏，不是完整自动评分引擎。

```bash
python3 -m pip install -r requirements.txt
python3 scripts/validate_eval_pack.py examples/minimal_eval_pack
python3 scripts/check_leakage.py assets/common_questions.template.yaml assets/group_prompts.template.md
python3 scripts/validate_eval_pack.py path/to/eval-pack
python3 scripts/check_leakage.py path/to/public/file-or-dir
python3 scripts/check_leakage.py --strict path/to/public/file-or-dir
python3 scripts/generate_answer_json.py --database path/to/data.duckdb --sql-dir path/to/standard_sql --output-dir path/to/answers
python3 scripts/score_results.py --results path/to/results/group_a_result.md --output path/to/results/scoring_worksheet.md
```

`generate_answer_json.py` 默认以只读模式打开 DuckDB，并拒绝执行不是 `SELECT` 或 `WITH` 开头的 SQL。只对可信的本地 SQL 和数据库使用它；生成的答案 JSON 可能包含敏感行，通常不应该提交到 Git。

## 目录结构

```text
data-analysis-ai-evaluator/
├── SKILL.md
├── agents/
├── assets/
├── examples/
├── references/
└── scripts/
```
