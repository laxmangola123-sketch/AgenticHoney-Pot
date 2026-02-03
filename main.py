import asyncio
import sys
from loguru import logger
from honeypot_server import honeypot
from agent_controller import agent
from database import db

async def main():
    logger.info("🚀 Starting Agentic Honeypot System")
    await db.connect()
    
    tasks = [
        asyncio.create_task(honeypot.ssh_honeypot()),
        asyncio.create_task(agent.monitor()),
    ]
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Stopped")
        sys.exit(0)
