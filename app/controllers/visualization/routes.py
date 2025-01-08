import os

import requests
from flask import Blueprint, render_template, redirect, url_for, request, session, flash

template_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'visualization')

visualization_bp = Blueprint('visualization', __name__, template_folder=template_folder)

API_BASE_URL = 'http://localhost:5000/api'


def get_headers():
    """Получить заголовки с токеном JWT из заголовков запроса."""
    headers = {'Content-Type': 'application/json'}
    # Получаем токен из заголовков Authorization
    token = request.headers.get('Authorization')
    if token:
        headers['Authorization'] = token
    return headers


@visualization_bp.route('/')
def index():
    return render_template('index.html')


@visualization_bp.route('/tours')
def tours_list():
    # Получаем параметры фильтрации из запроса
    country = request.args.get('country')
    city = request.args.get('city')
    hotel = request.args.get('hotel')
    date = request.args.get('date')
    min_cost = request.args.get('min_cost')
    max_cost = request.args.get('max_cost')

    params = {}
    if country:
        params['country'] = country
    if city:
        params['city'] = city
    if hotel:
        params['hotel'] = hotel
    if date:
        params['date'] = date
    if min_cost:
        params['min_cost'] = min_cost
    if max_cost:
        params['max_cost'] = max_cost
    response = requests.get(f'{API_BASE_URL}/tours/', headers=get_headers(), params=params)

    if response.status_code == 200:
        tours = response.json()
    else:
        flash('Ошибка загрузки туров.', 'error')
        tours = []

    return render_template('tours_list.html', tours=tours)


@visualization_bp.route('/tours/create', methods=['GET', 'POST'])
def create_tour():
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'date': request.form['date'],
            'cost': request.form['cost'],
            'popularity': request.form['popularity'],
            'pay_type': request.form['pay_type'],
            'country': request.form['country'],
            'city': request.form['city'],
            'hotel': request.form['hotel'],
        }

        response = requests.post(f'{API_BASE_URL}/tours/', json=form_data, headers=get_headers())
        if response.status_code == 201:
            return redirect(url_for('visualization.tours_list'))
        flash('Ошибка при создании тура.', 'error')

    return render_template('tour_create.html')


@visualization_bp.route('/tours/edit/<int:tour_id>', methods=['GET', 'POST'])
def edit_tour(tour_id):
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'date': request.form['date'],
            'cost': request.form['cost'],
            'popularity': request.form['popularity'],
            'pay_type': request.form['pay_type'],
            'country': request.form['country'],
            'city': request.form['city'],
            'hotel': request.form['hotel'],
        }
        response = requests.put(f'{API_BASE_URL}/tours/{tour_id}', json=form_data, headers=get_headers())
        if response.status_code == 200:
            return redirect(url_for('visualization.tours_list'))

    response = requests.get(f'{API_BASE_URL}/tours/{tour_id}')
    if response.status_code == 200:
        tour = response.json()
    else:
        tour = {}

    return render_template('tour_edit.html', tour=tour)


@visualization_bp.route('/tours/<int:tour_id>')
def tour_detail(tour_id):
    response = requests.get(f'{API_BASE_URL}/tours/{tour_id}', headers=get_headers())
    if response.status_code == 200:
        tour = response.json()
    else:
        tour = {}

    return render_template('tour_detail.html', tour=tour)


@visualization_bp.route('/tours/delete/<int:tour_id>', methods=['GET', 'POST'])
def delete_tour(tour_id):
    response = requests.delete(f'{API_BASE_URL}/tours/{tour_id}', headers=get_headers())
    if response.status_code == 204:
        return redirect(url_for('visualization.tours_list'))
    return 'Ошибка при удалении тура', 400


@visualization_bp.route('/users')
def users_list():
    response = requests.get(f'{API_BASE_URL}/admin')
    if response.status_code == 200:
        users = response.json()
    else:
        users = []
    return render_template('users_list.html', users=users)


@visualization_bp.route('/admin/<int:user_id>')
def admin_detail(user_id):
    response = requests.get(f'{API_BASE_URL}/admin/{user_id}')
    if response.status_code == 200:
        user = response.json()
    else:
        user = {}

    return render_template('user_detail.html', user=user)


@visualization_bp.route('/admin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = {
            'username': request.form['username'],
            'email': request.form['email'],
            'password': request.form['password']
        }

        response = requests.post(f'{API_BASE_URL}/admin/register', json=form_data)
        if response.status_code == 201:
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('visualization.login'))
        flash('Ошибка регистрации.', 'error')

    return render_template('register.html')


@visualization_bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = {
            'username': request.form['username'],
            'password': request.form['password']
        }

        response = requests.post(f'{API_BASE_URL}/admin/login', json=form_data)
        if response.status_code == 200:
            flash('Вы успешно вошли в систему.', 'success')
            return redirect(url_for('visualization.index'))

        flash('Неверные данные для входа.', 'error')

    return render_template('login.html')


@visualization_bp.route('/admin/logout')
def logout():
    session.pop('jwt_token', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('visualization.login'))


@visualization_bp.route('/admin/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    response = requests.delete(f'{API_BASE_URL}/admin/{user_id}')
    if response.status_code == 204:
        return redirect(url_for('visualization.users_list'))
    return 'Ошибка при удалении пользователя', 400
