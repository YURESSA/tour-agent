from flask import request, flash
from flask_login import login_user, logout_user
from flask_restx import Namespace, Resource, fields

from app.controllers.constructor.crud import CRUD
from app.models.user import User

admin_ns = Namespace('admin', description='Операции администратора')
register_model = admin_ns.model('User', {
    'username': fields.String(required=True, description='Имя пользователя'),
    'email': fields.String(required=True, description='Электронная почта пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя'),
})
login_model = admin_ns.model('User', {
    'username': fields.String(required=True, description='Имя пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя'),
})
user_crud = CRUD(User)


@admin_ns.route('/')
class AdminList(Resource):
    def get(self):
        """
        Получить список всех пользователей.
        """
        users = user_crud.read_all()
        data = [user.__dict__ for user in users]
        for d in data:
            d.pop('_sa_instance_state', None)
        return data, 200


@admin_ns.route('/<int:admin_id>')
class AdminDetail(Resource):
    def get(self, admin_id):
        """
        Получить информацию о пользователе по ID.
        """
        user = user_crud.read(admin_id)
        if user:
            data = user.__dict__
            data.pop('_sa_instance_state', None)
            return data, 200
        return {'message': 'Пользователь не найден'}, 404

    def delete(self, admin_id):
        """
        Удалить пользователя по ID.
        """
        user_crud.delete(admin_id)
        return {'message': 'Пользователь успешно удален'}, 204


@admin_ns.route('/register')
class UserRegister(Resource):
    @admin_ns.doc('register_user')
    @admin_ns.expect(register_model, validate=True)
    def post(self):
        """
        Зарегистрировать нового пользователя.
        """
        data = request.json
        if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
            return {'message': 'Пользователь с таким именем или email уже существует'}, 400

        user = User(username=data['username'], email=data['email'])
        user.set_password(data['password'])
        user_data = {
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash
        }

        user = user_crud.create(user_data)

        return {'message': 'Пользователь успешно зарегистрирован', 'id': user.id}, 201


@admin_ns.route('/login')
class UserLogin(Resource):
    @admin_ns.doc('user_login')
    @admin_ns.expect(login_model, validate=True)
    def post(self):
        """
        Авторизовать пользователя.
        """
        data = request.json
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            login_user(user)
            flash('Успешный вход.')
            return {'message': 'Успешный вход'}, 200
        return {'message': 'Неверное имя пользователя или пароль'}, 401


@admin_ns.route('/logout')
class UserLogout(Resource):
    def post(self):
        """
        Завершить сеанс пользователя.
        """
        logout_user()
        return {'message': 'Выход выполнен успешно'}, 200
