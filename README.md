# MediGuard

## Problem Statement

MediGuard is an AI-assisted drug interaction and allergy checker designed to help patients and caregivers understand potential medication risks.

The system cross-checks a patient's current and newly added medications against known drug-drug interactions and recorded allergies. It also uses an LLM to explain identified risks in simple, understandable language.

MediGuard is a decision-support and educational tool. It is not intended to diagnose medical conditions or prescribe, change, or stop medications.

## Goals

- Check for potential drug-drug interactions.
- Check medications against known patient allergies.
- Classify the severity of identified risks.
- Generate simple explanations of detected risks.
- Provide suggested questions that patients can discuss with a healthcare professional.
- Maintain patient prescription and allergy information.
- Provide a simple interface for checking medication safety.

## Planned Technology Stack

- Python
- FastAPI
- SQLite / PostgreSQL
- OpenFDA
- RxNorm
- scikit-learn
- LangChain
- LLM API
- React / Streamlit
- Docker
- GitHub Actions

## Planned Architecture

```text
User
  |
  v
Frontend
  |
  v
FastAPI Backend
  |
  +----------------------+
  |                      |
  v                      v
Drug Interaction     Allergy Checker
Engine                   |
  |                      |
  +----------+-----------+
             |
             v
        Risk Scoring
             |
             v
       LLM Explanation
             |
             v
     Safety-Focused Result

## Current Implementation

MediGuard currently includes:

- OpenFDA drug-label data collection and JSON storage
- RxNorm API connectivity
- Drug-name normalization and fuzzy matching
- SQLite database initialization and medication data loading
- Drug interaction lookup and multi-drug pair checking
- Allergy matching against medication names and active ingredients
- Basic risk scoring
- Logging and error handling
- Automated tests using pytest

## Project Architecture

The project is organized into separate modules for data collection, core checking logic, database operations, testing, and logging.

See [`docs/architecture.md`](docs/architecture.md) for the architecture diagram, module descriptions, database design, testing strategy, and current limitations.

## Running Tests

Activate the virtual environment in PowerShell if it is not already active:

```powershell
.\venv\Scripts\Activate.ps1
```

Run all automated tests:

```powershell
pytest backend/tests
```

## Safety Limitations

MediGuard is an educational prototype, not a medical diagnosis or treatment tool. Its local interaction dataset is limited, and a missing interaction result does not establish that a medication combination is safe. Consult a qualified healthcare professional for medication and allergy concerns.