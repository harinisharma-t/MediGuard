
import json
import sqlite3

from database import load_drug_data


def test_load_drug_data_inserts_drug_records(tmp_path, monkeypatch):
    database_file = tmp_path / "test_mediguard.db"
    data_file = tmp_path / "drug_data.json"

    connection = sqlite3.connect(database_file)
    connection.execute(
        """
        CREATE TABLE drugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generic_name TEXT,
            brand_name TEXT,
            active_ingredient TEXT
        )
        """
    )
    connection.commit()
    connection.close()

    records = [
        {
            "brand_name": ["TestBrand"],
            "generic_name": ["test medicine"],
            "active_ingredient": ["test ingredient"],
        }
    ]

    data_file.write_text(json.dumps(records), encoding="utf-8")

    monkeypatch.setattr(load_drug_data, "DATABASE_FILE", database_file)
    monkeypatch.setattr(load_drug_data, "DATA_FILE", data_file)

    inserted_count = load_drug_data.load_drug_data()

    connection = sqlite3.connect(database_file)
    drugs = connection.execute(
        "SELECT generic_name, brand_name, active_ingredient FROM drugs"
    ).fetchall()
    connection.close()

    assert inserted_count == 1
    assert drugs == [
        ("test medicine", "TestBrand", "test ingredient")
    ]
