#!/usr/bin/env python3
"""生成评分工作表草稿，供评分 agent 或人工复核填写。"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


TASK_RE = re.compile(r"^###\s+`?([A-Za-z][A-Za-z0-9_.-]*)`?(?:\s+.*)?$", re.MULTILINE)


def extract_tasks(result_file: pathlib.Path) -> list[str]:
    text = result_file.read_text(encoding="utf-8")
    tasks = []
    for match in TASK_RE.finditer(text):
        task_id = match.group(1).strip()
        if task_id.lower() not in {"notes", "summary", "evidence", "errors"}:
            tasks.append(task_id)
    return tasks


def main() -> int:
    parser = argparse.ArgumentParser(description="根据实验结果生成评分工作表草稿。")
    parser.add_argument("--results", nargs="+", required=True, help="实验组结果 Markdown")
    parser.add_argument("--output", required=True, help="评分工作表输出路径")
    args = parser.parse_args()

    result_files = [pathlib.Path(p) for p in args.results]
    lines = ["# 评分工作表", ""]
    lines.append("| 任务编号 | 结果文件 | 可执行或可交付 | 结果准确 | 口径正确 | 分析解释 | 可追溯稳健 | 总分 | 扣分原因 |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---|")

    for result_file in result_files:
        for task_id in extract_tasks(result_file):
            lines.append(f"| {task_id} | {result_file} |  |  |  |  |  |  |  |")

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已生成评分工作表草稿：{output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
