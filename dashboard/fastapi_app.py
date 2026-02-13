from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Dummy pre-populated Riyadh Racecourse data ---
DUMMY_RIYADH = [
    {
        'race_number': 1,
        'distance_m': 1600,
        'class': 'Group 1',
        'horses': [
            {'name':'Badr Aslamawi','jockey':'Jockey 1','trainer':'Trainer 1'},
            {'name':'Yaroa','jockey':'Jockey 2','trainer':'Trainer 2'},
            {'name':'Almobeer','jockey':'Jockey 3','trainer':'Trainer 3'},
        ]
    },
    {
        'race_number': 2,
        'distance_m': 2000,
        'class': 'Group 2',
        'horses': [
            {'name':'Salfan','jockey':'Jockey 4','trainer':'Trainer 4'},
            {'name':'Fallat Kheir','jockey':'Jockey 5','trainer':'Trainer 5'},
        ]
    }
]

# --- AI Simulation Functions (Dummy placeholders) ---
def run_ai_predict(horses):
    """Simulate ensemble + RL predictions + bankroll probability"""
    predictions = []
    for h in horses:
        win_prob = np.random.uniform(0.3,0.8)
        stake_fraction = np.random.uniform(0.02,0.1)
        predictions.append({
            'name': h['name'],
            'jockey': h['jockey'],
            'trainer': h['trainer'],
            'win_prob': round(win_prob,2),
            'stake_fraction': round(stake_fraction,2)
        })
    return predictions

@app.get("/racecourse/{name}")
def get_racecourse(name:str):
    if name.lower() == "riyadh":
        races = DUMMY_RIYADH
    else:
        races = []
    # Run AI prediction for all horses
    for race in races:
        race['horses'] = run_ai_predict(race['horses'])
    return {"races": races}
