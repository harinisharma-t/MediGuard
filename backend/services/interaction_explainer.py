
def explain_interaction(interaction_result):
    """Convert a drug interaction result into a readable explanation."""

    if not isinstance(interaction_result, dict):
        raise TypeError("interaction_result must be a dictionary.")

    severity = str(
        interaction_result.get("severity", "unknown")
    ).strip().lower()

    drug_a = interaction_result.get("drug_a", "Unknown drug")
    drug_b = interaction_result.get("drug_b", "Unknown drug")
    description = interaction_result.get("description")

    if severity in {"major", "contraindicated"}:
        risk_message = (
            "This result indicates a potentially serious interaction. "
            "Seek advice from a qualified healthcare professional "
            "before taking these medicines together."
        )
    elif severity == "moderate":
        risk_message = (
            "This result indicates a potentially significant interaction. "
            "Ask a qualified healthcare professional how to manage it."
        )
    elif severity == "minor":
        risk_message = (
            "This result indicates a minor interaction in the available data. "
            "Ask a healthcare professional if you have concerns."
        )
    elif severity in {"none", "low"}:
        risk_message = (
            "No interaction was flagged by this result. "
            "This does not prove that taking these medicines together is safe."
        )
    else:
        risk_message = (
            "The interaction risk cannot be determined from the available "
            "information. Consult a qualified healthcare professional."
        )

    explanation = (
        f"Medicines: {drug_a} and {drug_b}\n"
        f"Reported severity: {severity.title()}\n"
        f"Explanation: {risk_message}"
    )

    if description:
        explanation += f"\nAvailable details: {description}"

    explanation += (
        "\n\nSafety note: This is an educational explanation, "
        "not medical advice. Do not start, stop, or change medication "
        "without consulting a qualified healthcare professional."
    )

    return explanation
