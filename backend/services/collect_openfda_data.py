import json
from pathlib import Path

import requests


OPENFDA_URL = "https://api.fda.gov/drug/label.json"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FOLDER = PROJECT_ROOT / "data"
OUTPUT_FILE = DATA_FOLDER / "openfda_drug_labels.json"


def collect_openfda_data(limit=10):
    collected_records = []
    skip = 0

    while len(collected_records) < limit:
        remaining_records = limit - len(collected_records)
        batch_size = min(5, remaining_records)

        params = {
            "limit": batch_size,
            "skip": skip,
        }

        response = requests.get(
            OPENFDA_URL,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        for record in results:
            openfda_info = record.get("openfda", {})

            cleaned_record = {
                "brand_name": openfda_info.get("brand_name", []),
                "generic_name": openfda_info.get("generic_name", []),
                "substance_name": openfda_info.get("substance_name", []),
                "active_ingredient": record.get("active_ingredient", []),
                "drug_interactions": record.get("drug_interactions", []),
                "contraindications": record.get("contraindications", []),
                "warnings": record.get("warnings", []),
                "precautions": record.get("precautions", []),
            }

            collected_records.append(cleaned_record)

        skip += len(results)

        if len(results) < batch_size:
            break

    return collected_records


def save_data(records):
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    print("Starting OpenFDA data collection...")

    records = collect_openfda_data(limit=10)

    save_data(records)

    print("Data collection completed.")
    print("Records collected:", len(records))
    print("Saved file:", OUTPUT_FILE)