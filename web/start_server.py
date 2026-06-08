#!/usr/bin/env python
"""
HBITS Pricing Suite Web Server
Serves v1 and v2 pricing models with version portal
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    pass

# Change to web directory
web_dir = Path(__file__).parent
os.chdir(web_dir)

print("=" * 60)
print("HBITS Pricing Suite - Web Server")
print("=" * 60)
print("")
print("Serving from:", web_dir)
print("")
print("Web Server Starting...")
print("URL: http://localhost:{}".format(PORT))
print("")
print("Structure:")
print("  /index.html           - Version Portal (START HERE)")
print("  /v2/                  - Version 2.0 (Margin-First)")
print("  /v1/                  - Version 1.1 (Legacy)")
print("  /data/                - Documentation & Data")
print("")
print("Quick Links:")
print("  Portal: http://localhost:{}/".format(PORT))
print("  V2.0:   http://localhost:{}/v2/".format(PORT))
print("  V1.1:   http://localhost:{}/v1/".format(PORT))
print("")
print("Press Ctrl+C to stop the server")
print("=" * 60)

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Server running at http://localhost:{}/".format(PORT))
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
