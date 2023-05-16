from utils import aletr_with_editor, fetch, remember


def exec_remember(task, conn):
    assert task["command"] == "remember", "Unreachable, remember called without add argument"

    if "--help" in task["flags"]:
        print_remember_help()
        exit(0)

    title = None
    value = None
    if task["subcommand"]:
        title = task["subcommand"]

    if task["options"]:
        value = " ".join(task["options"])

    positional_flags = list(map(lambda s: s[0], task["positional"]))

    if value is not None and \
        ("-v" in positional_flags or "--value" in positional_flags):

        flag_val = next(filter(lambda s: s[0] == "-v" or s[0] == "--value", task["positional"]))
        print("ERR: Conflicting value: Cannot use both flags and options for value")
        print("---> flags: %s %s" % (flag_val[0], flag_val[1]))
        print("---> options: %s" % " ".join(task["options"]))
        exit(1)
    elif value is None and \
        ("-v" in positional_flags and "--value" in positional_flags):

        value = next(filter(lambda s: s[0] == "-v" or s[0] == "--value", task["positional"]))[1]


    if title is not None and \
        ("-t" in positional_flags or "--title" in positional_flags):

        flag_val = next(filter(lambda s: s[0] == "-t" or s[0] == "--title", task["positional"]))
        print("ERR: Conflicting title. Cannot use both flags and options for title")
        print("---> flags: %s %s" % (flag_val[0], flag_val[1]))
        print("---> options: %s" % " ".join(task["options"]))
        exit(1)
    elif title is None and \
        ("-t" in positional_flags and "--title" in positional_flags):

        title = next(filter(lambda s: s[0] == "-t" or s[0] == "--title", task["positional"]))[1]

    if value is not None and \
        ("-sv" in task["flags"] or "--stdin-val" in task["flags"]):

        print("ERR: Conflicting value. Cannot use both stdin and options for value")
        exit(1)
    elif value is None and \
        ("-sv" in task["flags"] or "--stdin-val" in task["flags"]):

        try:
            v = ""
            while True:
                v += input()
                v += '\n'
        except (EOFError, KeyboardInterrupt) as _:
            value = v

    if "-a" in task["flags"] or "--alter" in task["flags"]:
        value = aletr_with_editor(value if value is not None else "")

    if title is None:
        print("ERR: Title is required")
        exit(1)
    if value is None:
        print("ERR: Value is required")
        exit(1)

    prev_data = fetch(conn, title)
    if prev_data:
        print("ERR: reminder with that title already exists.")
        exit(1)

    remember(conn, title, value)
    if "-q" not in task["flags"] and "--quiet" not in task["flags"]:
        print("Remembered '" + title +"'")


def print_remember_help():
    print("""
remember - Remember note
> remind remember <title> <value>

Flags:
    -q, --quiet         : Don't print anything after remembering
    -a, --alter         : Open editor to alter value directly. If value is provided, it will be inserted into editor.
    -sv, --stdin-val    : Read value from stdin.
    -t, --title <title> : Title of the note
    -v, --value <value> : Value of the note
    -h, --help          : Print this help message
    """)
