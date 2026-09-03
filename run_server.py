"""
SmartLibrary ERP Web Server Starter.
Run with: python run_server.py
"""
import sys
from wsgiref.simple_server import make_server
from smartlib.web.app import create_app

def main():
    host = "127.0.0.1"
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    app = create_app()
    server = make_server(host, port, app)
    print("=" * 70)
    print("  SmartLibrary ERP - Enterprise Library Management System")
    print(f"  Live Local Server: http://{host}:{port}")
    print(f"  Admin Portal:      http://{host}:{port}/admin/dashboard")
    print(f"  Librarian Desk:    http://{host}:{port}/librarian/dashboard")
    print(f"  Member Portal:     http://{host}:{port}/member/dashboard")
    print("=" * 70)
    print("Pre-seeded Test Accounts:")
    print("  Admin:     admin@library.com     / Admin@123")
    print("  Librarian: librarian@library.com / Librarian@123")
    print("  Member:    member@library.com    / Member@123")
    print("=" * 70)
    print("Press Ctrl+C to shut down server.")
    server.serve_forever()

if __name__ == "__main__":
    main()
