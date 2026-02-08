"""
Database module for quiz bot.
Stores leads in SQLite database.
"""
import os
import aiosqlite
from typing import List, Optional
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "data/database.sqlite3")


async def init_db() -> None:
    """Initialize database and create tables if not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                answers TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_lead(
    user_id: int,
    username: Optional[str],
    answers: List[str]
) -> int:
    """
    Save lead answers to database.
    
    Args:
        user_id: Telegram user ID
        username: Telegram username
        answers: List of quiz answers
    
    Returns:
        ID of created lead record
    """
    answers_text = "|||".join(answers)
    created_at = datetime.now().isoformat()
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            INSERT INTO leads (user_id, username, answers, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, username, answers_text, created_at)
        )
        await db.commit()
        return cursor.lastrowid


async def get_leads_count() -> int:
    """Get total number of leads."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM leads")
        row = await cursor.fetchone()
        return row[0] if row else 0
