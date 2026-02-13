from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.ai_modules import run_ai_predict

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DUMMY_DB = {
    'Riyadh': [
        {'race_number':1,'distance_m':1600,'class':'Group 1','horses':[{'name':'Badr Aslamawi','jockey':'J1','trainer':'T1'},
                                                                      {'name':'Yaroa','jockey':'J2','trainer':'T2'}]},
        {'race_number':2,'distance_m':2000,'class':'Group 2','horses':[{'name':'Salfan','jockey':'J3','trainer':'T3'},
                                                                      {'name':'Fallat Kheir','jockey':'J4','trainer':'T4'}]}
    ],
    'Greyville': [
        {'race_number':1,'distance_m':1200,'class':'Class 1','horses':[{'name':'Horse A','jockey':'Jockey 1','trainer':'Trainer 1'},
                                                                       {'name':'Horse B','jockey':'Jockey 2','trainer':'Trainer 2'}]},
        {'race_number':2,'distance_m':1400,'class':'Class 2','horses':[{'name':'Horse C','jockey':'Jockey 3','trainer':'Trainer 3'}]}
    ]
}

@app.get("/racecourse/{name}")
def get_racecourse(name: str):
    races = DUMMY_DB.get(name, [])
    for race in races:
        race['horses'] = run_ai_predict(race['horses'])
    return {"races": races}
