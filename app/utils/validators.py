import jsonschema
from jsonschema import validate

def validate_policy(policy_json: list) -> bool:
    """
    Validates that policy JSON is correctly structured.
    Each rule should have:
      - condition: {field, op, value}
      - action: string
    """
    rule_schema = {
        "type": "object",
        "properties": {
            "condition": {
                "type": "object",
                "properties": {
                    "field": {"type": "string"},
                    "op": {"type": "string"},
                    "value": {}
                },
                "required": ["field", "op", "value"]
            },
            "action": {"type": "string"}
        },
        "required": ["condition", "action"]
    }

    try:
        for rule in policy_json:
            validate(instance=rule, schema=rule_schema)
        return True
    except jsonschema.ValidationError as e:
        print(f"Policy validation error: {e}")
        return False
