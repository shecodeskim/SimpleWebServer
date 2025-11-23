# run_server.py
import http.server
import socketserver
import os
import sys
from functools import partial

PORT = 8000

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    # override log to reduce console noise
    def log_message(self, format, *args):
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format%args))

if __name__ == "__main__":
    # serve from the directory where this script lives
    web_dir = os.path.join(os.path.dirname(__file__))
    os.chdir(web_dir)
    handler = QuietHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server")
            httpd.server_close()
            sys.exit(0)
