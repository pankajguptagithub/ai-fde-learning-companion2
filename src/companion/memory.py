import sqlite3
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "companion.db"


def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True,exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS attempts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                score REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

def save_attempt(
    user_id: str,
    topic: str,
    score: float,
) -> None:

    if not 0 <= score <= 1:
        raise ValueError("score must be between 0 and 1")


    initialize_database()

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO attempts(
                user_id,
                topic,
                score,
                created_at
            )
            VALUES (?,?,?,?)
            """,
            (
                user_id,
                topic,
                score,
                datetime.now().isoformat(),
            ),
        )

def get_attempts(
    user_id: str,
    topic: str,
) -> list[dict]:
    initialize_database()

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT
                id,
                user_id,
                topic,
                score,
                created_at
            FROM attempts
            WHERE user_id = ?
                AND topic = ?
            ORDER BY id
            """,
            (
                user_id,
                topic,
            ),
        ).fetchall()

    return [dict(row) for row in rows]

