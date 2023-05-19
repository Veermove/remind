#!/usr/bin/python3

import sqlite3
import os
import argparse

from remind   import exec_remind
from remember import exec_remember
from list     import exec_list
from forget   import exec_forget
from alter    import exec_alter

COMMANDS = [
    "help", "list", "remember", "version", "forget", "alter"
]

NAME = "remind"

VERSION = "1.1.0"

#TODO https://docs.python.org/3/howto/argparse.html#argparse-tutorial
#



def main():
    db_path = str("/home/" + os.getlogin() + "/.reminder.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminder(
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            title          TEXT NOT NULL UNIQUE,
            value          TEXT NOT NULL,
            creation_date  DATETIME NOT NULL,
            last_modified  DATETIME NOT NULL
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS reminder_title_ind
            ON reminder(title)
    """)


    parser = argparse.ArgumentParser(prog=NAME, description="A simple program for creating persisting notes", add_help=True)
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode", required=False)
    parser.add_argument("arguments", nargs="*")

    args, rest = parser.parse_known_args()

    if args.arguments[0] not in COMMANDS:
        exec_remind(args, con)

    subargs = args.arguments + rest

    mgp = argparse.ArgumentParser(prog=NAME, description="A simple program for creating persisting notes", add_help=True)
    mgp.add_argument("-q", "--quiet", action="store_true", help="Quiet mode", required=False)
    subparsers = mgp.add_subparsers(help="Command to execute", dest="command")


    # Alter
    parser_alter = subparsers.add_parser("alter", help="Alter reminder")
    parser_alter.add_argument("title", nargs="*", help="Title of the reminder to alter")

    # List
    parser_list = subparsers.add_parser("list", help="List reminders")
    sort_group = parser_list.add_mutually_exclusive_group()
    sort_group.add_argument("-t", "--title", action="store_true", help="Sort by title")
    sort_group.add_argument("-d", "--date", action="store_true", help="Sort by date")

    # Forget
    parser_forget = subparsers.add_parser("forget", help="Forget reminder")
    parser_forget.add_argument("title", nargs="*", help="Title of the reminder to forget")

    # Remember
    parser_remember = subparsers.add_parser("remember", help="Remember reminder")
    parser_remember.add_argument("--title", "-t", action="append", help="Title of the reminder to remember")
    parser_remember.add_argument("--alter", "-a", action="store_true", help="Alter reminder with value if provided")
    value_group = parser_remember.add_mutually_exclusive_group(required=False)
    value_group.add_argument("--value", "-v", action="append", help="Value of the reminder to remember")
    value_group.add_argument("--stdin-val", "-sv", action="store_true", help="Provide value from stdin")

    # Version
    subparsers.add_parser("version", help="Check version of the program")

    args = mgp.parse_args(subargs)

    print(args)

    if args.command == "list":
        exec_list(args, con)
    elif args.command == "alter":
        exec_alter(args, con)
    elif args.command == "forget":
        exec_forget(args, con)
    elif args.command == "remember":
        exec_remember(args, con)
    elif args.command == "version":
        print(NAME + " " + VERSION)
    else:
        # Unreachable
        assert False, "Unreachable"

if __name__ == "__main__":
    main()
