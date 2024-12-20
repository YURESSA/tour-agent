from app.extensions import db


class Tour(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    popularity = db.Column(db.String(50))
    pay_type = db.Column(db.String(50))
