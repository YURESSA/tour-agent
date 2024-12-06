from app.utils.db_connection import get_connection


class CRUD:
    def __init__(self, model):
        if self.check_table(model):
            self.model = model

    @staticmethod
    def check_table(model):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM {model}')
        except Exception as e:
            print(e)
        else:
            return True

    def create(self, data):
        connection = get_connection()
        cursor = connection.cursor()
        fields = ', '.join(list(data.keys()))
        values = ', '.join(['?'] * len(data))
        cursor.execute(f'INSERT INTO {self.model} ({fields}) VALUES ({values})', list(data.values()))
        connection.commit()

    def read(self, _id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {self.model} WHERE id=?', (_id,))
        return cursor.fetchone()

    def read_all(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM {self.model}')
        return cursor.fetchall()

    def update(self, _id, data):
        connection = get_connection()
        cursor = connection.cursor()
        fields = ' = ?,'.join(list(data.keys()) + [' '])
        fields = fields[:-2]
        query = f'UPDATE {self.model} SET {fields} WHERE id=?'
        cursor.execute(query, list(data.values()) + [_id])
        connection.commit()

    def delete(self, _id):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM {self.model} WHERE id=?', (_id,))
        connection.commit()


if __name__ == '__main__':
    crud = CRUD('admin')
    crud.delete(1)
