from itertools import takewhile

def remember(program_name, con, cur, argss):
    if argss[0] == '--help':
        p_help()

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

def p_help(program_name):
    print("Usage: %s remember <title> <value>" % program_name)
    print("Remembers a note.")
    print("Title and value can be provided in any order as long as title is prefixed by:")
    print("    --title or -t")
    print("and value by:")
    print("    --value or -v\n")
    print("Additional option for providing value is with standard input. This is done via flags -sv or --stdinvalue.")
    exit(0)
