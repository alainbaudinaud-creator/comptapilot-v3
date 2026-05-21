@plan_comptable_routes.route('/', methods=['GET'])
@login_required
def get_plan_comptable():
    societe_id = request.args.get('societe_id')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    if societe_id:
        c.execute("""
            SELECT id, numero, libelle, type 
            FROM plan_comptable 
            WHERE societe_id = ?
        """, (societe_id,))
    else:
        c.execute("""
            SELECT id, numero, libelle, type 
            FROM plan_comptable
        """)

    rows = c.fetchall()
    conn.close()

    return jsonify([
        {
            "id": row[0],
            "numero": row[1],
            "libelle": row[2],
            "type": row[3]
        }
        for row in rows
    ])
