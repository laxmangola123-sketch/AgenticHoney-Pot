"""Multi-protocol Honeypot Server"""
import socket
import threading
import asyncio
from loguru import logger
from faker import Faker
from config import Config
from database import db

fake = Faker()

class HoneypotServer:
    def __init__(self):
        self.active_connections = {}
    
    async def ssh_honeypot(self):
        """Fake SSH server"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', Config.SSH_PORT))
        sock.listen(5)
        logger.info(f"🐝 SSH Honeypot listening on port {Config.SSH_PORT}")
        
        while True:
            client, addr = await asyncio.get_event_loop().sock_accept(sock)
            asyncio.create_task(self.handle_ssh(client, addr))
    
    async def handle_ssh(self, client, addr):
        ip = addr[0]
        await db.log_connection(ip, Config.SSH_PORT, 'ssh')
        
        # Send fake banner
        banner = f"SSH-2.0-{Config.FAKE_SERVICES['ssh']['version']}\r\n".encode()
        client.send(banner)
        
        try:
            while True:
                data = client.recv(1024)
                if not data:
                    break
                
                # Log credentials attempts
                if b'username:' in data.lower() or b'password:' in data.lower():
                    await db.log_attack(ip, 'ssh_bruteforce', data.decode())
                
                # Send deceptive responses
                response = self.generate_ssh_response(data.decode())
                client.send(response.encode())
                
        except:
            pass
        finally:
            client.close()
    
    def generate_ssh_response(self, data):
        responses = [
            "Permission denied (publickey,password).",
            "Last login: {} from {}".format(fake.date_time().strftime('%c'), fake.ipv4()),
            "$ "
        ]
        return fake.random_element(responses)
    
    async def http_honeypot(self):
        """Fake HTTP server"""
        from http.server import HTTPServer, BaseHTTPRequestHandler
        class HoneyHandler(BaseHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.ip = None
                super().__init__(*args, **kwargs)
            
            def log_request(self, code='-', size='-'):
                pass
            
            def do_GET(self):
                self.ip = self.client_address[0]
                asyncio.create_task(db.log_connection(self.ip, Config.HTTP_PORT, 'http'))
                
                # Fake vulnerable web app
                self.send_response(200)
                self.send_header('Server', Config.FAKE_SERVICES['http']['server'])
                self.end_headers()
                self.wfile.write(b"""
                <html><body>
                <h1>Fake Admin Panel</h1>
                <form method="POST">
                Username: <input name="user"><br>
                Password: <input name="pass" type="password"><br>
                <input type="submit">
                </form>
                </body></html>
                """)
            
            def do_POST(self):
                asyncio.create_task(db.log_attack(self.ip, 'http_form', self.path))
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.end_headers()
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', Config.HTTP_PORT))
        httpd = HTTPServer(('', Config.HTTP_PORT), HoneyHandler)
        logger.info(f"🌐 HTTP Honeypot listening on port {Config.HTTP_PORT}")
        httpd.serve_forever()

honeypot = HoneypotServer()
