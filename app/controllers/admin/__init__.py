from flask import Blueprint
from flask_restx import Api

from .admin import admin_ns

admin_bp = Blueprint(
    'admin_bp', __name__
)
api = Api(
    admin_bp,
    title='Tour Agent Admin API',
    description='Admin API for Tour Agent',
)

api.add_namespace(admin_ns, path='/admin')
