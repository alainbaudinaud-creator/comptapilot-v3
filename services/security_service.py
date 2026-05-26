import psycopg2

def get_conn():
    return psycopg2.connect(
        host='postgres',
        database='comptapilot',
        user='comptapilot',
        password='comptapilot'
    )

def audit(user_email, action, ip=None):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO security_logs (user_email, action, ip) VALUES (%s, %s, %s)',
            (user_email, action, ip)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print('AUDIT ERROR:', e)

def require_login():
    return True

