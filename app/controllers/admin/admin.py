from flask import render_template
from flask_restx import Namespace, Resource, fields
from app.controllers.admin.models.admin import admin

admin_ns = Namespace(
    'admin',
    description='Admin operations'
)


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
