#!/usr/bin/python3

import os
import sqlite3
import sys

from itertools import takewhile

VERSION = "1.0.3"
TEMP_FILE_PATH = str("/home/" + os.getlogin() + '/~temp.remind')

# ALTER ======

def alter(program_name, con, args):
    if not args:
        print("ERR: you need to provide title of reminder to alter it")
        exit(1)

    title = (" ".join(args)).strip()
    if title.startswith("--help"):
        p_help_alter(program_name)

    prev = fetch(con, title)
    prev_value = prev[0][1]


    with open(TEMP_FILE_PATH, 'w+') as file:
        file.write(prev_value)

    os.system("%s %s" % (os.getenv('EDITOR'), TEMP_FILE_PATH))

    curr_value = None

    with open(TEMP_FILE_PATH, 'r') as file:
        curr_value = file.read()

    if not curr_value:
        print("ERR: cannot leave empty reminder. To remove reminder use '%s forget'" % program_name)
        os.remove(TEMP_FILE_PATH)
        exit(1)

    con.execute("""
        UPDATE reminder
        SET
            last_modified = (datetime('now')),
            value = ?
        WHERE title = ?""",
        (curr_value.strip() + "\n", title.strip(),))

    os.remove(TEMP_FILE_PATH)
    print("Altered memory of '" + title + "'")
    con.commit()

def p_help_alter(prog_name):
    print("Usage: %s alter <title>" % prog_name)
    print("Allows to edit reminder with text editor of choice.")
    print("Note: Temporary file will created at %s" % TEMP_FILE_PATH)
    print("Text editor decided by environment variable EDITOR will be",
          "opened with that file. Once editor is closed file will be removed.")

    exit(0)


### FORGET   ========

def forget(program_name, con, args):
    title = " ".join(args)

    if title.startswith("--help"):
        p_help_forget(program_name)

    result_data = fetch(con, title)
    if not result_data:
        print("ERR: Entry with title: ", title, "does not exist.")
        exit(1)

    print("Dropping", " ".join([result_data[0][0], "added on", result_data[0][2]]))
    delete(con, title)

def delete(con, title):
    con.execute("DELETE FROM reminder WHERE title = ?", (title.strip(),))
    con.commit()


def p_help_forget(program_name):
    print("Usage: %s forget <title>" % program_name)
    print("Immieditaly removes note from memory.")
    exit(0)


### REMEMBER ========

def remember(program_name, con, cur, argss):
    if argss and argss[0] == '--help':
        p_help_remember(program_name)

    if len(argss) < 2:
        print("ERR: title and value are needed to insert reminder")
        exit(1)

    t, v = None, None

    def take_title(args):
        title = [s for s in takewhile(lambda x: x not in ['-v', '--value', '-sv', '--stdinvalue'])]
        return title, args[len(title):]

    def take_value(args):
        value = [s for s in takewhile(lambda x: x not in ['-t', '--title', '-sv', '--stdinvalue'])]
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

def p_help_remember(program_name):
    print("Usage: %s remember <title> <value>" % program_name)
    print("Remembers a note.")
    print("Title and value can be provided in any order as long as title is prefixed by:")
    print("    --title or -t")
    print("and value by:")
    print("    --value or -v\n")
    print("Additional option for providing value is with standard input. This is done via flags -sv or --stdinvalue.\n")
    exit(0)


### REMIND ========

def fetch(con, title):
    result = con.execute("SELECT title, value, creation_date FROM reminder WHERE title = ?", (title.strip(),))
    return result.fetchall()

def remind(con, _args, arg):
    result_data = fetch(con, arg + " " + " ".join(_args))
    if result_data:
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
