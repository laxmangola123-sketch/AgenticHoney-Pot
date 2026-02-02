"""Honeypot Database Layer"""
import asyncio
import aiomysql
from datetime import datetime
from loguru import logger
from config import Config

class HoneypotDB:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=Config.DB_HOST, port=Config.DB_PORT,
            user=Config.DB_USER, password=Config.DB_PASS,
            db=Config.DB_NAME, autocommit=True
        )
    
    async def log_connection(self, ip, port, protocol, username=None, password=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO connections (ip, port, protocol, username, password, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (ip, port, protocol, username, password, datetime.now()))
    
    async def log_attack(self, ip, attack_type, payload, severity=1):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO attacks (ip, attack_type, payload, severity, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (ip, attack_type, payload, severity, datetime.now()))
    
    async def get_ip_stats(self, ip):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT COUNT(*), AVG(severity) FROM attacks WHERE ip = %s
                """, (ip,))
                return await cur.fetchone()
    
    async def ban_ip(self, ip, reason):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO banned_ips (ip, reason, banned_at)
                    VALUES (%s, %s, %s)
                """, (ip, reason, datetime.now()))

db = HoneypotDB()
