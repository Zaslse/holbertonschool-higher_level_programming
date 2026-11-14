#!/usr/bin/python3
"""Create and populate the sample SQLite Products database."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'products.db'


def create_database():
    """Create the table and insert the sample products without duplicates."""
    with sqlite3.connect(str(DB_PATH)) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL
            )
        """)
        connection.executemany(
            'INSERT OR IGNORE INTO Products (id, name, category, price) '
            'VALUES (?, ?, ?, ?)',
            [(1, 'Laptop', 'Electronics', 799.99),
             (2, 'Coffee Mug', 'Home Goods', 15.99)]
        )


if __name__ == '__main__':
    create_database()
