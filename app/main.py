from fastapi import FastAPI, Depends
from app.schemas.request import DecisionRequest
from app.schemas.response import DecisionResponse
from app.engine.decision_engine import DecisionEngine
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter
from typing import List
from app.models.policy import Policy
from app.models.audit import AuditLog

app = FastAPI(
    title="Policy-Driven Decision Engine",
    description="Hybrid Rules + ML Decision Engine with explainable audits",
    version="1.0.0"
)

decision_engine = DecisionEngine()

@app.post("/evaluate", response_model=DecisionResponse)
async def evaluate_policy(request: DecisionRequest, db: Session = Depends(get_db)):
    """
    Evaluate a request using policy rules + ML hybrid engine.
    """
    decision_result = decision_engine.evaluate(request.dict())
    # Save audit
    decision_engine.save_audit(db, request.dict(), decision_result)
    return decision_result


# --- Admin Dashboard ---
admin_router = APIRouter(prefix="/admin", tags=["Admin"])

# View all policies
@admin_router.get("/policies", response_model=List[dict])
def list_policies(db: Session = Depends(get_db)):
    policies = db.query(Policy).all()
    return [{"id": p.id, "name": p.name, "version": p.version, "policy_json": p.policy_json} for p in policies]

# View audit logs
@admin_router.get("/audits", response_model=List[dict])
def list_audits(db: Session = Depends(get_db)):
    audits = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    return [{"id": a.id, "request_data": a.request_data, "decision_data": a.decision_data, "timestamp": a.timestamp} for a in audits]

# Add or update a policy
@admin_router.post("/policies")
def add_policy(name: str, policy_json: dict, db: Session = Depends(get_db)):
    existing = db.query(Policy).filter_by(name=name).first()
    if existing:
        existing.policy_json = policy_json
        existing.version += 1
    else:
        new_policy = Policy(name=name, policy_json=policy_json)
        db.add(new_policy)
    db.commit()
    return {"status": "success", "policy_name": name}

app.include_router(admin_router)
