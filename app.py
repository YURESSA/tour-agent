from flask import Flask, render_template
from flask_login import LoginManager, login_required
from app.controllers.admin import admin_bp
from app.controllers.tours.routes import tours_bp
from app.controllers.tours import tours_bp1
from app.controllers.admin.admin import User

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'tour_agent'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(tours_bp)
app.register_blueprint(tours_bp1, url_prefix='/api')


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/login')
def get():
    return render_template('login.html')


@login_manager.user_loader
def load_user(user_id):
    return User(1, 'admin', '@@@@', '8888')


if __name__ == "__main__":
    app.run()
