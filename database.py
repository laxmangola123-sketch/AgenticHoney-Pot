import aiosqlite
from loguru import logger

class Database:
    def __init__(self):
        self.db_path = "honeypot.db"

    async def connect(self):
        try:
            # Ye line localhost ki jagah file use karegi
            self.conn = await aiosqlite.connect(self.db_path)
            logger.info(f"✅ SQLite Database connected at {self.db_path}")
            
            # Table banane ka logic (agar nahi hai)
            await self.conn.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await self.conn.commit()
        except Exception as e:
            logger.error(f"❌ Database Error: {e}")

db = Database()
