# MediGuard Domain Research

## Drug Interaction Severity Levels

### Minor
A minor interaction may cause a limited or small effect. It generally does not require a major change in treatment, although monitoring may still be appropriate.

### Moderate
A moderate interaction may worsen a patient's condition or reduce the effectiveness of a medication. It may require additional monitoring or a change in therapy.

### Major
A major interaction can cause significant harm to the patient. The combination may need to be avoided or used only with strong clinical precautions.

### Contraindicated
A contraindicated combination should not be used together because the potential risks are considered unacceptable.

> Note: These severity categories are simplified for the MediGuard prototype and should not replace professional clinical judgment.

## Data Sources

### OpenFDA

OpenFDA provides public APIs for FDA datasets, including drug labeling information.

Potential MediGuard uses:
- Drug names
- Active ingredients
- Warnings and precautions
- Contraindications
- Drug interaction information when available in drug labels

Website: https://open.fda.gov/

### RxNorm

RxNorm is a standardized medication terminology maintained by the U.S. National Library of Medicine.

Potential MediGuard uses:
- Standardized generic drug names
- Brand and generic relationships
- Drug normalization
- Standard medication identifiers

Website: https://www.nlm.nih.gov/research/umls/rxnorm/

### DrugBank

DrugBank provides extensive drug and drug-interaction information. However, its data is subject to licensing and access restrictions.

For the MediGuard prototype, we will prioritize publicly accessible sources such as OpenFDA and RxNorm rather than assuming DrugBank data can be freely downloaded or redistributed.

Website: https://go.drugbank.com/

## Initial Data Source Decision

For the initial MediGuard prototype:

1. RxNorm will be used primarily for drug name normalization and standardized medication information.
2. OpenFDA will be used for publicly available drug labeling and safety information.
3. DrugBank will be treated as a reference for understanding the domain and as a potential licensed source rather than assuming its data is freely available.
## Why These Sources?

MediGuard needs reliable and standardized medication information. RxNorm is useful for identifying and normalizing medications, while OpenFDA provides publicly accessible safety and drug-label information.

Using multiple sources also reduces dependence on a single dataset and allows the system to combine standardized drug information with safety-related information.

For this academic prototype, publicly accessible sources are preferred so that the project can be developed and demonstrated without relying on restricted commercial datasets.
## Drug Allergy Data Decision

A clean public dataset specifically representing confirmed patient drug allergies was not identified for the initial prototype.

Public pharmacovigilance sources contain adverse drug reaction reports, but an adverse reaction should not automatically be interpreted as a confirmed drug allergy.

Therefore, MediGuard will initially use a small, clearly documented allergy mapping for prototype testing. This mapping will be treated as demonstration data rather than real patient data.

Future versions could integrate a properly licensed clinical terminology or allergy knowledge source.