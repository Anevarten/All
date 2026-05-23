"""
SQLite database layer.
DB file lives at: natures-slumber/data/store.db
Tables: orders, order_items, ratings
"""
import sqlite3
from pathlib import Path
from datetime import datetime

import os
# On Render the persistent disk is mounted at /data; locally use project/data/
_data_dir = Path("/data") if os.path.isdir("/data") else Path(__file__).parent / "data"
DB_PATH = _data_dir / "store.db"


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS orders (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ref         TEXT    NOT NULL UNIQUE,
                name        TEXT    NOT NULL,
                email       TEXT    NOT NULL,
                phone       TEXT    NOT NULL,
                address     TEXT    NOT NULL,
                city        TEXT    NOT NULL,
                pincode     TEXT    NOT NULL,
                notes       TEXT,
                total       INTEGER NOT NULL,
                status      TEXT    NOT NULL DEFAULT 'pending',
                created_at  TEXT    NOT NULL
            );
            CREATE TABLE IF NOT EXISTS order_items (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id  INTEGER NOT NULL REFERENCES orders(id),
                slug      TEXT    NOT NULL,
                name      TEXT    NOT NULL,
                price     INTEGER NOT NULL,
                qty       INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS ratings (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                slug       TEXT    NOT NULL,
                stars      INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5),
                review     TEXT,
                created_at TEXT    NOT NULL
            );
        """)


# ── Orders ────────────────────────────────────────────────────────────────────

def create_order(data: dict, items: list[dict]) -> str:
    """Insert order + items, return order ref."""
    ref = f"NS-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{data['name'][:3].upper()}"
    total = sum(i["price"] * i["qty"] for i in items)
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO orders (ref, name, email, phone, address, city, pincode, notes, total, status, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (ref, data["name"], data["email"], data["phone"],
             data["address"], data["city"], data["pincode"],
             data.get("notes", ""), total, "pending",
             datetime.utcnow().isoformat()),
        )
        oid = cur.lastrowid
        conn.executemany(
            "INSERT INTO order_items (order_id, slug, name, price, qty) VALUES (?,?,?,?,?)",
            [(oid, i["slug"], i["name"], i["price"], i["qty"]) for i in items],
        )
    return ref


def get_order(ref: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM orders WHERE ref=?", (ref,)).fetchone()
        if not row:
            return None
        items = conn.execute(
            "SELECT * FROM order_items WHERE order_id=?", (row["id"],)
        ).fetchall()
        return {"order": dict(row), "items": [dict(i) for i in items]}


def list_orders(status: str | None = None) -> list[dict]:
    with get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM orders WHERE status=? ORDER BY id DESC", (status,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        return [dict(r) for r in rows]


def update_order_status(ref: str, status: str) -> None:
    with get_conn() as conn:
        conn.execute("UPDATE orders SET status=? WHERE ref=?", (status, ref))


# ── Ratings ───────────────────────────────────────────────────────────────────

def add_rating(slug: str, stars: int, review: str = "") -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO ratings (slug, stars, review, created_at) VALUES (?,?,?,?)",
            (slug, stars, review, datetime.utcnow().isoformat()),
        )


def get_ratings(slug: str) -> dict:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT stars, review, created_at FROM ratings WHERE slug=? ORDER BY id DESC",
            (slug,),
        ).fetchall()
    if not rows:
        return {"avg": 0, "count": 0, "reviews": []}
    avg = sum(r["stars"] for r in rows) / len(rows)
    return {
        "avg": round(avg, 1),
        "count": len(rows),
        "reviews": [dict(r) for r in rows[:10]],
    }
