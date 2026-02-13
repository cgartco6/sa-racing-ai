import xgboost as xgb
import pandas as pd

def train_gpu_model(X, y):
    model = xgb.XGBClassifier(
        tree_method="gpu_hist",
        predictor="gpu_predictor",
        max_depth=8,
        learning_rate=0.03,
        n_estimators=1000
    )
    model.fit(X, y)
    return model
