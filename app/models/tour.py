from app.extensions import db


class Tour(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    popularity = db.Column(db.Integer, nullable=False)
    pay_type = db.Column(db.String, nullable=False)

    country = db.Column(db.String, nullable=False, default='Не указано')
    city = db.Column(db.String, nullable=False, default='Не указано')
    hotel = db.Column(db.String, nullable=False, default='Не указано')