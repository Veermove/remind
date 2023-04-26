#!/usr/bin/python3

import os
import sqlite3
import sys
from itertools import takewhile

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
        remember(con, cur, args)
    elif _arg == 'forget':
        forget(con, cur, args)
    elif _arg == 'alter':
        alter(con, cur, args)
    elif _arg == 'version':
        print("Current remind version:", VERSION)
    else:
        remind(con, args, _arg)

def alter(con, cur, args):
    if not args:
        print("ERR: you need to provide title of reminder to alter it")
        exit(1)

    title = (" ".join(args)).strip()
    prev = fetch(con, title)
    prev_value = prev[0][1]
    temp_file_path = str("/home/" + os.getlogin() + '/~temp.remind')

    with open(temp_file_path, 'w+') as file:
        file.write(prev_value)

    os.system("%s %s" % (os.getenv('EDITOR'), temp_file_path))

    curr_value = None

    with open(temp_file_path, 'r') as file:
        curr_value = file.read()

    if not curr_value:
        print("ERR: cannot leave empty reminder. To remove reminder use 'remind forget'")
        os.remove(temp_file_path)
        exit(1)

    con.execute("""
        UPDATE reminder
        SET last_modified = (datetime('now')),
            value = ?
        WHERE title = ?
    """, (curr_value.strip(), title.strip(),))
    os.remove(temp_file_path)
    print("Altered memory of '" + title + "'")
    con.commit()


def forget(con, cur, args):
    title = " ".join(args)
    result_data = fetch(con, title)
    if not result_data:
        print("ERR: Entry with title: ", title, "does not exist.")
        exit(1)

    print("Dropping", " ".join([result_data[0][0], "added on", result_data[0][2]]))
    delete(con, title)


def fetch(con, title):
    result = con.execute("SELECT title, value, creation_date FROM reminder WHERE title = ?", (title.strip(),))
    return result.fetchall()

def delete(con, title):
    con.execute("DELETE FROM reminder WHERE title = ?", (title.strip(),))
    con.commit()


def remind(con, _args, arg):
    result_data = fetch(con, arg + " " + " ".join(_args))
    if result_data:
        header = " ".join([result_data[0][0], "|    added on", result_data[0][2]])
        print(header)
        print("".ljust(len(header), '-'))
        print(result_data[0][1])


def remember(con, cur, argss):
    if len(argss) < 2:
        print("ERR: title and value are needed to insert reminder")
        exit(1)

    t, v = None, None

    def take_title(args):
        title = [s for s in takewhile(lambda x: x != '-v' and x != '--value' and x != '-sv' and x != '--stdinvalue', args)]
        return title, args[len(title):]

    def take_value(args):
        value = [s for s in takewhile(lambda x: x != '-t' and x != '--title' and x != '-sv' and x != '--stdinvalue', args)]
        return value, args[len(value):]

    while (t is None or v is None) and len(argss) > 0:
        flag_0 = argss.pop(0)

        if flag_0 == '-v' or flag_0 == '--value':
            v, argss = take_value(argss)
            v = " ".join(v)
        elif flag_0 == '-t' or flag_0 == '--title':
            t, argss = take_title(argss)
            t = " ".join(t)
        elif flag_0 == '-sv' or flag_0 == '--stdinvalue':
            try:
                value = ""
                while True:
                    value += input()
                    value += '\n'
            except (EOFError, KeyboardInterrupt) as _:
                v = value
                continue
        else:
            print("ERR: Unrecognized flag " + flag_0)
            exit(1)

    if t is None:
        print("ERR: Title is missing")
        exit(1)

    if v is None:
        print("ERR: Value is missing")
        exit(1)

    title, value = t, v

    result = con.execute("SELECT title, value, creation_date FROM reminder WHERE title = ?", (title,))
    result_data = result.fetchall()
    if result_data:
        print("ERR: reminder with that title already exists.")
        exit(1)

    cur.execute("""
        INSERT INTO reminder (title, value, creation_date, last_modified)
        VALUES(?, ?, datetime('now'), datetime('now'))
    """, (title, value,))
    con.commit()
    print("Remembered '" + title +"', ", cur.lastrowid)

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
