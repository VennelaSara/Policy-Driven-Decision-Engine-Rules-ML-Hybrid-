import pytest
from app.engine.rules_engine import RulesEngine

def test_rules_engine():
    policies = [
        {"condition": {"field": "amount", "op": ">", "value": 1000}, "action": "flag"},
        {"condition": {"field": "user_role", "op": "==", "value": "guest"}, "action": "review"},
        {"condition": {"field": "department", "op": "in", "value": ["HR", "Finance"]}, "action": "allow"}
    ]
    engine = RulesEngine(policies)

    # Test amount > 1000
    result = engine.evaluate({"amount": 1500, "user_role": "employee", "department": "Finance"})
    assert result["action"] == "flag"

    # Test user_role guest
    result = engine.evaluate({"amount": 100, "user_role": "guest", "department": "IT"})
    assert result["action"] == "review"

    # Test department in list
    result = engine.evaluate({"amount": 100, "user_role": "employee", "department": "Finance"})
    assert result["action"] == "allow"

    # Test no match
    result = engine.evaluate({"amount": 50, "user_role": "employee", "department": "IT"})
    assert result["action"] == "allow"

    print("Rules Engine Test Passed")
