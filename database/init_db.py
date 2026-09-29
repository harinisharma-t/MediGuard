import sqlite3
from pathlib import Path


DATABASE_FOLDER = Path(__file__).resolve().parent
DATABASE_FILE = DATABASE_FOLDER / "mediguard.db"
SCHEMA_FILE = DATABASE_FOLDER / "schema.sql"


def initialize_database():
    connection = sqlite3.connect(DATABASE_FILE)

    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        schema = file.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()

    print("Database initialization completed.")
    print("Database:", DATABASE_FILE)