from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields

from app.controllers.tours.models.tours import tour_crud

tours_ns = Namespace('tours', description='Операции с турами')

tour_model = tours_ns.model('Tour', {
    'id': fields.Integer(readOnly=True, description='ID тура'),
    'name': fields.String(required=True, description='Название тура'),
    'date': fields.String(required=True, description='Дата проведения тура'),
    'cost': fields.Float(required=True, description='Стоимость тура'),
    'popularity': fields.Integer(required=True, description='Популярность тура (по шкале от 1 до 10)'),
    'pay_type': fields.String(required=True, description='Тип оплаты (например, полный или в рассрочку)'),
    'country': fields.String(description='Страна'),
    'city': fields.String(description='Город'),
    'hotel': fields.String(description='Отель'),
})

filter_model = tours_ns.model('TourFilter', {
    'country': fields.String(description='Страна для фильтрации'),
    'city': fields.String(description='Город для фильтрации'),
    'hotel': fields.String(description='Отель для фильтрации'),
    'date': fields.String(description='Дата тура для фильтрации (формат YYYY-MM-DD)'),
})


@tours_ns.route('/')
class TourList(Resource):
    @jwt_required()
    @tours_ns.doc('get_all_tours')
    @tours_ns.param('country', 'Страна тура')
    @tours_ns.param('city', 'Город тура')
    @tours_ns.param('hotel', 'Отель тура')
    @tours_ns.param('date', 'Дата тура в формате YYYY-MM-DD')
    @tours_ns.param('min_cost', 'Минимальная стоимость тура')
    @tours_ns.param('max_cost', 'Максимальная стоимость тура')
    def get(self):
        """
        Получить список всех туров или фильтрованные туры по параметрам.
        """
        filters = {
            'country': request.args.get('country'),
            'city': request.args.get('city'),
            'hotel': request.args.get('hotel'),
            'date': request.args.get('date'),
            'min_cost': request.args.get('min_cost'),
            'max_cost': request.args.get('max_cost'),
        }
        filters = {key: value for key, value in filters.items() if value}
        tours = tour_crud.filter_tours(filters)

        return [
            {
                'id': t.id, 'name': t.name, 'date': t.date, 'cost': t.cost,
                'popularity': t.popularity, 'pay_type': t.pay_type,
                'country': t.country, 'city': t.city, 'hotel': t.hotel
            } for t in tours
        ], 200

    @jwt_required()
    @tours_ns.doc('create_tour')
    @tours_ns.expect(tour_model)
    def post(self):
        """
        Создать новый тур.
        """
        data = request.json
        new_tour = tour_crud.create(data)
        return {'message': 'Тур успешно создан', 'id': new_tour.id}, 201


@tours_ns.route('/<int:tour_id>')
class TourDetail(Resource):
    @tours_ns.doc('get_tour')
    def get(self, tour_id):
        """
        Получить информацию о туре по ID.
        """
        tour = tour_crud.read(tour_id)
        if tour:
            return {'id': tour.id, 'name': tour.name, 'date': tour.date, 'cost': tour.cost,
                    'popularity': tour.popularity, 'pay_type': tour.pay_type, 'country': tour.country,
                    'city': tour.city, 'hotel': tour.hotel}, 200
        return {'message': 'Тур не найден'}, 404

    @jwt_required()
    @tours_ns.doc('update_tour')
    @tours_ns.expect(tour_model)
    def put(self, tour_id):
        """
        Обновить информацию о туре.
        """
        data = request.json
        updated_tour = tour_crud.update(tour_id, data)
        if updated_tour:
            return {'message': 'Тур успешно обновлен'}, 200
        return {'message': 'Тур не найден'}, 404

    @jwt_required()
    @tours_ns.doc('delete_tour')
    def delete(self, tour_id):
        """
        Удалить тур по ID.
        """
        if tour_crud.delete(tour_id):
            return {'message': 'Тур успешно удален'}, 204
        return {'message': 'Тур не найден'}, 404
