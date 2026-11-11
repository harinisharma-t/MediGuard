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

## Day 34
- Added a test for inserting multiple drug records in one operation.
- Verified that three valid drug records are inserted successfully.
- Confirmed that all 53 backend tests pass.

## Day 35
- Added a test for mixed valid and invalid drug records.
- Verified that valid records are inserted while records without generic names are skipped.
- Confirmed that all 54 backend tests pass.

## Day 36
- Added a test for duplicate drug records within the same dataset.
- Verified that duplicate records are inserted only once.
- Confirmed that all 55 backend tests pass.

## Day 37
- Added a test for different brands sharing the same generic drug name.
- Verified that both brand records are inserted separately.
- Confirmed that all 56 backend tests pass.

## Day 38
- Added a test for the same brand name associated with different generic medicines.
- Verified that both drug records are inserted separately.
- Confirmed that all 57 backend tests pass.

## Day 39
- Added a test to verify how the drug loader handles multiple values in OpenFDA fields.
- Verified that the first brand name, generic name, and active ingredient are selected.
- Confirmed that all 58 backend tests pass.

## Day 40
- Added a test to verify repeated execution of the drug data loader.
- Confirmed that the first execution inserts the record and the second inserts no duplicates.
- Verified that all 59 backend tests pass.

## Day 41
- Added a test for OpenFDA records containing empty name lists.
- Verified that records without a generic name are skipped while valid records are inserted.
- Confirmed that all 60 backend tests pass.

## Day 42
- Added a test for handling an empty OpenFDA dataset.
- Verified that the loader returns zero and inserts no drug records.
- Confirmed that all 61 backend tests pass.

## Day 43
- Improved drug data loading by skipping non-dictionary records.
- Added tests for malformed records containing None, strings, and numbers.
- Verified that valid records continue to load correctly.
- Confirmed that all 62 backend tests pass.

## Day 44
- Improved drug data validation for malformed OpenFDA field values.
- Added checks to ensure brand names, generic names, and active ingredients are lists.
- Added a test covering non-list field values.
- Confirmed that all 63 backend tests pass.
## Day 45
- Improved database connection cleanup using a try/finally block.
- Added a test verifying that the SQLite connection closes after an insertion error.
- Confirmed that all 64 backend tests pass.

## Day 46
- Improved drug data loading by validating the top-level JSON dataset structure.
- Added a test to verify that non-list datasets return zero without opening a database connection.
- Confirmed that all 65 backend tests pass.

## Day 47
- Improved drug data validation to reject whitespace-only generic names.
- Added a test verifying that blank generic names are skipped.
- Confirmed that all 66 backend tests pass.

## Day 48
- Improved drug data loading to handle missing JSON files safely.
- Added error handling for invalid JSON content.
- Added two tests covering missing files and invalid JSON.
- Confirmed that all 68 backend tests pass.
