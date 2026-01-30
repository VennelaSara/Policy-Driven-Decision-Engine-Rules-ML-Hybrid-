import operator
from typing import Any, Dict, Union

# Supported operators
OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "in": lambda a, b: a in b,
    "not_in": lambda a, b: a not in b,
}

class RulesEngine:
    """
    Evaluates rules dynamically from JSON with conflict resolution.
    """

    def __init__(self, policies: list = None):
        self.policies = policies or []

    def load_policies(self, policies: list):
        self.policies = policies

    def evaluate_rule(self, data: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """
        Evaluate single rule against data.
        """
        condition = rule.get("condition", {})
        field = condition.get("field")
        op = condition.get("op")
        value = condition.get("value")

        data_value = data.get(field)
        if data_value is None:
            return False  # missing field fails safely

        if op not in OPS:
            raise ValueError(f"Unsupported operator: {op}")

        return OPS[op](data_value, value)

    def evaluate(self, data: Dict[str, Any]) -> Dict[str, Union[bool, str]]:
        """
        Evaluate all policies and resolve conflicts:
        - Most specific rule (more conditions) wins
        - First match if equal specificity
        """
        matched_rules = []
        for rule in self.policies:
            if self.evaluate_rule(data, rule):
                matched_rules.append(rule)

        if not matched_rules:
            return {"matched": False, "action": "allow", "rule": None}

        # Resolve conflict by specificity (more conditions)
        matched_rules.sort(key=lambda r: len(r.get("condition", {})), reverse=True)
        winning_rule = matched_rules[0]
        return {"matched": True, "action": winning_rule.get("action"), "rule": winning_rule}
