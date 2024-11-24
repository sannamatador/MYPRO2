import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config
from models import db, User, Product, Order


class UserModelView(ModelView):
    column_list = ('id', 'first_name', 'last_name', 'email')  # Поля для отображения в таблице
    form_columns = ('first_name', 'last_name', 'email')


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Order, db.session))

db.init_app(app)

with app.app_context():
    db.create_all()  # Создает таблицы в базе данных по моделям

if __name__ == '__main__':
    app.run(debug=True)
