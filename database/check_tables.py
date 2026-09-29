import sqlite3
from pathlib import Path

DATABASE_FILE = Path(__file__).resolve().parent / "mediguard.db"

connection = sqlite3.connect(DATABASE_FILE)

tables = connection.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name;
    """
).fetchall()

print("Tables created:")

for table in tables:
    print("-", table[0])

connection.close()