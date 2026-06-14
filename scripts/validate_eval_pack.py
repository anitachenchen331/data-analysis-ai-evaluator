#!/usr/bin/env python3
"""检查数据分析 AI 产品评测包的基本结构和泄漏风险。"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


FORBIDDEN_PUBLIC_TOKENS = [
    "expected_logic",
    "expected_sql",
    "answer_path",
    "standard_sql",
    "common_errors",
    "标准答案",
    "标准查询",
    "常见错误",
]

TASK_START_RE = re.compile(r"^\s*-\s+task_id:\s*(.+?)\s*$")
FIELD_RE = re.compile(r"^\s{4}([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")

PUBLIC_TASK_FIELDS = [
    "task_id",
    "category",
    "module_under_test",
    "question",
    "response_mode",
    "expected_artifact_type",
]


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def clean_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def read_tasks(path: pathlib.Path, label: str) -> list[dict[str, str]]:
    tasks: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    saw_tasks = False
    for line in read_text(path).splitlines():
        if line.strip() == "tasks:":
            saw_tasks = True
            continue
        match = TASK_START_RE.match(line)
        if match:
            current = {"task_id": clean_scalar(match.group(1))}
            tasks.append(current)
            continue
        field = FIELD_RE.match(line)
        if current is not None and field:
            current[field.group(1)] = clean_scalar(field.group(2))
    if not saw_tasks:
        raise ValueError(f"{label} 缺少 tasks 列表")
    if not tasks:
        raise ValueError(f"{label} tasks 为空")
    for index, task in enumerate(tasks, start=1):
        if not task.get("task_id"):
            raise ValueError(f"{label} 第 {index} 个 task 缺少 task_id")
    return tasks


def task_ids(tasks: list[dict[str, str]]) -> list[str]:
    return [task["task_id"] for task in tasks]


def duplicate_ids(ids: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for task_id in ids:
        if task_id in seen:
            duplicates.add(task_id)
        seen.add(task_id)
    return sorted(duplicates)


def main() -> int:
    parser = argparse.ArgumentParser(description="检查评测包结构和公开题集泄漏风险。")
    parser.add_argument("eval_dir", help="评测包目录")
    args = parser.parse_args()

    root = pathlib.Path(args.eval_dir)
    errors: list[str] = []

    required_paths = [
        "questions/common_questions.yaml",
        "questions/scoring_key_internal.yaml",
        "scoring_rubric.md",
    ]

    for rel in required_paths:
        if not (root / rel).exists():
            errors.append(f"缺少必要文件：{rel}")

    public_questions = root / "questions/common_questions.yaml"
    if public_questions.exists():
        text = read_text(public_questions)
        for token in FORBIDDEN_PUBLIC_TOKENS:
            if token in text:
                errors.append(f"公开题集疑似泄漏内部字段或答案线索：{token}")
        try:
            public_tasks = read_tasks(public_questions, "公开题集")
            public_ids = task_ids(public_tasks)
            for task_id in duplicate_ids(public_ids):
                errors.append(f"公开题集 task_id 重复：{task_id}")
            for task in public_tasks:
                missing_fields = [field for field in PUBLIC_TASK_FIELDS if field not in task]
                if missing_fields:
                    errors.append(f"公开题集 {task.get('task_id', '<unknown>')} 缺少字段：{', '.join(missing_fields)}")
        except ValueError as exc:
            errors.append(str(exc))

    scoring_key = root / "questions/scoring_key_internal.yaml"
    if public_questions.exists() and scoring_key.exists():
        try:
            public_ids = set(task_ids(read_tasks(public_questions, "公开题集")))
            internal_ids = set(task_ids(read_tasks(scoring_key, "内部评分 key")))
            for task_id in sorted(public_ids - internal_ids):
                errors.append(f"公开题集任务缺少内部评分 key：{task_id}")
            for task_id in sorted(internal_ids - public_ids):
                errors.append(f"内部评分 key 缺少公开题目：{task_id}")
        except ValueError as exc:
            errors.append(str(exc))

    standard_sql = root / "standard_sql"
    answers = root / "answers"
    if standard_sql.exists() and answers.exists():
        sql_ids = {p.stem for p in standard_sql.glob("*.sql")}
        answer_ids = {p.stem for p in answers.glob("*.json")}
        missing_answers = sorted(sql_ids - answer_ids)
        missing_sql = sorted(answer_ids - sql_ids)
        for task_id in missing_answers:
            errors.append(f"标准查询缺少答案 JSON：{task_id}")
        for task_id in missing_sql:
            errors.append(f"答案 JSON 缺少标准查询：{task_id}")

    if errors:
        print("检查未通过：")
        for error in errors:
            print(f"- {error}")
        return 1

    print("检查通过：评测包结构和公开题集未发现明显问题。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
