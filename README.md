![数据分析 AI 产品评测器概览](docs/skill-overview.png)

# Data Analysis AI Evaluator（数据分析 AI 产品评测器）

这是一个 Codex 技能，用来设计和运行数据分析类 AI 产品评测。它适用于数据问答、SQL 或查询生成、语义层、图表生成、看板生成、异动诊断、归因分析、自动报告、权限治理和完整产品链路评估。

核心方法是：先调研产品公开能力，再由人确认评测目标、实验组、数据场景、问题矩阵和评分体系，最后生成互相隔离的公开题集、内部评分键、标准答案、实验提示词和评分报告。

关键词：数据分析评测、AI 产品评测、数据问答、SQL 生成、查询生成、语义层、指标口径、图表生成、看板生成、异动诊断、归因分析、自动报告、权限治理、评测隔离、人在回路、评分体系、标准答案、评测包。

## 这个技能能做什么

- 在设计评测前，先调研被测产品公开声称支持的数据分析能力。
- 让人确认评测目标、实验组、数据场景、问题矩阵和评分规则。
- 生成分层隔离的公开题集、内部评分键、标准答案、实验提示词、结果模板和最终评分报告。
- 通过公开输入与内部答案材料隔离，降低实验污染风险。
- 只有在人确认后，才把单次评测经验沉淀为通用经验。

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

推荐生成的评测包结构：

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

`questions/common_questions.yaml` 是公开给实验运行组读取的题集。`questions/scoring_key_internal.yaml`、`standard_sql/`、`answers/` 和历史 `results/` 是内部材料，只能在评分阶段读取。

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

## 离线或受限环境

这个技能通常会从产品公开资料开始调研。如果当前环境无法联网、无法访问产品文档、私有看板或账号，就只使用用户提供的材料。没有来源支撑的产品能力要标记为 `待确认`，不要自行推断。

## 评测完整性规则

- 公开题集不能包含标准答案、标准查询、常见错误或评分提示。
- 实验运行组不能读取内部评分键、标准答案、标准查询、历史组输出或最终评分报告。
- 评分阶段可以读取内部材料，但必须在实验输出完成之后。
- 模糊问题应该标记为需要澄清，不要硬给答案。
- 敏感或越权请求应该拒绝，并给出安全替代方案。

## 开源注意事项

发布自己的评测包前，必须移除私有产品文档、凭证、本机绝对路径、专有数据集和不该公开的答案键。

本仓库已经包含常见生成物的 `.gitignore` 规则，但每次公开发布前仍建议检查暂存区：

```bash
git status --short
git diff --cached --stat
git diff --cached
python3 scripts/validate_eval_pack.py examples/minimal_eval_pack
python3 scripts/check_leakage.py examples/minimal_eval_pack/questions/common_questions.yaml
```

不要公开真实评测包，除非你已经删除或重新生成内部答案、标准 SQL、专有数据集、原始模型输出、凭证和本机路径。
