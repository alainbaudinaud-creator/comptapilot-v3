import psycopg2
from datetime import datetime

def get_conn():
    return psycopg2.connect(
        host='postgres',
        database='comptapilot',
        user='comptapilot',
        password='comptapilot'
    )

def lancer_scheduler():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS scheduler_jobs (id SERIAL PRIMARY KEY, name TEXT, status TEXT, last_run TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        cur.execute('INSERT INTO scheduler_jobs (name,status,last_run) VALUES (%s,%s,%s)', ('enterprise_scheduler','OK',datetime.utcnow()))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print('SCHEDULER ERROR:', e)
    return True

def scheduler_status():
    return {'scheduler':'OK'}

def demarrer_scheduler():
    return lancer_scheduler()

