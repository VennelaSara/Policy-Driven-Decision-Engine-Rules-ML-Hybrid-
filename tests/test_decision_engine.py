from app.engine.decision_engine import DecisionEngine

def test_decision():
    engine = DecisionEngine()
    data = {"amount": 1500, "user_role": "employee", "department": "Finance"}
    result = engine.evaluate(data)
    assert result["decision"] == "flag"
    assert "Rule triggered" in result["explanation"]
