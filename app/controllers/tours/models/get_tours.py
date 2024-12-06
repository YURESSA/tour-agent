def get_tours(connection, pay_type):
    cur = connection.cursor()
    cur.execute('''
        SELECT 
            tr.trip_name AS name, 
            t.start_date AS date, 
            t.cost AS cost, 
            t.popularity AS popularity,
            t_p.pay_type AS pay_type
        FROM tour AS t
        JOIN trip AS tr ON t.trip_id = tr.trip_id
        JOIN tour_purchase AS t_p ON t.tour_id = t_p.tour_id
        WHERE t_p.pay_type = ?
    ''', (pay_type,))
    result = cur.fetchall()
    return [
        {
            "name": row[0],
            "date": row[1],
            "cost": row[2],
            "popularity": row[3],
            "pay_type": "Наличные" if row[4] == 0 else "Безналичные"
        }
        for row in result
    ]
