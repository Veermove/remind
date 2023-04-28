
def fetch(con, title):
    result = con.execute("SELECT title, value, creation_date FROM reminder WHERE title = ?", (title.strip(),))
    return result.fetchall()

def remind(con, _args, arg):
    result_data = fetch(con, arg + " " + " ".join(_args))
    if result_data:
        header = " ".join([result_data[0][0], "|    added on", result_data[0][2]])
        print(header)
        print("".ljust(len(header), '-'))
        print(result_data[0][1])




def exec_list(cur, args):
    order = ""
    if len(args) > 0:
        sort_flag = args.pop(0)
        if sort_flag == '-d' or sort_flag == '--date':
            order = "ORDER BY creation_date ASC"
        elif sort_flag == '-t' or sort_flag == '--title':
            order = "ORDER BY title ASC"
        else:
            print("ERR: Unrecognized sort flag '" + sort_flag + "'. Possible sort flags: -d --date -t --tile")
            exit(1)

    result = cur.execute("""
        SELECT title, creation_date FROM reminder
    """ + order)

    res_data = result.fetchall()

    if not res_data:
        exit(0)

    longest = max(map(lambda x: len(x[0]), res_data))
    for (title, date) in res_data:
        print(title.ljust(longest), end="")
        print("   ", end="")
        print(date)


