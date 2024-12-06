from flask import render_template
from flask_restx import Namespace, Resource, fields

admin_ns = Namespace(
    'admin',
    description='Admin operations'
)


@admin_ns.route('/')
class AdminController(Resource):
    def get(self):
        return render_template('admin.html')
