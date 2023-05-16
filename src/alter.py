from utils import update, aletr_with_editor, fetch, pipe

def exec_alter(task, conn):
    assert task["command"] == "alter", "Unreachable, remember called without argument"

    if "--help" in task["flags"]:
        print_alter_help()
        exit(0)

    title = None

    p_flags = list(map(lambda x: x[0], task["positional"]))
    if "-t" in p_flags:
        title = task["positional"][p_flags.index("-t")][1]
    elif "--title" in p_flags:
        title = task["positional"][p_flags.index("--title")][1]

    if not title:
        title = task["subcommand"] + " " + " ".join(task["options"])

    if not title.strip():
        print("ERR: you need to provide title of reminder to alter it")
        exit(1)

    title = title.strip()
    result_data = fetch(conn, title)

    if not result_data:
        print("ERR: Entry with title: ", title, "does not exist.")
        exit(1)

    update_value = lambda curr_value: update(conn, title, curr_value)

    pipe(result_data[0][1],
        aletr_with_editor,
        update_value
    )
    if "-q" not in task["flags"] and "--quiet" not in task["flags"]:
        print("Altered memory of '" + title + "'")



def print_alter_help():
    print("Usage: remind alter <title>")
    print("Flags:")
    print("  -h, --help     : Print this help message")
    print("  -q, --quiet    : Do not print anything after altering memory")
