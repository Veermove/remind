from utils import fetchall


#TODO: [-f <filter>] [-l <limit>] [-o <offset>]
def exec_list(task, conn):
    order = " ORDER BY "
    order_set = False
    if task["flags"]:
        if '-sd' in task["flags"] or '--sort-date' in task["flags"]:
            order += " creation_date ASC"
            if order_set:
                order += ","
            order_set = True
        elif "-st" in task["flags"] or "--sort-title" in task["flags"]:
            order += " title ASC"
            if order_set:
                order += ","
            order_set = True

    if order.startswith(","):
        order = order[1:].strip()

    if order_set:
        res_data = fetchall(conn, order)
    else:
        res_data = fetchall(conn, "")


    if not res_data:
        exit(0)

    longest = max(map(lambda x: len(x[0]), res_data))
    for (title, date) in res_data:
        print(title.ljust(longest), end="")
        print("   ", end="")
        if "-q" not in task["flags"] and "--quiet" not in task["flags"]:
            print(date)
        else:
            print()
