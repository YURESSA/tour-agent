from flask import request
from flask_restx import Namespace, Resource, fields
from app.controllers.bookings.models.bookings import bookings_crud

bookings_ns = Namespace('bookings', description='Операции с заявками на туры')

booking_model = bookings_ns.model('Booking', {
    'tour_id': fields.Integer(required=True, description='ID тура'),
    'full_name': fields.String(required=True, description='ФИО'),
    'passport_data': fields.String(required=True, description='Паспортные данные'),
    'phone': fields.String(required=True, description='Телефон'),
    'email': fields.String(required=True, description='Email'),
    'consent': fields.Boolean(required=True, description='Согласие на оформление заявки'),
    'number_of_people': fields.Integer(required=True, description='Количество человек')
})


@bookings_ns.route('/')
class BookingList(Resource):
    @bookings_ns.doc('get_all_bookings')
    def get(self):
        """
        Получить список всех заявок.
        """
        bookings = bookings_crud.read_all()
        return [{'id': b.id, 'tour_id': b.tour_id, 'full_name': b.full_name, 'passport_data': b.passport_data,
                 'phone': b.phone, 'email': b.email, 'consent': b.consent} for b in bookings], 200

    @bookings_ns.doc('create_booking')
    @bookings_ns.expect(booking_model)
    def post(self):
        """
        Оформить заявку на тур.
        """
        data = request.json
        booking = bookings_crud.create(data)
        return {'message': 'Заявка успешно оформлена', 'id': booking.id}, 201
