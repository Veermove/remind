#!/usr/bin/python3

import os
import sqlite3
import sys

from src.alter import alter
from src.forget import forget
from src.remember import remember
from src.remind import exec_list, remind

VERSION = "1.0.1"

def main():
    args = sys.argv
    db_path = str("/home/" + os.getlogin() + "/.reminder.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    name = args.pop(0)
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

    if len(args) < 1:
        print("ERR, use: remind remember [-t|--title] <title> [-v|--value|-sv|--stdinvalue] <value>")
        print("or: remind <title>")
        print("or: remind list [-t|--title|-d|--date]")
        exit(1)

    _arg = args.pop(0)
    if _arg == 'list':
        exec_list(cur, args)
    elif _arg == 'remember':
        remember(name, con, cur, args)
    elif _arg == 'forget':
        forget(name, con, args)
    elif _arg == 'alter':
        alter(name, con, args)
    elif _arg == 'version':
        print("Current remind version:", VERSION)
    else:
        remind(con, args, _arg)


if __name__ == "__main__":
    main()
