from flask import Flask, render_template

from app.controllers.admin import admin_bp
from app.controllers.tours.routes import tours_bp
from app.controllers.tours import tours_bp1

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'tour_agent'
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(tours_bp)
app.register_blueprint(tours_bp1, url_prefix='/api')


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
