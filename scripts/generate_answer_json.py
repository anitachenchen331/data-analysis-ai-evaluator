#!/usr/bin/env python3
"""执行标准 SQL 并生成答案 JSON。"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


READONLY_SQL_RE = re.compile(r"^\s*(select|with)\b", re.IGNORECASE)


def import_duckdb():
    try:
        import duckdb  # type: ignore
    except ModuleNotFoundError as exc:
        raise SystemExit("未安装 duckdb。请在可用环境中安装后重试。") from exc
    return duckdb


def main() -> int:
    parser = argparse.ArgumentParser(description="用标准 SQL 自动生成答案 JSON。")
    parser.add_argument("--database", required=True, help="DuckDB 数据库路径")
    parser.add_argument("--sql-dir", required=True, help="标准 SQL 目录")
    parser.add_argument("--output-dir", required=True, help="答案 JSON 输出目录")
    parser.add_argument(
        "--allow-write-sql",
        action="store_true",
        help="允许执行非 SELECT/WITH 开头的 SQL，并以非只读模式连接数据库。",
    )
    args = parser.parse_args()

    duckdb = import_duckdb()
    sql_dir = pathlib.Path(args.sql_dir).resolve()
    output_dir = pathlib.Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(args.database, read_only=not args.allow_write_sql)
    for sql_file in sorted(sql_dir.glob("*.sql")):
        sql = sql_file.read_text(encoding="utf-8")
        if not args.allow_write_sql and not READONLY_SQL_RE.match(sql):
            print(f"跳过非只读 SQL：{sql_file}", file=sys.stderr)
            continue
        result = con.execute(sql)
        columns = [col[0] for col in result.description]
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
        payload = {
            "task_id": sql_file.stem,
            "sql_file": sql_file.relative_to(sql_dir).as_posix(),
            "row_count": len(rows),
            "columns": columns,
            "rows": rows,
        }
        out = output_dir / f"{sql_file.stem}.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print(f"已生成：{out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
