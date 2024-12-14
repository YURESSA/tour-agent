import flask
from flask import redirect, url_for, render_template
from flask_login import login_user, UserMixin, logout_user
from flask_restx import Namespace, Resource

from app.controllers.admin.models.admin import admin

admin_ns = Namespace(
    'admin',
    description='Admin operations'
)


class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return str(self.id)


@admin_ns.route('/')
class AdminController(Resource):
    def get(self):
        data = admin.read_all()
        return data, 200


@admin_ns.route('/<int:admin_id>')
@admin_ns.param('admin_id', 'int')
class AdminGetOneController(Resource):
    def get(self, admin_id):
        data = admin.read(admin_id)
        return data, 200

    def delete(self, admin_id):
        admin.delete(admin_id)
        return 204


@admin_ns.route('/login')
class UserLogin(Resource):
    def post(self):
        user = User(1, 'admin', '@@@@', '8888')
        login_user(user)
        flask.flash('Logged in successfully.')
        return {'success': True}


@admin_ns.route('/logout')
class UserLogout(Resource):
    def post(self):
        logout_user()
        return {'logout': True}
