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


drugs = connection.execute(
    """
    SELECT id, generic_name, brand_name, active_ingredient
    FROM drugs
    ORDER BY id;
    """
).fetchall()

print("\nDrugs stored in database:")

for drug in drugs:
    print(
        f"ID: {drug[0]} | "
        f"Generic: {drug[1]} | "
        f"Brand: {drug[2]} | "
        f"Active ingredient: {drug[3]}"
    )

connection.close()