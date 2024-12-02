import pytest
import time
from flask import Flask
from models import db, User, Product, Order


@pytest.fixture
def test_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем базу данных в памяти
    app.config['TESTING'] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()  # Создание всех таблиц
        yield app

        db.drop_all()  # Удаление всех таблиц после тестов


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_user_creation(client):
    with client.application.app_context():
        start_time = time.perf_counter()
        user = User(first_name='John', last_name='Doe', email='john.doe@example.com')
        print(f"User  creation time: {(time.perf_counter() - start_time):.6f} seconds")
        db.session.add(user)
        db.session.commit()


def test_product_creation(client):
    with client.application.app_context():
        start_time = time.perf_counter()
        product = Product(name='Test Product', description='This is a test product', price=10.00, quantity=100)
        print(f"Product  creation time: {(time.perf_counter() - start_time):.6f} seconds")
        db.session.add(product)
        db.session.commit()



def test_order_creation(client):
    with client.application.app_context():
        start_time = time.perf_counter()
        user = User(first_name='Jane', last_name='Doe', email='jane.doe@example.com')
        product = Product(name='Test Product', description='This is a test product', price=10.00)

        db.session.add(user)
        db.session.add(product)
        db.session.commit()

        order = Order(user_id=user.id, product_id=product.id, product_name=product.name, quantity=2,
                      total_price=product.price * 2)
        print(f"Product  creation time: {(time.perf_counter() - start_time):.6f} seconds")
        db.session.add(order)
        db.session.commit()




