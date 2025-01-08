from app.extensions import db


class CRUD:
    def __init__(self, model):
        self.model = model

    def read_all(self):
        return self.model.query.all()

    def read(self, record_id):
        return self.model.query.get(record_id)

    def create(self, data):
        record = self.model(**data)
        db.session.add(record)
        db.session.commit()
        return record

    def delete(self, record_id):
        record = self.model.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()
            return True
        return False

    def update(self, record_id, data):
        record = self.read(record_id)
        if record:
            for key, value in data.items():
                setattr(record, key, value)
            db.session.commit()
            return record
        return None
