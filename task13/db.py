import sqlite3

DB_PATH = "sample.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_sales_data(month):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT date, region, revenue, units
    FROM sales
    WHERE substr(date, 1, 7) = ?
    """

    cursor.execute(query, (month,))
    rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "date": r[0],
            "region": r[1],
            "revenue": r[2],
            "units": r[3]
        })

    conn.close()
    return data