import sqlite3

conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sales")

cursor.execute("""
CREATE TABLE sales (
    date TEXT,
    region TEXT,
    revenue INTEGER,
    units INTEGER
)
""")

sample_data = [
    ("2026-01-01", "North", 412000, 1000),
    ("2026-01-02", "East", 338000, 900),
    ("2026-01-03", "South", 309000, 800),
    ("2026-01-04", "West", 189000, 700),
]

cursor.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", sample_data)

conn.commit()
conn.close()

print("✅ Database initialized")