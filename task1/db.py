import sqlite3
from datetime import datetime

DB = "products.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            asin TEXT PRIMARY KEY,
            title TEXT,
            price REAL,
            last_seen TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_products(products):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    for asin, title, price, last_seen in products:
        cur.execute("""
            INSERT INTO products (asin, title, price, last_seen)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(asin) DO UPDATE SET
                title = excluded.title,
                price = excluded.price,
                last_seen = excluded.last_seen
        """, (asin, title, price, last_seen))

    conn.commit()
    conn.close()


def last_seen_prices():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT asin, price FROM products")
    rows = cur.fetchall()

    conn.close()

    result = {}

    for asin, price in rows:
        result[asin] = price

    return result