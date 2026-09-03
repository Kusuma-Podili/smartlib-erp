"""
Console execution entrypoint: python -m smartlib.cli.manage <command>
"""

import argparse
import sys
from smartlib.cli.commands import CLICommands

def main():
    parser = argparse.ArgumentParser(description="SmartLibrary ERP Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # init-db
    subparsers.add_parser("init-db", help="Initialize SQLite tables and schema")

    # seed
    subparsers.add_parser("seed", help="Seed default admin, librarian, and patron accounts")

    # list-users
    subparsers.add_parser("list-users", help="List registered users in system")

    # create-user
    create_parser = subparsers.add_parser("create-user", help="Register a new user account")
    create_parser.add_argument("--username", required=True, help="Username")
    create_parser.add_argument("--email", required=True, help="Email address")
    create_parser.add_argument("--password", required=True, help="Account password")
    create_parser.add_argument("--role", default="MEMBER", choices=["ADMIN", "LIBRARIAN", "MEMBER"], help="User role")

    args = parser.parse_args()

    if args.command == "init-db":
        CLICommands.init_db()
    elif args.command == "seed":
        CLICommands.seed_data()
    elif args.command == "list-users":
        CLICommands.list_users()
    elif args.command == "create-user":
        CLICommands.create_user(args.username, args.email, args.password, args.role)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
