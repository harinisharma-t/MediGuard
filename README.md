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