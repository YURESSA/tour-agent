def create_table_of_popular_routes(connection):
    cur = connection.cursor()

    cur.execute('''
                    CREATE TABLE IF NOT EXISTS popular_routes (
                        route_id INTEGER PRIMARY KEY,
                        trip_name TEXT NOT NULL,
                        demand_percentage REAL NOT NULL
                    )
                ''')
    connection.commit()
    cur.execute('DELETE FROM popular_routes')
    connection.commit()
    cur.execute('''
                    INSERT INTO popular_routes (route_id, trip_name, demand_percentage)
                    SELECT trip_id, trip_name, demand_percentage
                    FROM trip
                    WHERE demand_percentage > 75
                ''')
    connection.commit()

    added_rows = cur.rowcount
