#!/usr/bin/env python3
import argparse
import os
import sqlite3
import sys
from pathlib import Path


def resolve_db_path(raw_path: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(raw_path))
    return Path(expanded)


def ensure_parent_dir(db_path: Path) -> None:
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise OSError(
            f"Failed to create directory '{db_path.parent}'. "
            "Set DATABASE_PATH to a writable location."
        ) from exc


def init_db(db_path: Path) -> str:
    ensure_parent_dir(db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.execute("PRAGMA journal_mode=WAL;")
        mode = cursor.fetchone()[0]
        if str(mode).lower() != "wal":
            raise RuntimeError(f"Expected WAL mode, got '{mode}'")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS apex_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "INSERT OR IGNORE INTO apex_meta (key, value) VALUES ('schema_version', '1')"
        )
        conn.commit()
        return mode
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    default_path = os.getenv("DATABASE_PATH", "./data/apex.db")
    parser = argparse.ArgumentParser(
        description="Initialize the Project Apex SQLite database with WAL mode."
    )
    parser.add_argument(
        "--db-path",
        default=default_path,
        help="Path to SQLite database (default: DATABASE_PATH or ./data/apex.db)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = resolve_db_path(args.db_path)
    try:
        mode = init_db(db_path)
    except Exception as exc:
        print(f"[init_db] ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"[init_db] SQLite initialized at {db_path}")
    print(f"[init_db] journal_mode={mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
