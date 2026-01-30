from pydantic import BaseModel
from typing import Optional, Any

class DecisionResponse(BaseModel):
    """
    Output payload from decision engine
    """
    decision: str                 # allow / flag / review
    rule_matched: bool            # Was a rule triggered?
    ml_prediction: Optional[Any]  # ML predicted class or None
    explanation: str              # Human-readable explanation

    class Config:
        schema_extra = {
            "example": {
                "decision": "flag",
                "rule_matched": True,
                "ml_prediction": 1,
                "explanation": "Rule triggered: {'condition': {'field': 'amount', 'op': '>', 'value': 1000}, 'action': 'flag'}, action: flag | ML model predicted: 1 with confidence 0.78 | Decision flagged based on ML confidence threshold > 0.7"
            }
        }
