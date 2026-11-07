
import json
import sqlite3
from pathlib import Path


DATABASE_FOLDER = Path(__file__).resolve().parent
DATABASE_FILE = DATABASE_FOLDER / "mediguard.db"

PROJECT_ROOT = DATABASE_FOLDER.parent
DATA_FILE = PROJECT_ROOT / "data" / "openfda_drug_labels.json"


def load_drug_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    connection = sqlite3.connect(DATABASE_FILE)

    inserted_count = 0

    try:
        for record in records:
            if not isinstance(record, dict):
                continue

            brand_names = record.get("brand_name", [])
            generic_names = record.get("generic_name", [])
            active_ingredients = record.get("active_ingredient", [])

            brand_name = (
                brand_names[0]
                if isinstance(brand_names, list) and brand_names
                else None
            )

            generic_name = (
                generic_names[0]
                if isinstance(generic_names, list) and generic_names
                else None
            )

            active_ingredient = (
                active_ingredients[0]
                if isinstance(active_ingredients, list) and active_ingredients
                else None
            )

            if not generic_name:
                continue

            existing_drug = connection.execute(
                """
                SELECT id
                FROM drugs
                WHERE generic_name = ?
                  AND brand_name IS ?
                """,
                (generic_name, brand_name),
            ).fetchone()

            if existing_drug:
                continue

            connection.execute(
                """
                INSERT INTO drugs (
                    generic_name,
                    brand_name,
                    active_ingredient
                )
                VALUES (?, ?, ?)
                """,
                (
                    generic_name,
                    brand_name,
                    active_ingredient,
                ),
            )

            inserted_count += 1

        connection.commit()

    finally:
        connection.close()

    return inserted_count


if __name__ == "__main__":
    inserted_count = load_drug_data()

    print("Drug data loading completed.")
    print("New drug records inserted:", inserted_count)
