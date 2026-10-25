# MediGuard Progress Log

## Day 1
- Created the MediGuard project repository and local project structure.
- Set up the Python virtual environment and initial project documentation.
- Created the initial README with the project goals, architecture, technology stack, and safety notice.
## Day 2
- Researched drug interaction severity levels and documented Minor, Moderate, Major, and Contraindicated categories.
- Researched OpenFDA, RxNorm, and DrugBank as potential medication data sources.
- Documented the decision to prioritize publicly accessible sources for the prototype.

## Day 3
- Installed the Python packages required for API communication and data handling.
- Created and tested connection scripts for the OpenFDA Drug Label API and RxNorm.
- Documented the limitations of publicly available drug-allergy data and the planned prototype approach.

## Day 4
- Explored OpenFDA drug-label fields and RxNorm standardized medication fields using the existing API connection scripts.
- Identified the medication, interaction, safety, and identification fields required by the MediGuard prototype.
- Documented the initial internal data schema for normalized drugs, interactions, severity, and allergy information.

## Day 5
- Built an OpenFDA data collection pipeline that retrieves drug-label records in batches.
- Extracted medication names, active ingredients, interaction information, contraindications, warnings, and precautions.
- Collected a small working dataset for the next stages of MediGuard data processing.
## Day 29
- Added a test for mixed numeric and string drug names in interaction explanations.
- Verified the interaction explainer test suite: 30 tests passed.

## Day 30
- Added a test verifying that database initialization creates the required MediGuard tables.
- Tested database initialization using a temporary SQLite database.
- Confirmed that all 48 backend tests pass.

## Day 31
- Added a test for loading drug records into a temporary SQLite database.
- Verified that drug names and active ingredients are inserted correctly.
- Confirmed that all 49 backend tests pass.

## Day 33
- Added a test for drug records with missing optional fields.
- Verified that missing brand names and active ingredients are stored as `None`.
- Confirmed that all 52 backend tests pass.