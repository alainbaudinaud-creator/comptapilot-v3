import psycopg2
from werkzeug.security import check_password_hash

def get_conn():
    return psycopg2.connect(
        host='postgres',
        database='comptapilot',
        user='comptapilot',
        password='comptapilot'
    )

def login(email, password):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        'SELECT id,email,password_hash,role,company FROM users WHERE email=%s',
        (email,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    user = {
        'id': row[0],
        'email': row[1],
        'password_hash': row[2],
        'role': row[3],
        'company': row[4],
        'nom': row[1]
    }

    if password == user['password_hash']:
        return user

    try:
        if check_password_hash(user['password_hash'], password):
            return user
    except:
        pass

    return None

