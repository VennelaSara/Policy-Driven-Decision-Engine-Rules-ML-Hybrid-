import pickle
import numpy as np
from app.config import ML_MODELS_PATH

class MLEngine:
    """
    ML model loader and predictor.
    """

    def __init__(self, model_path=ML_MODELS_PATH):
        self.model = self.load_model(model_path)

    def load_model(self, path):
        try:
            with open(path, "rb") as f:
                model = pickle.load(f)
            return model
        except Exception:
            # fallback dummy model
            from sklearn.ensemble import RandomForestClassifier
            dummy = RandomForestClassifier()
            dummy.classes_ = np.array([0, 1])
            self.model = dummy
            return dummy

    def predict(self, features: dict) -> dict:
        """
        Predict risk/confidence score.
        """
        X = np.array([list(features.values())])
        try:
            pred = int(self.model.predict(X)[0])
            conf = float(np.max(self.model.predict_proba(X)))
        except Exception:
            pred = 0
            conf = 0.5
        return {"prediction": pred, "confidence": conf}
