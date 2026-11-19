from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from study_assistant import ask_gemini


def process_question(payload, answer=ask_gemini):
    if not isinstance(payload, dict) or not isinstance(payload.get("question"), str) or not payload["question"].strip():
        return 400, {"success": False, "message": "Please enter a study question."}
    question = payload["question"].strip()
    if len(question) > 8000:
        return 400, {"success": False, "message": "Question is too long."}
    try:
        success, message = answer(question)
    except Exception:
        success, message = False, "AI service is unavailable. Please try again later."
    return (200 if success else 503), {"success": success, "message": message}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", os.getenv("ALLOWED_ORIGIN", "http://localhost:8080"))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", os.getenv("ALLOWED_ORIGIN", "http://localhost:8080"))
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/ask":
            return self.send_json(404, {"success": False, "message": "Endpoint not found."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 65536:
                raise ValueError()
            payload = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeError):
            return self.send_json(400, {"success": False, "message": "Invalid request."})
        status, result = process_question(payload)
        self.send_json(status, result)


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    ThreadingHTTPServer((host, int(os.getenv("PORT", "8000"))), Handler).serve_forever()
