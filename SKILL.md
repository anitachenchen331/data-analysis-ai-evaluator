---
name: data-analysis-ai-evaluator
description: 设计和运行数据分析类 AI 产品评测，适用于数据问答、查询生成、语义层工具、图表生成、看板生成、异动诊断、归因分析、自动报告、权限治理和完整产品链路评估。使用时先根据用户提供的产品名称或链接调研公开产品能力，再通过人在回路确认评测目标、实验组、数据场景、问题矩阵、评分体系，随后生成评测资产、隔离实验提示词、标准答案和评分报告，并在用户确认后沉淀通用经验。
---

# 数据分析 AI 产品评测器

## 核心原则

先调研产品公开能力，再设计评测。不要直接根据用户一句话假设产品能力；如果用户只给产品名或链接，先读取官方资料、代码仓库、文档、示例或其他公开信息，整理能力主张、证据来源和可信度，再让用户确认本轮真正要评测的能力与实验目的。

保持评测隔离。公开题集不能包含标准答案、标准查询、常见错误或评分提示；实验运行组不能读取内部评分键、标准答案、历史结果或其他实验组输出；评分阶段才读取内部答案材料。

保持通用。不要把任一行业、任一产品或任一历史案例写成默认前提。每轮评测的数据场景、指标口径、问题矩阵、实验组和评分权重都必须围绕当轮已确认的产品能力和用户目标定制。

必须人在回路。凡是不确认就可能导致后续整体方向错误的节点，都要停下来让用户确认。具体确认节点见 `references/human_in_loop_gates.md`。

## 工作流

1. **产品调研与目标确认**：读取 `references/product_research.md`，生成产品能力画像，附来源与可信度，让用户确认评测目标。
2. **实验组设计**：读取 `references/experiment_group_design.md`，按实验目的动态推荐最小可行且最有解释力的实验组。
3. **评测蓝图设计**：读取 `references/evaluation_blueprint.md` 和 `references/question_matrix_design.md`，合并设计数据场景、指标口径、问题矩阵，并让用户确认。
4. **评测资产生成**：使用 `assets/` 下模板生成公开题集、内部评分键、实验提示词、统一结果模板和评分规则。
5. **实验运行与记录**：按 `references/result_report_spec.md` 记录每组输出、工具证据、耗时、错误和实际读取文件。
6. **评分与结论**：读取 `references/scoring_system.md`，用内部评分键、标准答案和结果文件生成最终评分报告。
7. **经验沉淀**：读取 `references/learning_capture.md`，先生成候选经验清单，经用户确认后再写回技能或项目资产。

完整流程说明见 `references/workflow.md`。

## 必须优先确认的事项

在继续生成资产前，至少确认：

- 被测产品名称和版本。
- 本轮要评测的产品能力。
- 本轮实验目的：选型、验收、对比、复测、风险审计或产品改进。
- 数据场景和数据来源：真实数据、脱敏数据或合成数据。
- 实验组数量与隔离规则。
- 评分维度和权重。

如果用户要求直接执行，但上述关键信息尚未确认，先输出当前已知信息和待确认项。

## 推荐输出结构

每轮评测建议生成：

- `product_eval_brief.md`
- `experiment_and_scoring_plan.md`
- `evaluation_blueprint.md`
- `questions/common_questions.yaml`
- `questions/scoring_key_internal.yaml`
- `standard_sql/` 或其他标准校验文件
- `answers/`
- `prompts/group_prompts.md`
- `templates/group_result_template.md`
- `scoring_rubric.md`
- `results/final_scoring_report.md`

实际文件名可按用户项目调整，但公开输入、内部答案、实验输出和评分报告必须分层隔离。

## 可用脚本

- `scripts/validate_eval_pack.py`：检查评测包结构、题集泄漏风险和模板覆盖情况。
- `scripts/generate_answer_json.py`：用标准 SQL 和数据库自动生成答案 JSON。
- `scripts/check_leakage.py`：扫描公开题集、实验提示词或结果文件中是否泄漏内部答案线索。
- `scripts/score_results.py`：根据评分配置和结果文件生成评分工作表草稿。

脚本是辅助工具，不替代人工确认。遇到标准答案争议、工具降级或实验目标变化时，必须先暂停并让用户确认。
