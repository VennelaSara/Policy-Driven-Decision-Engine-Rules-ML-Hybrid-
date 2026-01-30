def generate_explanation(rule_result: dict, ml_result: dict, data: dict) -> str:
    """
    Generate human-readable explanation for audit/compliance
    """
    explanation = []
    if rule_result["matched"]:
        explanation.append(f"Rule triggered: {rule_result['rule']}, action: {rule_result['action']}")
    else:
        explanation.append("No rules matched.")

    if ml_result["prediction"] is not None:
        explanation.append(f"ML model predicted: {ml_result['prediction']} with confidence {ml_result['confidence']:.2f}")
        if ml_result["confidence"] > 0.7:
            explanation.append("Decision flagged based on ML confidence threshold > 0.7")
    return " | ".join(explanation)
