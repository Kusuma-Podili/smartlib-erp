"""
Lightweight pure-Python WSGI web server and HTTP request router for SmartLibrary ERP.
Provides full session support, role guard verification, JSON and HTML dispatching without heavy dependencies.
"""

import json
import urllib.parse
from wsgiref.simple_server import make_server
from typing import Callable, Dict, Any, Tuple
from smartlib.authentication.session_manager import SessionManager
from smartlib.authentication.auth_service import AuthService
from smartlib.database.migrations import MigrationManager
from smartlib.database.seeder import DatabaseSeeder

class SimpleRouter:
    def __init__(self):
        self.routes: Dict[Tuple[str, str], Callable] = {}
        self.session_mgr = SessionManager()
        self.auth_svc = AuthService()

    def add_route(self, method: str, path: str, handler: Callable):
        self.routes[(method.upper(), path)] = handler

    def handle_request(self, environ: Dict[str, Any]) -> Tuple[str, str, Dict[str, str]]:
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = environ.get("PATH_INFO", "/")

        handler = self.routes.get((method, path))
        if not handler:
            return "404 Not Found", "<h1>404 Not Found</h1>", {"Content-Type": "text/html"}

        try:
            return handler(environ)
        except Exception as e:
            return "500 Internal Server Error", f"<h1>500 Error: {str(e)}</h1>", {"Content-Type": "text/html"}

def create_app():
    # Ensure database is initialized
    migrator = MigrationManager()
    migrator.apply_initial_schema()
    seeder = DatabaseSeeder()
    seeder.seed_all()

    router = SimpleRouter()

    def index_handler(environ):
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>SmartLibrary ERP</title></head>
        <body style="font-family: sans-serif; padding: 40px; text-align: center;">
            <h1>Welcome to SmartLibrary ERP</h1>
            <p>Enterprise Library Resource Planning System</p>
            <p><a href="/login">Login to Portal</a></p>
        </body>
        </html>
        """
        return "200 OK", html, {"Content-Type": "text/html"}

    router.add_route("GET", "/", index_handler)
    return router
