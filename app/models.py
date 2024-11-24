from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'  # Укажите название таблицы

    id = db.Column(db.Integer, primary_key=True)  # Добавьте первичный ключ
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Product(db.Model):
    __tablename__ = 'products'  # Укажите название таблицы

    id = db.Column(db.Integer, primary_key=True)  # Добавьте первичный ключ
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=0)  # Количество на складе
    status = db.Column(db.String(20), default='available')  # Убедитесь, что есть это поле

    # Определение возможных статусов
    STATUS_CHOICES = {
        'available': 'Доступен',
        'unavailable': 'Недоступен'
    }

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = 'orders'  # Укажите название таблицы

    id = db.Column(db.Integer, primary_key=True)  # Добавьте первичный ключ
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=1)  # Количество
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Время создания заказа
    total_price = db.Column(db.Numeric(10, 2), default=0.00)  # Общая цена

    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))

    def __repr__(self):
        return f"Order {self.id} by {self.user.first_name} - Status: {self.status}"
