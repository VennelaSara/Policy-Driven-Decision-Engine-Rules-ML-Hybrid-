from app.db.database import SessionLocal
from app.models.policy import Policy
from sqlalchemy.orm import Session
import threading
import time
import json

class PolicyLoader:
    """
    Dynamically loads policies from DB and keeps them updated
    """

    def __init__(self, reload_interval: int = 10):
        self.policies = []
        self.reload_interval = reload_interval  # seconds
        self.lock = threading.Lock()
        self._load_policies()
        threading.Thread(target=self._periodic_reload, daemon=True).start()

    def _load_policies(self):
        db: Session = SessionLocal()
        try:
            policies_db = db.query(Policy).all()
            new_policies = []
            for p in policies_db:
                new_policies.extend(p.policy_json)  # flatten all policies
            with self.lock:
                self.policies = new_policies
        finally:
            db.close()

    def _periodic_reload(self):
        while True:
            time.sleep(self.reload_interval)
            self._load_policies()

    def get_policies(self):
        with self.lock:
            return self.policies.copy()
