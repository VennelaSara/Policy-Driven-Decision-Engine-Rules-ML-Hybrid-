import pytest
from app.engine.ml_engine import MLEngine

def test_ml_engine_prediction():
    ml_engine = MLEngine()
    features = {"feature1": 0.5, "feature2": 1.2, "feature3": -0.3, "feature4": 0.8, "feature5": 2.1}

    result = ml_engine.predict(features)
    assert "prediction" in result
    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1

    print("ML Engine Test Passed:", result)
