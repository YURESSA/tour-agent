from flask import request, jsonify
from flask_login import login_required
from flask_restx import Namespace, Resource, fields
from app.models.tour import Tour, db

tours_ns = Namespace('tours', description='Операции с турами')

tour_model = tours_ns.model('Tour', {
    'id': fields.Integer(readOnly=True, description='ID тура'),
    'name': fields.String(required=True, description='Название тура'),
    'date': fields.String(required=True, description='Дата проведения тура'),
    'cost': fields.Float(required=True, description='Стоимость тура'),
    'popularity': fields.Integer(required=True, description='Популярность тура (по шкале от 1 до 10)'),
    'pay_type': fields.String(required=True, description='Тип оплаты (например, полный или в рассрочку)')
})


@tours_ns.route('/')
class TourList(Resource):
    @login_required
    @tours_ns.doc('get_all_tours')
    def get(self):
        """
        Получить список всех туров.
        """
        tours = Tour.query.all()
        return [{'id': t.id, 'name': t.name, 'date': t.date, 'cost': t.cost, 'popularity': t.popularity,
                 'pay_type': t.pay_type} for t in tours], 200

    @login_required
    @tours_ns.doc('create_tour')
    @tours_ns.expect(tour_model)
    def post(self):
        """
        Создать новый тур.
        """
        data = request.json
        new_tour = Tour(**data)
        db.session.add(new_tour)
        db.session.commit()
        return {'message': 'Тур успешно создан'}, 201


@tours_ns.route('/<int:tour_id>')
class TourDetail(Resource):
    @tours_ns.doc('get_tour')
    def get(self, tour_id):
        """
        Получить информацию о туре по ID.
        """
        tour = Tour.query.get(tour_id)
        if tour:
            return {'id': tour.id, 'name': tour.name, 'date': tour.date, 'cost': tour.cost,
                    'popularity': tour.popularity, 'pay_type': tour.pay_type}, 200
        return {'message': 'Тур не найден'}, 404

    @tours_ns.doc('update_tour')
    @tours_ns.expect(tour_model)
    def put(self, tour_id):
        """
        Обновить информацию о туре.
        """
        data = request.json
        tour = Tour.query.get(tour_id)
        if tour:
            for key, value in data.items():
                setattr(tour, key, value)
            db.session.commit()
            return {'message': 'Тур успешно обновлен'}, 200
        return {'message': 'Тур не найден'}, 404

    @tours_ns.doc('delete_tour')
    def delete(self, tour_id):
        """
        Удалить тур по ID.
        """
        tour = Tour.query.get(tour_id)
        if tour:
            db.session.delete(tour)
            db.session.commit()
            return {'message': 'Тур успешно удален'}, 204
        return {'message': 'Тур не найден'}, 404
