import requests

OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def explore_openfda():
    params = {
        "limit": 1
    }

    response = requests.get(OPENFDA_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    data = explore_openfda()

    print("OpenFDA data exploration")
    print("=" * 30)

    results = data.get("results", [])

    if results:
        drug = results[0]

        print("\nAvailable fields:")
        for field in drug.keys():
            print("-", field)

        print("\nOpenFDA identification fields:")
        openfda = drug.get("openfda", {})

        for field, value in openfda.items():
            print(f"{field}: {value}")

        print("\nUseful MediGuard fields:")
        for field in [
            "active_ingredient",
            "drug_interactions",
            "contraindications",
            "warnings",
            "precautions",
        ]:
            value = drug.get(field)

            if value:
                print(f"\n{field}:")
                print(str(value)[:500])

    else:
        print("No records returned.")