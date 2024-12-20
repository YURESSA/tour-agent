from flask import Flask
from flask_restx import Api

from app.controllers.admin.routes import admin_ns
from app.controllers.tours.routes import tours_ns
from app.controllers.visualization.routes import visualization_bp
from app.extensions import db, login_manager
from app.models.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tour_agent.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='None',
                  PERMANENT_SESSION_LIFETIME=86400)
db.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


api = Api(app, doc='/api/')
api.add_namespace(admin_ns, path='/api/admin')
api.add_namespace(tours_ns, path='/api/tours')

app.register_blueprint(visualization_bp, url_prefix='/visualization')
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
