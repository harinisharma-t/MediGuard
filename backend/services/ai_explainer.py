
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from backend.services.interaction_explainer import explain_interaction


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
DEFAULT_MODEL = "meta/llama-3.1-8b-instruct"


def generate_ai_explanation(interaction_result):
    """Generate a cautious AI explanation with a rule-based fallback."""

    fallback = explain_interaction(interaction_result)

    api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        return {
            "explanation": fallback,
            "provider": "rule_based",
            "used_fallback": True,
        }

    model = os.getenv("NVIDIA_MODEL", DEFAULT_MODEL)

    system_prompt = (
        "You explain medication interaction information in simple language. "
        "Use only the supplied interaction data. Do not invent medical facts, "
        "interaction severity, or evidence. Do not diagnose, prescribe, or "
        "recommend starting, stopping, or changing medicines. Never claim "
        "that a medicine combination is safe. If evidence is missing or "
        "unknown, clearly preserve that uncertainty. Keep the explanation "
        "short, clear, and educational. Always include a reminder to consult "
        "a qualified healthcare professional."
    )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": (
                    "Explain this interaction result:\n"
                    + json.dumps(interaction_result, ensure_ascii=False)
                ),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 400,
    }

    try:
        response = requests.post(
            NVIDIA_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()
        explanation = (
            data["choices"][0]["message"]["content"].strip()
        )

        if not explanation:
            raise ValueError("AI returned an empty explanation.")

        return {
            "explanation": explanation,
            "provider": "nvidia",
            "used_fallback": False,
        }

    except (
        requests.RequestException,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
    ):
        return {
            "explanation": fallback,
            "provider": "rule_based",
            "used_fallback": True,
        }
