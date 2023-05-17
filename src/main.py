#!/usr/bin/python3

import sys
import sqlite3
import os
import argparse
from typing import List

from remind   import exec_remind
from remember import exec_remember
from list     import exec_list
from forget   import exec_forget
from alter    import exec_alter

COMMANDS = [
    "help", "list", "remember", "version", "forget", "alter"
]

# Flags that will consume next token ie. --title <title value>
POSITIONAL_FLAGS = [
    "-t", "--title", "-v", "--value"
]

NAME = "remind"

VERSION = "1.1.0"

#TODO https://docs.python.org/3/howto/argparse.html#argparse-tutorial

def remove_positional_flags(i, args: List[str], tasks):
    if args[i] not in POSITIONAL_FLAGS:
        assert False, "Unreachable, ther is not positional flag to remove"

    sflag = args[i]
    if len(args) <= i + 1:
        print("ERR, positional flag '%s' requires value" % sflag)
        exit(1)

    val = args[i + 1]

    tasks["positional"].append((sflag, val))

    return i + 1, tasks


def main2():
    args = sys.argv

    NAME = args.pop(0)

    task = {
        "command": None,
        "subcommand": None,
        "options": [],
        "flags": [],
        "positional": []
    }

    n_args = []
    i = 0
    while True:
        if i >= len(args):
            break

        x = args[i]
        if x not in POSITIONAL_FLAGS and (x.startswith("-")):
            task["flags"].append(x)
        elif x in POSITIONAL_FLAGS:
            i, task = remove_positional_flags(i, args, task)
        else:
            n_args.append(x)

        i += 1

    while True:
        if not n_args:
            break
        n_args, task = handle_args(n_args, task)

    if not task["command"]:
        print("ERR: Command is need")
        exit(1)

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

    if task["command"] == "help":
        exec_help()
    elif task["command"] == "list":
        exec_list(task, con)
    elif task["command"] == "alter":
        exec_alter(task, con)
    elif task["command"] == "forget":
        exec_forget(task, con)
    elif task["command"] == "remember":
        exec_remember(task, con)
    elif task["command"] == "version":
        print("remind version ", VERSION)
    else:
        exec_remind(task, con)

def exec_help():
    # General overview of the program
    print("Usage: remind [command] [subcommand] [options]")
    print("Commands:")
    print("  help")
    print("  list")
    print("  remember <title> <value>")
    print("  forget <title>")
    print("  alter <title>")
    print("  version")


def handle_args(args: List[str], context):
    arg = args.pop(0)

    if not context["command"]:
        if arg.lower() in COMMANDS:
            context["command"] = arg.lower()
        else:
            context["command"] = "show"
            context["subcommand"] = arg
    elif not context["subcommand"]:
        context["subcommand"] = arg
    else:
        context["options"].append(arg)

    return args, context


def main():
    parser = argparse.ArgumentParser(prog=NAME, description="A simple program for creating persisting notes", add_help=True)
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode", required=False)
    parser.add_argument("arguments", nargs="*")

    args, rest = parser.parse_known_args()


    print(rest)
    print(args)

    if args.arguments[0] not in COMMANDS:
        # REMIND
        pass

    subargs = args.arguments + rest

    print(subargs)

    mgp = argparse.ArgumentParser(prog=NAME, description="A simple program for creating persisting notes", add_help=True)
    subparsers = mgp.add_subparsers(help="Command to execute", dest="command")


    # # Alter
    parser_alter = subparsers.add_parser("alter", help="Alter reminder")
    parser_alter.add_argument("title", nargs="*", help="Title of the reminder to alter")

    # List
    parser_list = subparsers.add_parser("list", help="List reminders")
    sort_group = parser_list.add_mutually_exclusive_group()
    sort_group.add_argument("-t", "--title", action="store_true", help="Sort by title")
    sort_group.add_argument("-d", "--date", action="store_true", help="Sort by date")

    # # Forget
    parser_forget = subparsers.add_parser("forget", help="Forget reminder")
    parser_forget.add_argument("title", nargs="*", help="Title of the reminder to forget")

    # # Remember
    parser_remember = subparsers.add_parser("remember", help="Remember reminder")
    parser_remember.add_argument("--title", "-t", action="append", help="Title of the reminder to remember")
    parser_remember.add_argument("--alter", "-a", action="store_true", help="Alter reminder with value if provided")
    value_group = parser_remember.add_mutually_exclusive_group(required=False)
    value_group.add_argument("--value", "-v", action="append", help="Value of the reminder to remember")
    value_group.add_argument("--stdin-val", "-sv", action="store_true", help="Provide value from stdin")

    args = mgp.parse_args(subargs)

    print(args)
    pass

if __name__ == "__main__":
    main()
    # main2()
