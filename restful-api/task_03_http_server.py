#!/usr/bin/python3
"""Serve a small JSON API using Python's standard HTTP server."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleAPIHandler(BaseHTTPRequestHandler):
    """Respond to GET requests for known API endpoints."""

    def do_GET(self):
        """Return content for the requested endpoint."""
        if self.path == "/":
            self.respond(200, "Hello, this is a simple API!", "text/plain")
        elif self.path == "/status":
            self.respond(200, "OK", "text/plain")
        elif self.path == "/data":
            self.respond(200, json.dumps({
                "name": "John", "age": 30, "city": "New York"
            }), "application/json")
        elif self.path == "/info":
            self.respond(200, json.dumps({
                "version": "1.0",
                "description": "A simple API built with http.server"
            }), "application/json")
        else:
            self.respond(404, "Endpoint not found", "text/plain")

    def respond(self, status, message, content_type):
        """Send an HTTP response with its headers and UTF-8 body."""
        body = message.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("", 8000), SimpleAPIHandler).serve_forever()
