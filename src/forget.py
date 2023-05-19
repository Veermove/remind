from utils import fetch, delete

def exec_forget(task, conn):
    if not task.title:
        print("ERR: No title given.")
        exit(1)


    title = " ".join(task.title)

    result_data = fetch(conn, title)
    if not result_data:
        print("ERR: Entry with title: ", title, "does not exist.")
        exit(1)

    if not task.quiet:
        print("Dropping", " ".join([result_data[0][0], "added on", result_data[0][2]]))
    delete(conn, title)
