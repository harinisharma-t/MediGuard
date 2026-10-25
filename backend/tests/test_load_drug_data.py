
import json
import sqlite3

from database import load_drug_data


def create_test_database(database_file):
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


def test_load_drug_data_inserts_drug_records(tmp_path, monkeypatch):
    database_file = tmp_path / "test_mediguard.db"
    data_file = tmp_path / "drug_data.json"

    create_test_database(database_file)

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


def test_load_drug_data_skips_existing_drug_records(tmp_path, monkeypatch):
    database_file = tmp_path / "test_mediguard.db"
    data_file = tmp_path / "drug_data.json"

    create_test_database(database_file)

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

    first_count = load_drug_data.load_drug_data()
    second_count = load_drug_data.load_drug_data()

    connection = sqlite3.connect(database_file)
    drug_count = connection.execute(
        "SELECT COUNT(*) FROM drugs"
    ).fetchone()[0]
    connection.close()

    assert first_count == 1
    assert second_count == 0
    assert drug_count == 1


def test_load_drug_data_skips_records_without_generic_name(
    tmp_path, monkeypatch
):
    database_file = tmp_path / "test_mediguard.db"
    data_file = tmp_path / "drug_data.json"

    create_test_database(database_file)

    records = [
        {
            "brand_name": ["IncompleteBrand"],
            "generic_name": [],
            "active_ingredient": ["test ingredient"],
        }
    ]

    data_file.write_text(json.dumps(records), encoding="utf-8")

    monkeypatch.setattr(load_drug_data, "DATABASE_FILE", database_file)
    monkeypatch.setattr(load_drug_data, "DATA_FILE", data_file)

    inserted_count = load_drug_data.load_drug_data()

    connection = sqlite3.connect(database_file)
    drug_count = connection.execute(
        "SELECT COUNT(*) FROM drugs"
    ).fetchone()[0]
    connection.close()

    assert inserted_count == 0
    assert drug_count == 0


def test_load_drug_data_handles_missing_optional_fields(
    tmp_path, monkeypatch
):
    database_file = tmp_path / "test_mediguard.db"
    data_file = tmp_path / "drug_data.json"

    create_test_database(database_file)

    records = [{"generic_name": ["test medicine"]}]

    data_file.write_text(json.dumps(records), encoding="utf-8")

    monkeypatch.setattr(load_drug_data, "DATABASE_FILE", database_file)
    monkeypatch.setattr(load_drug_data, "DATA_FILE", data_file)

    inserted_count = load_drug_data.load_drug_data()

    connection = sqlite3.connect(database_file)
    drug = connection.execute(
        """
        SELECT generic_name, brand_name, active_ingredient
        FROM drugs
        """
    ).fetchone()
    connection.close()

    assert inserted_count == 1
    assert drug == ("test medicine", None, None)
