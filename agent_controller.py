"""AI Agent Controller - The Brain"""
import asyncio
import time
from loguru import logger
from config import Config
from database import db
from threat_analyzer import ThreatAnalyzer
from response_engine import ResponseEngine

class AgentController:
    def __init__(self):
        self.analyzer = ThreatAnalyzer()
        self.response = ResponseEngine()
        self.suspicious_ips = {}
    
    async def monitor(self):
        """Continuously monitor and analyze threats"""
        while True:
            await self.analyze_recent_activity()
            await self.execute_responses()
            await asyncio.sleep(30)  # Check every 30 seconds
    
    async def analyze_recent_activity(self):
        """Analyze connections and attacks"""
        # Get recent connections (placeholder - integrate real DB)
        recent_ips = await self.get_suspicious_ips()
        
        for ip, score in recent_ips.items():
            if score > Config.ANALYSIS_THRESHOLD:
                logger.warning(f"🤖 Agent analyzing suspicious IP: {ip} (score: {score:.2f})")
                threat_level = await self.analyzer.assess_threat(ip)
                
                if threat_level > Config.AUTO_BAN_THRESHOLD:
                    await self.response.ban_ip(ip, f"AI-detected threat level: {threat_level}")
    
    async def get_suspicious_ips(self):
        """Get IPs with high activity"""
        # Simulated analysis
        return {
            "192.168.1.100": 0.85,
            "10.0.0.50": 0.92,
            "203.0.113.5": 0.78
        }
    
    async def execute_responses(self):
        """Execute intelligent responses"""
        for ip, action in self.response.pending_actions.items():
            logger.info(f"🎯 Executing response against {ip}: {action}")
            await self.response.apply_action(ip, action)

agent = AgentController()
