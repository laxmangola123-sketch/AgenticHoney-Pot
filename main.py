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
    
    # Start tasks
    tasks = [
        asyncio.create_task(honeypot.ssh_honeypot()),
        asyncio.create_task(agent.monitor()),
    ]
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Honeypot stopped by user")
        sys.exit(0)



