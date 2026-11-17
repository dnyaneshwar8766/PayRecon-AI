"""Small SQLite persistence layer for reconciliation run history."""
from __future__ import annotations
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("PAYRECON_DB_PATH", Path(__file__).resolve().parents[1] / "payrecon.db"))

def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize():
    with _connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS reconciliation_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            source TEXT NOT NULL,
            summary_json TEXT NOT NULL,
            result_json TEXT NOT NULL
        )""")

def save_run(result: dict[str, Any], source: str = "manual") -> dict[str, Any]:
    created_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO reconciliation_runs(created_at, source, summary_json, result_json) VALUES (?, ?, ?, ?)",
            (created_at, source, json.dumps(result.get("summary", {})), json.dumps(result)),
        )
        run_id = cur.lastrowid
    return {"id": run_id, "created_at": created_at, "source": source, "summary": result.get("summary", {})}

def list_runs(limit: int = 20):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, created_at, source, summary_json FROM reconciliation_runs ORDER BY id DESC LIMIT ?",
            (max(1, min(limit, 100)),),
        ).fetchall()
    return [{"id": r["id"], "created_at": r["created_at"], "source": r["source"], "summary": json.loads(r["summary_json"])} for r in rows]

def get_run(run_id: int):
    with _connect() as conn:
        row = conn.execute("SELECT result_json FROM reconciliation_runs WHERE id = ?", (run_id,)).fetchone()
    return json.loads(row["result_json"]) if row else None
