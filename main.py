"""Agentic Honeypot Main Orchestrator"""
import asyncio
import signal
import sys
from loguru import logger
from honeypot_server import honeypot, HoneypotServer
from agent_controller import agent
from database import db
from config import Config

async def main():
    logger.info("🚀 Starting Agentic Honeypot System")
    
    # Initialize database
    await db.connect()
    
    # Start honeypot services
    tasks = [
        asyncio.create_task(honeypot.ssh_honeypot()),
        asyncio.create_task(agent.monitor()),
    ]
    
    # Graceful shutdown
    def shutdown():
        logger.info("🛑 Shutting down honeypot...")
        for task in tasks:
            task.cancel()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, lambda s, f: shutdown())
    signal.signal(signal.SIGTERM, lambda s, f: shutdown())
    
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())
