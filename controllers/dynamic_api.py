from flask import Blueprint
from flask import jsonify
from flask import request
from database import get_db_connection

bp_dynamic_api = Blueprint("dynamic_api", __name__)

def sanitize(name):
    return "".join(
        c for c in name.lower()
        if c.isalnum() or c == "_"
    )

@bp_dynamic_api.route("/api/dynamic/<module>", methods=["GET"])
def dynamic_get(module):

    module = sanitize(module)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS dyn_{module} (
            id SERIAL PRIMARY KEY,
            data JSONB NOT NULL
        )
    ''')

    conn.commit()

    cur.execute(f'''
        SELECT id, data
        FROM dyn_{module}
        ORDER BY id DESC
    ''')

    rows = cur.fetchall()

    result = []

    for r in rows:

        item = r[1]
        item["id"] = r[0]

        result.append(item)

    cur.close()
    conn.close()

    return jsonify({
        "rows": result
    })

@bp_dynamic_api.route("/api/dynamic/<module>", methods=["POST"])
def dynamic_post(module):

    module = sanitize(module)

    payload = request.json or {}

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS dyn_{module} (
            id SERIAL PRIMARY KEY,
            data JSONB NOT NULL
        )
    ''')

    conn.commit()

    cur.execute(
        f'''
        INSERT INTO dyn_{module} (data)
        VALUES (%s)
        RETURNING id
        ''',
        [json.dumps(payload)]
    )

    new_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "success": True,
        "id": new_id
    })

@bp_dynamic_api.route("/api/dynamic/<module>/<int:item_id>", methods=["DELETE"])
def dynamic_delete(module, item_id):

    module = sanitize(module)

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        f'''
        DELETE FROM dyn_{module}
        WHERE id=%s
        ''',
        [item_id]
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "success": True
    })
