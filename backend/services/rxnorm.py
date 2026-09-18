import requests

RXNORM_URL = "https://rxnav.nlm.nih.gov/REST/drugs.json"


def search_drug(drug_name):
    params = {
        "name": drug_name
    }

    response = requests.get(RXNORM_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    drug_name = "amoxicillin"

    data = search_drug(drug_name)

    print("RxNorm connection successful.")
    print("Search term:", drug_name)

    groups = data.get("drugGroup", {}).get("conceptGroup", [])

    if groups:
        print("RxNorm returned drug information.")
    else:
        print("No drug information found.")