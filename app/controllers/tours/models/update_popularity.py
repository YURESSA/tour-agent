def update_popularity_table(connection):
    cur = connection.cursor()
    cur.execute('''
                UPDATE tour
                SET popularity = CASE
                    WHEN (SELECT demand_percentage FROM trip WHERE trip.trip_id = tour.trip_id) > 75 THEN 'популярный'
                    WHEN (SELECT demand_percentage FROM trip WHERE trip.trip_id = tour.trip_id) BETWEEN 50 AND 75 THEN 'средний'
                    ELSE 'не очень'
                END
            ''')
    connection.commit()
    return cur.rowcount
