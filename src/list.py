from utils import fetchall


#TODO: [-f <filter>] [-l <limit>] [-o <offset>]
def exec_list(task, conn):
    order = ""
    if 'title' in task and task.title:
        order += " ORDER BY title ASC"
    elif 'date' in task and task.date:
        order += " ORDER BY creation_date ASC"

    res_data = fetchall(conn, order)


    if not res_data:
        exit(0)

    longest = max(map(lambda x: len(x[0]), res_data))
    for (title, date) in res_data:
        print(title.ljust(longest), end="")
        print("   ", end="")
        if not task.quiet:
            print(date)
        else:
            print()

    exit(0)
