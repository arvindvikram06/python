import sqlite3

connection = None

# Initialize connection to the SQLite database
def connect(db_name="orm.db"):
    global connection
    connection = sqlite3.connect(db_name)
    # Enable access to rows as dictionaries
    connection.row_factory = sqlite3.Row

# Execute a raw SQL query safely with parameters
def execute(query, params=None):
    if params is None:
        params = []

    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    return cursor