# MediGuard — System Architecture

## 1. Project Overview

MediGuard is a prototype drug interaction and allergy checker. It checks medication names against a local database, identifies possible allergy matches, and assigns a basic risk level based on the available information.

MediGuard is a decision-support prototype, not a medical diagnosis tool. Its results depend on the completeness and accuracy of its database.

## 2. Technology Stack

- **Language:** Python
- **Database:** SQLite
- **Data sources:** OpenFDA Drug Label API and RxNorm API
- **Drug name matching:** RapidFuzz
- **Testing:** pytest
- **Logging:** Python logging module

## 3. High-Level Architecture

```text
External Data Sources
(OpenFDA and RxNorm)
          |
          v
Data Collection and Normalization
          |
          v
JSON Dataset
          |
          v
SQLite Database
          |
          v
Core Checking Logic
  |          |
  v          v
Interaction  Allergy
Checker      Checker
  |          |
  +-----+----+
        |
        v
Risk Scoring
        |
        v
Results and Logs
```

This diagram represents the intended data flow. The current implementation has working data collection, database loading, interaction checking, allergy checking, risk scoring, and logging modules. A complete application interface and API are planned for later phases.

## 4. Main Project Modules

### Data Collection — `backend/services/`

- `openfda.py`: Tests connectivity to the OpenFDA API.
- `rxnorm.py`: Searches medication information using RxNorm.
- `collect_openfda_data.py`: Collects a small set of drug-label records and saves them as JSON.
- `drug_name_normalizer.py`: Normalizes medication names and builds brand-to-generic mappings.
- `drug_name_matcher.py`: Uses RapidFuzz to find approximate medication-name matches.
- `risk_scorer.py`: Assigns a basic risk level from interaction severity and allergy risk.

### Core Logic — `backend/core/`

- `interaction_checker.py`: Looks up medications and checks stored drug-interaction pairs. It also supports checking all pairs in a list of medications.
- `allergy_checker.py`: Checks a medication's generic name, brand name, and active ingredient for a possible match against a supplied allergen.

### Database — `database/`

- `schema.sql`: Defines patients, prescriptions, drugs, interactions, and allergies tables.
- `init_db.py`: Initializes the SQLite database.
- `load_drug_data.py`: Loads collected medication data into the database.
- `check_tables.py`: Displays database tables and stored drug records.

### Tests — `backend/tests/`

Automated tests cover risk scoring, interaction and allergy checks, fuzzy matching, and synthetic patient scenarios.

### Logging — `backend/utils/`

- `logger.py`: Configures application logging and writes runtime entries to `logs/mediguard.log`.

## 5. Database Design

The SQLite database contains five main tables:

- **patients:** Basic patient records.
- **drugs:** Generic names, brand names, and active ingredients.
- **prescriptions:** Links patients to prescribed drugs and records dosage and frequency.
- **interactions:** Stores drug pairs, severity, and descriptions.
- **allergies:** Stores patient allergen information and optional reaction details.

Foreign keys link prescriptions to patients and drugs, and allergies to patients.

## 6. Testing Strategy

The project uses pytest for automated verification.

Run the complete test suite from the project root:

```powershell
pytest backend/tests
```

Tests validate implemented behavior against the current local database and synthetic scenarios. Passing tests do not establish that the medication database is medically complete.

## 7. Current Limitations

- The interaction database contains only a small prototype dataset.
- An interaction not found in the local database does not prove that a drug combination is safe.
- Allergy matching is a basic text comparison, not a clinical allergy assessment.
- Risk scoring uses simplified rules.
- The complete API, LLM explanations, frontend, authentication, and deployment are planned for later stages.

## 8. Safety Notice

MediGuard is an educational prototype and must not replace a doctor or pharmacist. Users should consult a qualified healthcare professional about medication interactions, allergies, or treatment decisions.