from pydantic import BaseModel
from typing import Dict, Any

class DecisionRequest(BaseModel):
    """
    Input payload for decision engine
    Can include any domain-specific fields (amount, user_role, content, etc.)
    """
    data: Dict[str, Any]

    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "amount": 1200,
                    "user_role": "employee",
                    "department": "Finance",
                    "content": "This is a test message"
                }
            }
        }
