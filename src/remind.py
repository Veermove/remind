from utils import fetch, fetchall_titles


def exec_remind(task, conn):
    print(task)

    name = " ".join(task.arguments)

    result_data = fetch(conn, name)

    if result_data:
        if not task.quiet:
            header = " ".join([result_data[0][0], "|    added on", result_data[0][2]])
            print(header)
            print("".ljust(len(header), '-'))
        print(result_data[0][1])
    else:
        first_letter = name[0]
        results = fetchall_titles(conn, first_letter)
        if not task.quiet:
            print("ERR, no reminder with name '%s'" % name.strip())
            print("Did you mean one of these?")
            i = 0
            for res in results:
                if i >= 3:
                    break
                i += 1
                print("  ", res[0])

    exit(0)
