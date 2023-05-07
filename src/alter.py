import os

from utils import fetch

TEMP_FILE_PATH = str("/home/" + os.getlogin() + '/~temp.remind')

def alter(program_name, con, args):
    if not args:
        print("ERR: you need to provide title of reminder to alter it")
        exit(1)

    title = (" ".join(args)).strip()
    if title.startswith("--help"):
        p_help_alter(program_name)

    prev = fetch(con, title)
    prev_value = prev[0][1]


    with open(TEMP_FILE_PATH, 'w+') as file:
        file.write(prev_value)

    os.system("%s %s" % (os.getenv('EDITOR'), TEMP_FILE_PATH))

    curr_value = None

    with open(TEMP_FILE_PATH, 'r') as file:
        curr_value = file.read()

    if not curr_value:
        print("ERR: cannot leave empty reminder. To remove reminder use '%s forget'" % program_name)
        os.remove(TEMP_FILE_PATH)
        exit(1)

    con.execute("""
        UPDATE reminder
        SET
            last_modified = (datetime('now')),
            value = ?
        WHERE title = ?""",
        (curr_value.strip() + "\n", title.strip(),))

    os.remove(TEMP_FILE_PATH)
    print("Altered memory of '" + title + "'")
    con.commit()

def p_help_alter(prog_name):
    print("Usage: %s alter <title>" % prog_name)
    print("Allows to edit reminder with text editor of choice.")
    print("Note: Temporary file will created at %s" % TEMP_FILE_PATH)
    print("Text editor decided by environment variable EDITOR will be",
          "opened with that file. Once editor is closed file will be removed.")

    exit(0)
