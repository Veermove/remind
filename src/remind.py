#!/usr/bin/python3

import os
import sqlite3
import sys

from alter import alter
from forget import forget
from remember import remember
from utils import fetch

VERSION = "1.0.6"

def remind(con, _args, arg):
    q = False
    if arg == '-q':
        q = True
        arg = ""
    if _args and  _args[-1] == '-q':
        q = True
        _args.remove('-q')
    if arg == '--quiet':
        q = True
        arg = ""
    if _args and  _args[-1] == '--quiet':
        q = True
        _args.remove('--quiet')

    result_data = fetch(con, arg + " " + " ".join(_args))

    if result_data:
        if not q:
            header = " ".join([result_data[0][0], "|    added on", result_data[0][2]])
            print(header)
            print("".ljust(len(header), '-'))
        print(result_data[0][1])

def exec_list(cur, args):
    order = ""
    if len(args) > 0:
        sort_flag = args.pop(0)
        if sort_flag == '-d' or sort_flag == '--date':
            order = "ORDER BY creation_date ASC"
        elif sort_flag == '-t' or sort_flag == '--title':
            order = "ORDER BY title ASC"
        else:
            print("ERR: Unrecognized sort flag '" + sort_flag + "'. Possible sort flags: -d --date -t --tile")
            exit(1)

    result = cur.execute("""
        SELECT title, creation_date FROM reminder
    """ + order)

    res_data = result.fetchall()

    if not res_data:
        exit(0)

    longest = max(map(lambda x: len(x[0]), res_data))
    for (title, date) in res_data:
        print(title.ljust(longest), end="")
        print("   ", end="")
        print(date)


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
