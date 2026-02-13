from fastapi import FastAPI
import pandas as pd
from prediction.predictor import rank_race

app = FastAPI()

@app.get("/predict")
def predict():
    # Example: load test race data
    df = pd.DataFrame([
        {"draw":1,"weight":56,"rating":95,"form_score":80,"odds":4.5,"name":"Horse A"},
        {"draw":2,"weight":54,"rating":92,"form_score":78,"odds":6.0,"name":"Horse B"}
    ])
    ranked = rank_race(model=None, race_df=df)
    return ranked.to_dict(orient="records")
