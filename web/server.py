#!/usr/bin/env python3
"""
HBITS Pricing Suite Web Server
Serves v1 and v2 pricing models with version portal
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Configuration
PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        """Add CORS headers and cache control"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        super().end_headers()

def start_server():
    """Start the web server"""
    # Change to web directory
    web_dir = Path(__file__).parent
    os.chdir(web_dir)

    print(f"""
╔════════════════════════════════════════════════════════════╗
║   HBITS Pricing Suite - Web Server                         ║
║   Version Portal & Documentation                           ║
╚════════════════════════════════════════════════════════════╝

📁 Serving from: {web_dir}

🌐 Web Server Starting...
   URL: http://localhost:{PORT}/

📋 Structure:
   /index.html           ← Version Portal (START HERE)
   /v2/                  ← Version 2.0 (Margin-First)
      ├── index.html
      ├── comparison.html
      ├── pricing-model.md
      └── kbi-analysis.md
   /v1/                  ← Version 1.1 (Legacy)
   /data/                ← Shared Documentation & Data

🔗 Quick Links:
   Version Portal:  http://localhost:{PORT}/
   V2.0 Home:      http://localhost:{PORT}/v2/
   V1.1 Home:      http://localhost:{PORT}/v1/

⏹️  Press Ctrl+C to stop the server
""")

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"✅ Server running at http://localhost:{PORT}/\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n⏹️  Server stopped.")
            sys.exit(0)

if __name__ == '__main__':
    start_server()
