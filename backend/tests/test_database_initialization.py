import sqlite3

from database import init_db


def test_initialize_database_creates_required_tables(tmp_path, monkeypatch):
    database_file = tmp_path / "test_mediguard.db"

    monkeypatch.setattr(init_db, "DATABASE_FILE", database_file)

    init_db.initialize_database()

    connection = sqlite3.connect(database_file)

    tables = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }

    connection.close()

    assert {"patients", "drugs", "prescriptions", "interactions", "allergies"} <= tables
