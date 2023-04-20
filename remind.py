#!/usr/bin/python3

import sqlite3
import sys
from itertools import takewhile

def main():
    args = sys.argv
    con = sqlite3.connect("reminder.db")
    cur = con.cursor()
    name = args.pop(0)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminder(
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            title          TEXT NOT NULL,
            value          TEXT NOT NULL,
            creation_date  DATETIME NOT NULL
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS reminder_title_ind
            ON reminder(title)
    """)

    _arg = args.pop(0)
    if _arg == 'list':
        exec_list(cur, args)
    elif _arg == 'remember':
        remember(con, cur, args)


def remember(con, cur, argss):
    if len(argss) < 2:
        print("ERR: title and value are needed to insert reminder")
        exit(1)

    t, v = None, None

    def take_title(args):
        title = [s for s in takewhile(lambda x: x != '-v' and x != '--value', args)]
        return title, args[len(title):]

    def take_value(args):
        value = [s for s in takewhile(lambda x: x != '-t' and x != '--title', args)]
        return value, args[len(value):]

    while (t is None or v is None) and len(argss) > 0:
        flag_0 = argss.pop(0)

        if flag_0 == '-v' or flag_0 == '--value':
            v, argss = take_value(argss)
        elif flag_0 == '-t' or flag_0 == '--title':
            t, argss = take_title(argss)
        else:
            print("ERR: Unrecognized flag " + flag_0)
            exit(1)

    if t is None:
        print("ERR: Title is missing")
        exit(1)

    if v is None:
        print("ERR: Value is missing")
        exit(1)

    title, value = " ".join(t), " ".join(v)
    print(title, value)
    cur.execute("""
        INSERT INTO reminder (title, value, creation_date)
        VALUES(?, ?, datetime('now'))
    """, (title, value,))
    con.commit()
    print("Remembered: ", cur.lastrowid)

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






if __name__ == "__main__":
    main()
