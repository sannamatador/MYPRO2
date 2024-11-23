from flask import Flask
from models import db
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db.init_app(app)

with app.app_context():
    db.create_all()  # Создает таблицы в базе данных по моделям

if __name__ == '__main__':
    app.run(debug=True)
