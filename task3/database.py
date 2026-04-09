import sqlite3

connection = None

def connect(db_name="orm.db"):
    global connection
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row


def execute(query, params=None):
    if params is None:
        params = []

    print("SQL:", query)
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    return cursor