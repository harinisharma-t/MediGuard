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
    example_names = [
        " Warfarin ",
        "WARFARIN",
        "warfarin   sodium",
    ]

    print("Drug name normalization examples:")

    for name in example_names:
        print(f"{name!r} -> {normalize_drug_name(name)!r}")