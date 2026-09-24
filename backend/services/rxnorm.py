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

    print("RxNorm data exploration")
    print("=" * 30)
    print("Search term:", drug_name)

    groups = data.get("drugGroup", {}).get("conceptGroup", [])

    if groups:
        print("\nRxNorm returned the following information:")

        for group in groups:
            print("\nTerm type:", group.get("tty"))

            concepts = group.get("conceptProperties", [])

            for concept in concepts[:5]:
                print(
                    f"RXCUI: {concept.get('rxcui')} | "
                    f"Name: {concept.get('name')} | "
                    f"TTY: {concept.get('tty')}"
                )
    else:
        print("No drug information found.")