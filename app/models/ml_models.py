import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from app.config import ML_MODELS_PATH

class MLModelManager:
    """
    Handles ML model training, saving, and loading.
    """

    def __init__(self, model_path=ML_MODELS_PATH):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
        else:
            self.train_dummy_model()

    def train_dummy_model(self):
        """
        Train a dummy RandomForest model for zero-cost ML
        """
        X, y = make_classification(
            n_samples=1000,
            n_features=5,
            n_informative=3,
            n_redundant=0,
            n_classes=2,
            random_state=42
        )
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X_train, y_train)
        self.save_model()

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(self.model, f)

    def predict(self, features: dict):
        X = np.array([list(features.values())])
        pred = int(self.model.predict(X)[0])
        conf = float(np.max(self.model.predict_proba(X)))
        return {"prediction": pred, "confidence": conf}
