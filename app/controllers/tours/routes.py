import sqlite3

from flask import Blueprint, request, jsonify, render_template

from app.controllers.tours.models.get_tours import *
from app.controllers.tours.models.update_cost import *
from app.controllers.tours.models.update_popularity import *
from app.controllers.tours.models.create_popular_table import *

tours_bp = Blueprint(
    'routes_bp', __name__
)


@tours_bp.route('/tours')
def admin_home():
    return "Hello Tour!"


def get_connection():
    return sqlite3.connect('data/tour_agent.db3')


@tours_bp.route('/get_tours', methods=['GET'])
def get_tours_by_pay_type():
    pay_type = request.args.get('pay_type', '0')
    with get_connection() as con:
        tours = get_tours(con, pay_type)
    return render_template('tours.html', tours=tours, pay_type=pay_type)


@tours_bp.route('/update_tour_cost', methods=['POST'])
def update_tour_cost():
    data = request.form
    pay_type = data.get('pay_type', '0')
    with get_connection() as con:
        updated_rows = update_cost(con, pay_type)
    if updated_rows > 0:
        return jsonify({"message": f"Успешно обновлено {updated_rows} стоимостей путёвок"}), 200
    else:
        return jsonify({"message": "Не найдено туров с таким типом оплаты для обновления"}), 400


@tours_bp.route('/update_popularity', methods=['POST'])
def update_popularity():
    with get_connection() as con:
        updated_rows = update_popularity_table(con)
    if updated_rows > 0:
        return jsonify({"message": f"Популярность обновлена для {updated_rows} туров"}), 200
    else:
        return jsonify({"message": "Популярность не обновлена, нет подходящих данных"}), 400


@tours_bp.route('/create_popular_routes', methods=['POST'])
def create_popular_routes():
    try:
        with get_connection() as con:
            added_rows = create_table_of_popular_routes(con)

        if added_rows:
            return jsonify({"message": f"Добавлена таблица популярных маршрутов с {added_rows} строками"}), 200
        else:
            return jsonify({"message": "Не добавлено ни одной строки в таблицу популярных маршрутов"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
