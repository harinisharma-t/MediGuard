import re


def normalize_drug_name(drug_name):
    """
    Normalize a drug name for consistent matching.
    """

    if not drug_name:
        return ""

    normalized_name = drug_name.strip().lower()

    normalized_name = re.sub(r"\s+", " ", normalized_name)

    return normalized_name


def build_drug_name_mapping(records):
    """
    Build a mapping between brand names and generic names.
    """

    drug_mapping = {}

    for record in records:
        brand_names = record.get("brand_name", [])
        generic_names = record.get("generic_name", [])

        normalized_generics = [
            normalize_drug_name(name)
            for name in generic_names
            if name
        ]

        for brand_name in brand_names:
            normalized_brand = normalize_drug_name(brand_name)

            if normalized_brand and normalized_generics:
                drug_mapping[normalized_brand] = normalized_generics[0]

    return drug_mapping


if __name__ == "__main__":
    import json
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    data_file = project_root / "data" / "openfda_drug_labels.json"

    with open(data_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    drug_mapping = build_drug_name_mapping(records)

    print("Drug name normalization completed.")
    print("Records processed:", len(records))
    print("Brand-to-generic mappings:", len(drug_mapping))

    for brand_name, generic_name in list(drug_mapping.items())[:5]:
        print(f"{brand_name} -> {generic_name}")