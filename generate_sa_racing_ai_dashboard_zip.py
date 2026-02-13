import zipfile
import os

def generate_sa_racing_ai_dashboard_zip(output_path='sa_racing_ai_dashboard.zip'):
    # File structure and content
    files = {
        'backend/fastapi_app.py': """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from backend.ai_modules import run_ai_predict

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DUMMY_DB = {
    'Riyadh': [
        {'race_number':1,'distance_m':1600,'class':'Group 1','horses':[{'name':'Badr Aslamawi','jockey':'J1','trainer':'T1'}, {'name':'Yaroa','jockey':'J2','trainer':'T2'}]},
        {'race_number':2,'distance_m':2000,'class':'Group 2','horses':[{'name':'Salfan','jockey':'J3','trainer':'T3'}]}
    ],
    'Greyville': [
        {'race_number':1,'distance_m':1200,'class':'Class 1','horses':[{'name':'Horse A','jockey':'Jockey 1','trainer':'Trainer 1'},{'name':'Horse B','jockey':'Jockey 2','trainer':'Trainer 2'}]}
    ]
}

@app.get("/racecourse/{name}")
def get_racecourse(name:str):
    races = DUMMY_DB.get(name, [])
    for race in races:
        race['horses'] = run_ai_predict(race['horses'])
    return {"races": races}
""",
        'backend/ai_modules.py': """import numpy as np

def run_ai_predict(horses):
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
""",
        'db/schema.sql': """CREATE TABLE race_meetings (
    id SERIAL PRIMARY KEY,
    meeting_date DATE,
    racecourse VARCHAR(100),
    going VARCHAR(50),
    weather VARCHAR(50)
);
CREATE TABLE races (
    id SERIAL PRIMARY KEY,
    race_id INT,
    distance_m INT,
    class VARCHAR(50),
    surface VARCHAR(50)
);
CREATE TABLE horses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    sire VARCHAR(255),
    dam VARCHAR(255),
    age INT,
    sex VARCHAR(10)
);
CREATE TABLE runners (
    id SERIAL PRIMARY KEY,
    race_id INT,
    horse_id INT,
    draw INT,
    weight DECIMAL,
    jockey VARCHAR(255),
    trainer VARCHAR(255),
    official_rating INT,
    form_score DECIMAL,
    finish_position INT
);
CREATE TABLE odds_history (
    id SERIAL PRIMARY KEY,
    runner_id INT,
    timestamp TIMESTAMP,
    decimal_odds DECIMAL,
    source VARCHAR(50)
);
""",
        'db/loader.py': """import psycopg2

def populate_dummy_data():
    conn = psycopg2.connect(database='sa_racing', user='postgres', password='postgres', host='localhost', port=5432)
    cur = conn.cursor()
    cur.execute("INSERT INTO race_meetings (meeting_date,racecourse,going,weather) VALUES ('2026-02-14','Greyville','Good','Sunny');")
    cur.execute("INSERT INTO horses (name,sire,dam,age,sex) VALUES ('Horse A','Sire A','Dam A',5,'M'),('Horse B','Sire B','Dam B',4,'F');")
    cur.execute("INSERT INTO races (race_id,distance_m,class,surface) VALUES (1,1200,'Class 1','Turf');")
    cur.execute("INSERT INTO runners (race_id,horse_id,draw,weight,jockey,trainer,official_rating,form_score,finish_position) VALUES (1,1,1,56,'Jockey 1','Trainer 1',95,80,1),(1,2,2,54,'Jockey 2','Trainer 2',92,78,2);")
    cur.execute("INSERT INTO odds_history (runner_id,timestamp,decimal_odds,source) VALUES (1,'2026-02-14 10:00:00',4.5,'Dummy'),(2,'2026-02-14 10:00:00',6.0,'Dummy');")
    conn.commit()
    conn.close()
""",
        'frontend/dashboard.html': """<!DOCTYPE html>
<html lang='en'>
<head>
<meta charset='UTF-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>SA Racing AI Dashboard</title>
<style>
body{font-family:Arial,sans-serif;background:#f0f0f0;margin:0;padding:0}
header{background:#222;color:white;text-align:center;padding:1rem}
main{padding:1rem}
input[type=text]{width:250px;padding:0.5rem;margin-right:0.5rem}
button{padding:0.5rem 1rem;cursor:pointer}
.racecard{background:white;margin:1rem 0;padding:1rem;border-radius:8px;box-shadow:0 2px 5px rgba(0,0,0,0.2);cursor:move}
.race-title{font-weight:bold;margin-bottom:0.5rem}
.horse-widget{display:flex;justify-content:space-between;margin:0.25rem 0;padding:0.25rem 0.5rem;border-bottom:1px solid #eee}
.prob-bar{height:12px;background:#007bff;border-radius:5px}
.slider{width:100px}
</style>
</head>
<body>
<header><h1>SA Racing AI Dashboard</h1></header>
<main>
<div>
<input type='text' id='racecourseInput' placeholder='Enter Racecourse Name'>
<button onclick='loadRacecourse()'>Load Races</button>
</div>
<div id='raceContainer'></div>
</main>
<script>
function enableDragDrop(){const cards=document.querySelectorAll('.racecard');cards.forEach(card=>{card.draggable=true;card.ondragstart=e=>{e.dataTransfer.setData('text/plain',e.target.id)};card.ondragover=e=>e.preventDefault();card.ondrop=e=>{const draggedId=e.dataTransfer.getData('text/plain');const draggedEl=document.getElementById(draggedId);const dropTarget=e.target.closest('.racecard');if(draggedEl&&dropTarget&&draggedEl!==dropTarget){dropTarget.parentNode.insertBefore(draggedEl,dropTarget.nextSibling)}}})}
async function loadRacecourse(){const racecourse=document.getElementById('racecourseInput').value;const container=document.getElementById('raceContainer');container.innerHTML='<p>Loading...</p>';try{const res=await fetch(`http://127.0.0.1:8000/racecourse/${encodeURIComponent(racecourse)}`);const data=await res.json();container.innerHTML='';data.races.forEach((race,i)=>{const raceDiv=document.createElement('div');raceDiv.className='racecard';raceDiv.id='racecard'+i;raceDiv.innerHTML=`<div class='race-title'>Race ${race.race_number} - ${race.distance_m}m - ${race.class}</div>`;race.horses.forEach(horse=>{const hw=document.createElement('div');hw.className='horse-widget';hw.innerHTML=`<div>${horse.name} (${horse.jockey} / ${horse.trainer})</div><div style='width:200px;'><div class='prob-bar' style='width:${horse.win_prob*100}%'></div><small>${(horse.win_prob*100).toFixed(1)}%</small><input type='range' min='0' max='1' step='0.01' value='${horse.stake_fraction}' class='slider'></div>`;raceDiv.appendChild(hw);});container.appendChild(raceDiv);});enableDragDrop();}catch(err){console.error(err);container.innerHTML='<p style="color:red;">Failed to load races. Make sure backend is running.</p>'}}
</script>
</body>
</html>
""",
        'requirements.txt': """fastapi
uvicorn
numpy
psycopg2-binary
""",
        'README.md': """# SA Racing AI Dashboard

## Ubuntu 24.04
1. sudo apt update && sudo apt install -y python3 python3-venv python3-pip
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. uvicorn backend.fastapi_app:app --reload
6. Open frontend/dashboard.html in browser

## Windows 10 Pro
1. Install Python 3.11
2. python -m venv venv
3. venv\\Scripts\\activate
4. pip install -r requirements.txt
5. uvicorn backend.fastapi_app:app --reload
6. Open frontend/dashboard.html in browser
"""
    }

    # Create zip file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for path, content in files.items():
            zipf.writestr(path, content)

    print(f"Created full SA Racing AI Dashboard zip at {output_path}")

if __name__ == '__main__':
    generate_sa_racing_ai_dashboard_zip()
