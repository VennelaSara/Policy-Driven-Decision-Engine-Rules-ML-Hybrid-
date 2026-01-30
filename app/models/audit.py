from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from app.db.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_data = Column(JSON)
    decision_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

def save_audit_log(db, request_data, decision_data):
    from sqlalchemy.orm import Session
    log = AuditLog(request_data=request_data, decision_data=decision_data)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
