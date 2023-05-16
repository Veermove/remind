from utils import fetch, fetchall_titles


def exec_remind(task, conn):
    if "-h" in task["flags"] or "--help" in task["flags"]:
        print_remind_help()
        exit(0)

    if not task["command"]:
        print("ERR, need reminder name to disaply it")
        exit(1)

    assert task["command"] == "show", "Unreachable, Show called without show argument"

    name = task["subcommand"] + " "
    if task["options"]:
        name += " ".join(task["options"])

    result_data = fetch(conn, name)

    q = False
    if "-q" in task["flags"] or "--quiet" in task["flags"]:
        q = True

    if result_data:
        if not q:
            header = " ".join([result_data[0][0], "|    added on", result_data[0][2]])
            print(header)
            print("".ljust(len(header), '-'))
        print(result_data[0][1])
    else:
        first_letter = name[0]
        results = fetchall_titles(conn, first_letter)
        if results and not q:
            print("ERR, no reminder with name '%s'" % name.strip())
            print("Did you mean one of these?")
            i = 0
            for res in results:
                if i >= 3:
                    break
                i += 1
                print("  ", res[0])


def print_remind_help():
    print("Usage: remind [options] <name>")
    print("Flags:")
    print("  -q, --quiet    : Do not print the header")
    print("  -h, --help     : Print this help message")
