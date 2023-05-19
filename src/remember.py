from utils import aletr_with_editor, fetch, remember


def exec_remember(task, conn):

    if not task.title:
        print("ERR: Title is required")
        exit(1)

    title = task.title[0]
    value = None

    if task.value:
        value = task.value[0]
    elif task.stdin_val:
        try:
            v = ""
            while True:
                v += input()
                v += '\n'
        except (EOFError, KeyboardInterrupt) as _:
            value = v

    if task.alter:
        value = aletr_with_editor(" ".join(value) if value is not None else "")

    if value is None:
        print("ERR: Value is required")
        exit(1)

    prev_data = fetch(conn, title)

    if prev_data:
        print("ERR: reminder with that title already exists.")
        exit(1)

    remember(conn, title, value)
    if not task.quiet:
        print("Remembered '" + title +"'")

    exit(0)
