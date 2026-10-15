def explain_interaction(interaction_result):
    """Explain an interaction result without overstating available evidence."""

    if not isinstance(interaction_result, dict):
        raise TypeError("interaction_result must be a dictionary.")

    drug_a = interaction_result.get("drug_a")
    drug_b = interaction_result.get("drug_b")

    drug_a = str(drug_a).strip() if drug_a is not None else ""
    drug_b = str(drug_b).strip() if drug_b is not None else ""

    drug_a = drug_a or "Unknown drug"
    drug_b = drug_b or "Unknown drug"

    raw_severity = interaction_result.get("severity")
    severity = (
        str(raw_severity).strip().lower()
        if raw_severity is not None
        else ""
    )

    description = interaction_result.get("description")
    if description is not None and not isinstance(description, str):
        raise TypeError("description must be a string or None.")

    description = description.strip() if description else ""

    if "evidence_status" in interaction_result:
        raw_evidence_status = interaction_result["evidence_status"]

        if not isinstance(raw_evidence_status, str):
            evidence_status = "unknown"
        else:
            evidence_status = (
                raw_evidence_status.strip().lower() or "unknown"
            )
    else:
        evidence_status = "reported" if severity else "unknown"

    if evidence_status not in {"reported", "not_found", "unknown"}:
        evidence_status = "unknown"

    if evidence_status == "not_found":
        severity = "unknown"
        risk_message = (
            "No interaction record was found in the available database. "
            "This does not establish that the medicines are safe to use together."
        )
    elif evidence_status == "unknown":
        severity = "unknown"
        risk_message = (
            "The interaction risk cannot be determined because there is "
            "insufficient evidence in this result. Consult a qualified "
            "healthcare professional."
        )
    elif severity in {"major", "contraindicated"}:
        risk_message = (
            "This result reports a potentially serious interaction. "
            "Seek advice from a qualified healthcare professional "
            "before taking these medicines together."
        )
    elif severity == "moderate":
        risk_message = (
            "This result reports a potentially significant interaction. "
            "Ask a qualified healthcare professional how to manage it."
        )
    elif severity == "minor":
        risk_message = (
            "This result reports a minor interaction in the available data. "
            "Ask a healthcare professional if you have concerns."
        )
    elif severity in {"none", "low"}:
        risk_message = (
            "No interaction was flagged by this result. "
            "This does not prove that taking these medicines together is safe."
        )
    else:
        severity = "unknown"
        risk_message = (
            "The interaction risk cannot be determined from the available "
            "information. Consult a qualified healthcare professional."
        )

    explanation = (
        f"Medicines: {drug_a} and {drug_b}\n"
        f"Reported severity: {severity.title()}\n"
        f"Evidence status: {evidence_status.replace('_', ' ').title()}\n"
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
