# run_server.py
import http.server
import socketserver
import os
import sys

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "public")

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Allow local JS fetch if you later add API endpoints
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

if __name__ == "__main__":
    os.chdir(WEB_DIR)
    handler = CORSRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving HTTP on http://localhost:{PORT} (serving {WEB_DIR})")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server")
            httpd.server_close()
            sys.exit(0)
