import psycopg2

def get_connection():
    return psycopg2.connect(
        database="sa_racing",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )

def insert_runner(runner_data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO runners 
        (race_id, horse_id, draw, weight, jockey, trainer, official_rating, form_score, finish_position)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, runner_data)
    conn.commit()
    conn.close()
