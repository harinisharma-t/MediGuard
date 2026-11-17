
import requests


OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def search_drug_labels(drug_name, limit=5):
    drug_name = drug_name.strip()

    if not drug_name:
        raise ValueError("Drug name cannot be empty.")

    if not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100.")

    params = {
        "search": (
            f'openfda.brand_name:"{drug_name}" OR '
            f'openfda.generic_name:"{drug_name}"'
        ),
        "limit": limit,
    }

    response = requests.get(
        OPENFDA_URL,
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def test_openfda_connection():
    response = requests.get(
        OPENFDA_URL,
        params={"limit": 1},
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    data = search_drug_labels("amoxicillin")

    records = data.get("results", [])

    print("OpenFDA search successful.")
    print("Records received:", len(records))

    if records:
        record = records[0]

        print(
            "Example drug:",
            record.get("openfda", {}).get(
                "brand_name",
                ["Unknown"],
            )[0],
        )
