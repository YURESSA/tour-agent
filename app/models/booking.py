from app.extensions import db
from app.models.tour import Tour


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    passport_data = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    consent = db.Column(db.Boolean, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    tour = db.relationship('Tour', back_populates='bookings')


Tour.bookings = db.relationship('Booking', back_populates='tour', cascade='all, delete-orphan')
