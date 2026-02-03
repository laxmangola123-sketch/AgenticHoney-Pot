import asyncio
import sys
from flask import Flask, jsonify
import threading
from loguru import logger
from honeypot_server import honeypot
from agent_controller import agent
from database import db

# 1. Dummy API for Render & Tester
app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({"status": "running", "message": "Agentic Honeypot is Active"}), 200

def run_web_server():
    # Render hamesha port 10000 mangta hai
    app.run(host='0.0.0.0', port=10000)

async def main():
    logger.info("🚀 Starting Agentic Honeypot System")
    await db.connect()
    
    # 2. Start Web Server in a separate thread
    threading.Thread(target=run_web_server, daemon=True).start()
    
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
