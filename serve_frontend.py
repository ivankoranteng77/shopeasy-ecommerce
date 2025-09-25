#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend files.
This serves the static files and handles CORS for local development.
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse, parse_qs

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def serve_frontend(port=3000):
    """Serve the frontend on the specified port."""
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    if not os.path.exists(frontend_dir):
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return
    
    os.chdir(frontend_dir)
    
    print(f"🌐 Starting frontend server...")
    print(f"📂 Serving files from: {frontend_dir}")
    print(f"🔗 Frontend URL: http://localhost:{port}")
    print(f"🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped by user")
            sys.exit(0)

if __name__ == "__main__":
    port = 3000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid port number. Using default port 3000.")
    
    serve_frontend(port)