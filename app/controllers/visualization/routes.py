import os

import requests
from flask import Blueprint, render_template, redirect, url_for, request

template_folder = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'visualization')

visualization_bp = Blueprint('visualization', __name__, template_folder=template_folder)

API_BASE_URL = 'http://localhost:5000/api'


@visualization_bp.route('/')
def index():
    return render_template('index.html')


@visualization_bp.route('/tours')
def tours_list():
    response = requests.get(f'{API_BASE_URL}/tours/')
    if response.status_code == 200:
        tours = response.json()
    else:
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
            'pay_type': request.form['pay_type']
        }

        response = requests.post(f'{API_BASE_URL}/tours/', json=form_data)

        if response.status_code == 201:
            return redirect(url_for('visualization.tours_list'))

    return render_template('tour_create.html')


@visualization_bp.route('/tours/edit/<int:tour_id>', methods=['GET', 'POST'])
def edit_tour(tour_id):
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'date': request.form['date'],
            'cost': request.form['cost'],
            'popularity': request.form['popularity'],
            'pay_type': request.form['pay_type']
        }
        response = requests.put(f'{API_BASE_URL}/tours/{tour_id}', json=form_data)
        if response.status_code == 200:
            return redirect(url_for('visualization.tours_list'))

    response = requests.get(f'{API_BASE_URL}/tours/{tour_id}')
    if response.status_code == 200:
        tour = response.json()
    else:
        tour = {}

    return render_template('tour_edit.html', tour=tour)


@visualization_bp.route('/tours/delete/<int:tour_id>', methods=['GET', 'POST'])
def delete_tour(tour_id):
    response = requests.delete(f'{API_BASE_URL}/tours/{tour_id}')
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
            return redirect(url_for('visualization.users_list'))

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
            user_data = response.json()

            return redirect(url_for('visualization.users_list'))

        return 'Неверное имя пользователя или пароль', 401

    return render_template('login.html')


@visualization_bp.route('/admin/logout')
def logout():
    response = requests.post(f'{API_BASE_URL}/admin/logout')
    return redirect(url_for('visualization.login'))


@visualization_bp.route('/admin/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    response = requests.delete(f'{API_BASE_URL}/admin/{user_id}')
    if response.status_code == 204:
        return redirect(url_for('visualization.users_list'))
    return 'Ошибка при удалении пользователя', 400
