from remind import fetch

def forget(program_name, con, args):
    title = " ".join(args)

    if title.startswith("--help"):
        p_help()

    result_data = fetch(con, title)
    if not result_data:
        print("ERR: Entry with title: ", title, "does not exist.")
        exit(1)

    print("Dropping", " ".join([result_data[0][0], "added on", result_data[0][2]]))
    delete(con, title)

def delete(con, title):
    con.execute("DELETE FROM reminder WHERE title = ?", (title.strip(),))
    con.commit()


def p_help(program_name):
    print("Usage: %s forget <title>" % program_name)
    print("Immieditaly removes note from memory.")
    exit(0)
