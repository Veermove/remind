from utils import update, aletr_with_editor, fetch, pipe

def exec_alter(task, conn):
    if not task.title:
        print("ERR: No title given.")
        exit(1)


    title = " ".join(task.title)
    result_data = fetch(conn, title)

    if not result_data:
        print("ERR: Entry with title: ", title, "does not exist.")
        exit(1)

    update_value = lambda curr_value: update(conn, title, curr_value)

    pipe(result_data[0][1],
        aletr_with_editor,
        update_value
    )
    if not task.quiet:
        print("Altered memory of '" + title + "'")

    exit(0)

