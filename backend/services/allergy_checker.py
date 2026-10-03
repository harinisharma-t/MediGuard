import sqlite3
from pathlib import Path


DATABASE_FILE = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "mediguard.db"
)


def find_drug(drug_name):
    """
    Find a drug using its generic name or brand name.
    """

    connection = sqlite3.connect(DATABASE_FILE)

    drug = connection.execute(
        """
        SELECT id, generic_name, brand_name, active_ingredient
        FROM drugs
        WHERE LOWER(generic_name) = LOWER(?)
           OR LOWER(brand_name) = LOWER(?)
        LIMIT 1;
        """,
        (drug_name, drug_name),
    ).fetchone()

    connection.close()

    return drug


def check_allergy(drug_name, allergen):
    """
    Check whether a patient's allergen matches
    the drug name, brand name, or active ingredient.
    """

    drug = find_drug(drug_name)

    if not drug:
        return {
            "found": False,
            "allergy_risk": False,
            "message": "Drug was not found in the database."
        }

    generic_name = drug[1]
    brand_name = drug[2]
    active_ingredient = drug[3]

    allergen = allergen.strip().lower()

    drug_information = [
        generic_name,
        brand_name,
        active_ingredient,
    ]

    for information in drug_information:
        if information and allergen in information.lower():
            return {
                "found": True,
                "allergy_risk": True,
                "matched_information": information,
                "message": (
                    f"Possible allergy match found for "
                    f"{drug_name} and {allergen}."
                ),
            }

    return {
        "found": True,
        "allergy_risk": False,
        "matched_information": None,
        "message": "No allergy match found."
    }
if __name__ == "__main__":
    result = check_allergy(
        "Betadine",
        "povidone-iodine"
    )

    print("Allergy check result:")
    print(result)