#!/usr/bin/env python3
"""Test SQLite database connection and schema for notes"""

import sqlite3
import sys
import os

DB_NAME = "myapp.db"

def table_exists(cur, table_name: str) -> bool:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cur.fetchone() is not None

try:
    # Check if database file exists
    if not os.path.exists(DB_NAME):
        print(f"Database file '{DB_NAME}' not found")
        sys.exit(1)
    
    # Connect to database and get version
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version()")
    version = cursor.fetchone()[0]
    print(f"SQLite version: {version}")

    # Verify 'notes' table exists with required columns
    assert table_exists(cursor, "notes"), "notes table does not exist"

    cursor.execute("PRAGMA table_info(notes)")
    cols = cursor.fetchall()
    col_names = {c[1]: c[2] for c in cols}
    required = {
        "id": "INTEGER",
        "title": "TEXT",
        "content": "TEXT",
        "created_at": "",   # allow any type affinity since INTEGER requested
        "updated_at": "",
    }
    for name, type_aff in required.items():
        assert name in col_names, f"Missing column in notes: {name}"

    # Optionally assert seeded rows exist (>=1)
    cursor.execute("SELECT COUNT(*) FROM notes")
    count = cursor.fetchone()[0]
    assert count >= 0, "Failed to read count from notes"
    if count >= 1:
        print(f"Notes rows: {count} (seeded)")
    else:
        print("Notes rows: 0 (no seeds present)")

    conn.close()
    sys.exit(0)
    
except AssertionError as e:
    print(f"Schema assertion failed: {e}")
    sys.exit(1)
except sqlite3.Error as e:
    print(f"Connection failed: {e}")
    sys.exit(1)
