from app.engine.rules_engine import RulesEngine
from app.engine.ml_engine import MLEngine
from app.utils.explainability import generate_explanation
from app.db.redis_client import cache_get, cache_set
from app.models.audit import save_audit_log
from app.engine.policy_loader import PolicyLoader
import json

class DecisionEngine:
    """
    Combines Rules + ML to make hybrid decisions.
    """

    def __init__(self):
        # Dynamic policy loader with hot-reload
        self.policy_loader = PolicyLoader(reload_interval=10)
        self.rules_engine = RulesEngine(self.policy_loader.get_policies())
        self.ml_engine = MLEngine()

    def evaluate(self, data: dict) -> dict:
        # update rules dynamically
        self.rules_engine.load_policies(self.policy_loader.get_policies())

        cache_key = f"decision:{json.dumps(data, sort_keys=True)}"
        cached = cache_get(cache_key)
        if cached:
            return json.loads(cached)

        # Evaluate rules
        rule_result = self.rules_engine.evaluate(data)

        # Evaluate ML only if rules did not block
        if rule_result["action"] == "allow":
            ml_result = self.ml_engine.predict(data)
        else:
            ml_result = {"prediction": None, "confidence": None}

        # Combine rule + ML
        decision = self.combine(rule_result, ml_result)

        # Cache the decision
        cache_set(cache_key, json.dumps(decision), expire_seconds=300)

        # Generate explanation
        decision["explanation"] = generate_explanation(rule_result, ml_result, data)
        return decision

    def combine(self, rule_result: dict, ml_result: dict) -> dict:
        """
        Rule overrides ML; else ML confidence threshold used.
        """
        if rule_result["matched"]:
            return {
                "decision": rule_result["action"],
                "rule_matched": True,
                "ml_prediction": ml_result["prediction"]
            }

        if ml_result["confidence"] is not None and ml_result["confidence"] > 0.7:
            return {"decision": "flag", "rule_matched": False, "ml_prediction": ml_result["prediction"]}

        return {"decision": "allow", "rule_matched": False, "ml_prediction": ml_result["prediction"]}

    def save_audit(self, db, request_data: dict, decision_data: dict):
        save_audit_log(db, request_data, decision_data)
