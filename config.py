"""Agentic Honeypot Configuration"""
import os
from dataclasses import dataclass

@dataclass
class Config:
    # Network settings
    HOST = "0.0.0.0"
    SSH_PORT = 2222
    HTTP_PORT = 8080
    FTP_PORT = 2121
    TELNET_PORT = 2323
    
    # Honeypot services
    FAKE_SERVICES = {
        'ssh': {'version': 'OpenSSH_7.4p1 Ubuntu-10ubuntu0.2'},
        'http': {'server': 'Apache/2.4.29 (Ubuntu)'},
        'ftp': {'server': 'vsftpd 3.0.3'}
    }
    
    # AI Agent settings
    ANALYSIS_THRESHOLD = 0.7
    AUTO_BAN_THRESHOLD = 0.9
    MAX_CONNECTIONS = 100
    
    # Database
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_USER = "honeypot"
    DB_PASS = "securepass123"
    DB_NAME = "honeypot_db"
    
    # Response actions
    ENABLE_RATE_LIMIT = True
    ENABLE_DECEPTION = True
    ENABLE_COUNTER_TRACK = True
