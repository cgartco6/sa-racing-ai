import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import numpy as np

class EnsembleModel:
    def __init__(self):
        self.xgb = xgb.XGBClassifier(tree_method="gpu_hist")
        self.lgb = lgb.LGBMClassifier()
        self.cat = CatBoostClassifier(verbose=0)

    def fit(self, X, y):
        self.xgb.fit(X, y)
        self.lgb.fit(X, y)
        self.cat.fit(X, y)

    def predict_proba(self, X):
        p1 = self.xgb.predict_proba(X)[:,1]
        p2 = self.lgb.predict_proba(X)[:,1]
        p3 = self.cat.predict_proba(X)[:,1]
        return (p1+p2+p3)/3
