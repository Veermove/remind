
def fetch(con, title):
    result = con.execute("SELECT title, value, creation_date FROM reminder WHERE title = ?", (title.strip(),))
    return result.fetchall()
