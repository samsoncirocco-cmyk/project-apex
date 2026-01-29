#!/usr/bin/env python3
import os
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from queue import Queue, Empty


DEFAULT_DB_PATH = "/data/apex.db"
DEFAULT_POOL_SIZE = 10
MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def _resolve_db_path(db_path: str) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(db_path))
    return Path(expanded)


def _ensure_parent_dir(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)


def _apply_pragmas(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA wal_autocheckpoint=1000;")


def _init_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            applied_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def _applied_migrations(conn: sqlite3.Connection) -> set[str]:
    _init_schema(conn)
    rows = conn.execute("SELECT name FROM migrations").fetchall()
    return {row[0] for row in rows}


def _apply_migration(conn: sqlite3.Connection, name: str, sql: str) -> None:
    conn.executescript(sql)
    conn.execute("INSERT INTO migrations (name) VALUES (?)", (name,))


def apply_migrations(conn: sqlite3.Connection, migrations_dir: Path = MIGRATIONS_DIR) -> None:
    if not migrations_dir.exists():
        return

    applied = _applied_migrations(conn)
    migration_files = sorted(migrations_dir.glob("*.sql"))
    for path in migration_files:
        name = path.name
        if name in applied:
            continue
        sql = path.read_text(encoding="utf-8")
        _apply_migration(conn, name, sql)


class SQLiteConnectionPool:
    def __init__(
        self,
        db_path: str | Path,
        max_connections: int = DEFAULT_POOL_SIZE,
        timeout: float = 30.0,
    ) -> None:
        self.db_path = _resolve_db_path(str(db_path))
        self.max_connections = max_connections
        self.timeout = timeout
        self._pool: Queue[sqlite3.Connection] = Queue(max_connections)
        self._created = 0
        self._lock = threading.Lock()
        _ensure_parent_dir(self.db_path)

        conn = self._create_connection()
        try:
            _apply_pragmas(conn)
            apply_migrations(conn)
            conn.commit()
        finally:
            self._pool.put(conn)
            self._created = 1

    def _create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=self.timeout,
            check_same_thread=False,
        )
        conn.row_factory = sqlite3.Row
        _apply_pragmas(conn)
        return conn

    @contextmanager
    def connection(self) -> sqlite3.Connection:
        conn = self.acquire()
        try:
            yield conn
        finally:
            self.release(conn)

    def acquire(self) -> sqlite3.Connection:
        try:
            return self._pool.get_nowait()
        except Empty:
            with self._lock:
                if self._created < self.max_connections:
                    conn = self._create_connection()
                    self._created += 1
                    return conn
        return self._pool.get()

    def release(self, conn: sqlite3.Connection) -> None:
        self._pool.put(conn)

    def execute(self, sql: str, params: tuple | None = None) -> None:
        params = params or ()
        with self.connection() as conn:
            conn.execute(sql, params)
            conn.commit()

    def query(self, sql: str, params: tuple | None = None) -> list[sqlite3.Row]:
        params = params or ()
        with self.connection() as conn:
            cursor = conn.execute(sql, params)
            return cursor.fetchall()

    def mark_conversation_history_for_deletion(self, days: int = 90) -> int:
        sql = """
            UPDATE conversation_history
            SET marked_for_deletion_at = CURRENT_TIMESTAMP
            WHERE created_at < datetime('now', ?)
              AND marked_for_deletion_at IS NULL
        """
        cutoff = f"-{days} days"
        with self.connection() as conn:
            cursor = conn.execute(sql, (cutoff,))
            conn.commit()
            return cursor.rowcount

    def checkpoint(self, mode: str = "PASSIVE") -> tuple[int, int, int]:
        allowed = {"PASSIVE", "FULL", "RESTART", "TRUNCATE"}
        mode = mode.upper()
        if mode not in allowed:
            raise ValueError(f"Unsupported checkpoint mode: {mode}")
        sql = f"PRAGMA wal_checkpoint({mode});"
        with self.connection() as conn:
            row = conn.execute(sql).fetchone()
            return tuple(row)


def init_pool(
    db_path: str | Path | None = None,
    max_connections: int = DEFAULT_POOL_SIZE,
) -> SQLiteConnectionPool:
    db_path = db_path or os.getenv("DATABASE_PATH", DEFAULT_DB_PATH)
    return SQLiteConnectionPool(db_path=db_path, max_connections=max_connections)


if __name__ == "__main__":
    pool = init_pool()
    with pool.connection() as conn:
        mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
    print(f"[db_manager] SQLite ready at {pool.db_path}")
    print(f"[db_manager] journal_mode={mode}")
