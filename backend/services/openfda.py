import requests

OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def test_openfda_connection():
    params = {
        "limit": 1
    }

    response = requests.get(OPENFDA_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    data = test_openfda_connection()

    print("OpenFDA connection successful.")
    print("Records received:", len(data.get("results", [])))

    if data.get("results"):
        record = data["results"][0]
        print("Example drug:", record.get("openfda", {}).get("brand_name", ["Unknown"])[0])
        