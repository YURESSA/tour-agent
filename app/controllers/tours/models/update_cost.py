def update_cost(connection, pay_type):
    cur = connection.cursor()
    cur.execute('''
                UPDATE tour
                SET cost = cost * 1.15
                WHERE tour_id IN (
                    SELECT tour_id
                    FROM tour_purchase
                    WHERE pay_type = ?
                )
            ''', (pay_type,))
    connection.commit()
    return cur.rowcount
