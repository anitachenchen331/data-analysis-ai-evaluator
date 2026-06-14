#!/usr/bin/env python3
"""扫描公开文件是否包含内部评分或答案泄漏线索。

安全边界说明本身可能会提到禁止读取的内部路径。本脚本默认忽略
“禁止读取/隔离规则”等边界说明附近的敏感词，避免把安全提示误报成泄漏。
"""

from __future__ import annotations

import argparse
import pathlib
import sys


DEFAULT_TOKENS = [
    "expected_logic",
    "expected_sql",
    "answer_path",
    "standard_sql",
    "answers/",
    "scoring_key_internal",
    "标准答案",
    "标准查询",
    "内部评分",
]

BOUNDARY_MARKERS = [
    "禁止读取",
    "不要读取",
    "不得读取",
    "禁止文件",
    "隔离规则",
    "仅评分阶段",
    "评分阶段才",
    "实验运行组禁止",
    "运行阶段是否提供",
]


def is_boundary_notice(line: str, recent_lines: list[str]) -> bool:
    context = "\n".join(recent_lines + [line])
    return any(marker in context for marker in BOUNDARY_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser(description="检查公开文件是否泄漏内部答案线索。")
    parser.add_argument("paths", nargs="+", help="要扫描的文件或目录")
    parser.add_argument("--token", action="append", default=[], help="额外敏感词")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：安全边界说明中的敏感词也会被报告。",
    )
    args = parser.parse_args()

    tokens = DEFAULT_TOKENS + args.token
    files: list[pathlib.Path] = []
    for raw in args.paths:
        path = pathlib.Path(raw)
        if path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
        elif path.is_file():
            files.append(path)

    hits: list[str] = []
    for path in files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        recent_lines: list[str] = []
        for line_no, line in enumerate(lines, start=1):
            for token in tokens:
                if token in line:
                    if not args.strict and is_boundary_notice(line, recent_lines):
                        continue
                    hits.append(f"{path}:{line_no}: {token}")
            if line.strip():
                recent_lines = (recent_lines + [line])[-4:]

    if hits:
        print("发现可能泄漏：")
        for hit in hits:
            print(f"- {hit}")
        return 1

    print("未发现明显泄漏。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
