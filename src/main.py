#!/usr/bin/python3

import os
import sys
import sqlite3
from typing import List

from remind   import exec_remind
from list     import exec_list
from remember import exec_remember
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


def main():
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
        if x not in POSITIONAL_FLAGS and (x.startswith("-") or x.startswith("--")):
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


if __name__ == "__main__":
    main()
