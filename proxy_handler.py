import os
from dotenv import load_dotenv

# Load variables from a .env file
load_dotenv()

class ProxyManager:
    def __init__(self):
        # These are pulled from your system or a hidden .env file
        self.username = os.getenv("PROXY_USER")
        self.password = os.getenv("PROXY_PASS")
        self.host = os.getenv("PROXY_HOST", "proxy.provider.com:8001")

    def get_proxy_settings(self):
        if not self.username or not self.password:
            return None # Fallback if no proxy is configured
            
        return {
            "server": f"http://{self.host}",
            "username": self.username,
            "password": self.password
        }