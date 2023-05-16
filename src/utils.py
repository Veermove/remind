import os

TEMP_FILE_PATH = str("/home/" + os.getlogin() + '/~temp.remind')

def fetch(con, title):
    result = con.execute("SELECT title, value, creation_date FROM reminder WHERE title = ?", (title.strip(),))
    return result.fetchall()

def fetchall(con, ordering):
    stmt = """
        SELECT title, creation_date FROM reminder
    """ + ordering
    result = con.execute(stmt)

    return result.fetchall()

def fetchall_titles(con, name):
    if name:
        stmt = "SELECT title FROM reminder WHERE title LIKE ?"
        result = con.execute(stmt, (name.strip() + "%",))
    else:
        stmt = "SELECT title FROM reminder"
        con.execute(stmt)

    return result.fetchall()

def aletr_with_editor(def_value) -> str:
    with open(TEMP_FILE_PATH, 'w+') as file:
        file.write(def_value)

    os.system("%s %s" % (os.getenv('EDITOR'), TEMP_FILE_PATH))

    curr_value = None

    with open(TEMP_FILE_PATH, 'r') as file:
        curr_value = file.read()

    if not curr_value:
        print("ERR: cannot leave empty reminder. To remove reminder use 'remind forget'")
        os.remove(TEMP_FILE_PATH)
        exit(1)

    os.remove(TEMP_FILE_PATH)

    return curr_value

def update(con, title, value):
    con.execute("""
        UPDATE reminder
        SET
            last_modified = (datetime('now')),
            value = ?
        WHERE title = ?""",
        (value.strip() + "\n", title.strip(),))

    con.commit()

def remember(con, title, value):
    con.execute("""
        INSERT INTO reminder (title, value, creation_date, last_modified)
        VALUES(?, ?, datetime('now'), datetime('now'))
    """, (title, value,))
    con.commit()



def delete(con, title):
    con.execute("DELETE FROM reminder WHERE title = ?", (title.strip(),))
    con.commit()


def pipe(val, *kwargs):
    for func in kwargs:
        val = func(val)
    return val
