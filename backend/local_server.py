
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from handler import validate_notification


class NotificationRequestHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json(200, {"message": "CORS preflight accepted"})

    def do_POST(self):
        if self.path != "/notifications":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0 or length > 10000:
                self.send_json(400, {"error": "Invalid request size"})
                return

            raw_body = self.rfile.read(length)
            data = json.loads(raw_body.decode("utf-8"))

            notification, error = validate_notification(data)

            if error:
                self.send_json(400, {"error": error})
                return

            self.send_json(200, {
                "status": "validated",
                "message": "Request validated. No notification was sent.",
                "notification": notification,
            })

        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "Invalid JSON request"})

    def log_message(self, format_string, *args):
        print(f"[Local API] {format_string % args}")


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), NotificationRequestHandler)
    print("CloudNotify local API: http://127.0.0.1:8000")
    print("Press Control+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping CloudNotify local API.")
    finally:
        server.server_close()

