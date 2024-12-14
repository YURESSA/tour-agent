from flask import Flask, render_template
from flask_restx import Api

from app.controllers.tours.tours import tours_ns
from app.controllers.admin.admin import admin_ns

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'tour_agent'

api = Api(
    app,
    title='Tour agent API',
    prefix='/api',
    default='API',
    doc='/api/swagger',
    default_label='General operations'
)

api.add_namespace(admin_ns, path='/api/admin')
api.add_namespace(tours_ns, path='/api/tours')


@app.route('/')
def home():
    # todo: у меня не находил тут маршрут файла
    return '??'


if __name__ == "__main__":
    app.run()
