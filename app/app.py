import os

from flask import Flask, redirect, request, url_for
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView

from config import Config
from models import db, User, Product, Order
from forms import RegistrationForm


class UserModelView(ModelView):
    form = RegistrationForm

    @expose('/user/new/', methods=['GET', 'POST'])
    def new_user(self):
        if request.method == 'POST':
            try:
                username = request.form.get('username')
                email = request.form.get('email')
                new_user = User(username=username, email=email)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('admin.user.index'))
            except Exception as e:
                return f"An error occurred: {str(e)}", 500  # Возвращаем сообщение об ошибке

        return self.render('new_user.html')


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
