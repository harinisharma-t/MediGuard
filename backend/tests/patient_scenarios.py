
PATIENT_SCENARIOS = [
    {
        "name": "Patient with a known drug allergy",
        "drugs": ["Betadine"],
        "allergens": [
            {
                "drug": "Betadine",
                "allergen": "povidone-iodine",
                "expected_allergy_risk": True,
            }
        ],
    },
    {
        "name": "Patient taking a known database drug",
        "drugs": ["naproxen"],
        "allergens": [],
    },
    {
        "name": "Patient with an unknown drug name",
        "drugs": ["unknown-drug"],
        "allergens": [
            {
                "drug": "unknown-drug",
                "allergen": "povidone-iodine",
                "expected_allergy_risk": False,
            }
        ],
    },
    {
        "name": "Patient taking multiple known drugs",
        "drugs": [
            "naproxen",
            "povidone-iodine",
            "silicea",
        ],
        "allergens": [],
    },
    {
        "name": "Patient with a generic-name allergy match",
        "drugs": ["povidone-iodine"],
        "allergens": [
            {
                "drug": "povidone-iodine",
                "allergen": "povidone-iodine",
                "expected_allergy_risk": True,
            }
        ],
    },
]