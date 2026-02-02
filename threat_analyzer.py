"""AI Threat Analysis Engine"""
import re
from datetime import datetime, timedelta
from loguru import logger
from database import db

class ThreatAnalyzer:
    def __init__(self):
        self.attack_patterns = {
            'bruteforce': [r'admin', r'root', r'password', r'123456'],
            'sql_injection': [r"select.*from", r"union.*select", r"1=1"],
            'xss': [r"<script>", r"javascript:", r"onerror"],
            'rce': [r";\s*(cat|ls|whoami)", r"\$\(.*?\$?\)", r"\\\|"]
        }
    
    async def assess_threat(self, ip):
        """Calculate threat score for IP"""
        stats = await db.get_ip_stats(ip)
        connection_count, avg_severity = stats
        
        score = 0.0
        
        # Connection frequency
        if connection_count > 50:
            score += 0.3
        
        # Payload analysis
        attack_score = await self.analyze_payloads(ip)
        score += attack_score * 0.5
        
        # Behavioral patterns
        behavior_score = await self.analyze_behavior(ip)
        score += behavior_score * 0.2
        
        logger.info(f"📊 Threat assessment for {ip}: {score:.3f}")
        return min(1.0, score)
    
    async def analyze_payloads(self, ip):
        """Analyze malicious payloads"""
        score = 0.0
        patterns_matched = 0
        
        for pattern_type, regexes in self.attack_patterns.items():
            for regex in regexes:
                # Check recent attacks (simplified)
                if re.search(regex, "sample_payload", re.IGNORECASE):
                    patterns_matched += 1
        
        score = min(1.0, patterns_matched / len(self.attack_patterns))
        return score
    
    async def analyze_behavior(self, ip):
        """Analyze attacker behavior"""
        # Port scanning, timing patterns, etc.
        behaviors = ['rapid_connections', 'port_scanning', 'credential_stuffing']
        return len(behaviors) * 0.1

