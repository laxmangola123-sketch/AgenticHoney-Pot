import aiosqlite
from loguru import logger

class Database:
    def __init__(self):
        self.db_path = "honeypot.db"

    async def connect(self):
        try:
            # Localhost ki jagah file based database use hoga
            self.conn = await aiosqlite.connect(self.db_path)
            logger.info(f"✅ SQLite Database connected: {self.db_path}")
            
            # Logs store karne ke liye table
            await self.conn.execute("""
                CREATE TABLE IF NOT EXISTS honeypot_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT,
                    ip_address TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await self.conn.commit()
        except Exception as e:
            logger.error(f"❌ Database Connection Error: {e}")

db = Database()

