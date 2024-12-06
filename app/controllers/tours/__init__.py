from flask import Blueprint
from flask_restx import Api

from .tours import tours_ns

tours_bp1 = Blueprint(
    'routes_bp1', __name__
)
api = Api(
    tours_bp1,
    title='Tours API',
    description='A RESTful API for Tours'
)

api.add_namespace(tours_ns, path='/tours')
