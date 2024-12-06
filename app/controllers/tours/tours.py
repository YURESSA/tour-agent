from flask import render_template
from flask_restx import Namespace, Resource, fields

tours_ns = Namespace(
    'tours',
    description='Tours'
)

tours_model = tours_ns.model('Tour', {
    'id': fields.Integer(readonly=True, description='tour id'),
})


@tours_ns.route('/<int:id>')
class Tours(Resource):
    def put(self, id):
        return 'ДДДДДД'
