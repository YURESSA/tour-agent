from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields

from app.controllers.admin.models.admin import admin_crud
from app.models.user import User

admin_ns = Namespace('admin', description='Операции администратора')
register_model = admin_ns.model('Register', {
    'username': fields.String(required=True, description='Имя пользователя'),
    'email': fields.String(required=True, description='Email пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя'),
})
login_model = admin_ns.model('Login', {
    'username': fields.String(required=True, description='Имя пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя'),
})


@admin_ns.route('/')
class AdminList(Resource):
    @jwt_required()
    def get(self):
        """
        Получить список всех пользователей.
        """
        users = admin_crud.read_all()
        data = [user.__dict__ for user in users]
        for d in data:
            d.pop('_sa_instance_state', None)
        return data, 200


@admin_ns.route('/<int:admin_id>')
class AdminDetail(Resource):
    @jwt_required()
    def get(self, admin_id):
        """
        Получить информацию о пользователе по ID.
        """
        user = admin_crud.read(admin_id)
        if user:
            data = user.__dict__
            data.pop('_sa_instance_state', None)
            return data, 200
        return {'message': 'Пользователь не найден'}, 404

    @jwt_required()
    def delete(self, admin_id):
        """
        Удалить пользователя по ID.
        """
        admin_crud.delete(admin_id)
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

        user = admin_crud.create(user_data)

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
            access_token = create_access_token(identity=str(user.id))
            return {'access_token': access_token}, 200
        return {'message': 'Неверное имя пользователя или пароль'}, 401


@admin_ns.route('/logout')
class UserLogout(Resource):
    def post(self):
        """
        Завершить сеанс пользователя.
        """
        return {'message': 'Выход выполнен успешно'}, 200


@admin_ns.route('/me')
class CurrentUser(Resource):
    @jwt_required()
    def get(self):
        """
        Получить информацию о текущем аутентифицированном пользователе.
        """
        user_id = get_jwt_identity()
        user = admin_crud.read(user_id)
        if user:
            user_data = {
                'username': user.username,
                'email': user.email
            }
            return user_data, 200
        return {'message': 'Пользователь не найден'}, 404
