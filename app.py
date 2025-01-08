from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from app.controllers.admin.routes import admin_ns
from app.controllers.bookings.routes import bookings_ns
from app.controllers.tours.routes import tours_ns
from app.controllers.visualization.routes import visualization_bp
from app.extensions import db, jwt

allowed_origins = ["*"]

app = Flask(__name__, static_folder='app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tour_agent.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

app.config.update(SESSION_COOKIE_SECURE=False, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='None',
                  PERMANENT_SESSION_LIFETIME=86400)
CORS(app, supports_credentials=True, origins='*')

db.init_app(app)
jwt.init_app(app)

api = Api(app, doc='/api/')
api.add_namespace(admin_ns, path='/api/admin')
api.add_namespace(tours_ns, path='/api/tours')
api.add_namespace(bookings_ns, path='/api/bookings')


@api.doc(security='Bearer')
def configure_swagger(api):
    api.authorizations = {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    }
    api.security = [{'Bearer': []}]


configure_swagger(api)
app.register_blueprint(visualization_bp, url_prefix='/visualization')
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
