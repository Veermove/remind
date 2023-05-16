from utils import fetch, delete

def exec_forget(task, conn):
    assert task["command"] == "forget", "Unreachable, forget called without delete argument"

    if "--help" in task["flags"]:
        print_forget_help()
        exit(0)

    title = task["subcommand"]
    if task["options"]:
        title += " " + " ".join(task["options"])

    result_data = fetch(conn, title)
    if not result_data:
        print("ERR: Entry with title: ", title, "does not exist.")
        exit(1)

    if "-q" not in task["flags"] and "--quiet" not in task["flags"]:
        print("Dropping", " ".join([result_data[0][0], "added on", result_data[0][2]]))
    delete(conn, title)

def print_forget_help():
    print("Usage: forget [options] <title>")
    print("Flags:")
    print("  -q, --quiet    : Do not print the title of the entry being deleted")
    print("  -h, --help     : Print this help message")
