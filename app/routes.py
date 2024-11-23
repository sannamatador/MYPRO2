from flask import render_template, redirect, url_for, flash, request, session
from sqlalchemy.exc import NoResultFound

from app import db, app
from forms import RegistrationForm
from models import Product, Order, User


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()  # Получаем email из формы

        # Проверяем существование пользователя
        user = User.query.filter_by(email=email).first()  # Получаем первого пользователя с найденным email
        if user:  # Проверяем, существует ли пользователь
            session['user_id'] = user.id  # Сохраняем идентификатор пользователя в сессии
            return render_template('success1.html', first_name=user.first_name)  # Успешный вход
        else:
            # Обработка случая, когда пользователь не найден
            return render_template('login.html', error='Пользователь с таким email не найден.')

    # Если метод не POST, просто возвращаем страницу входа
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Удаление всех данных из сессии
    session.clear()  # или session.pop('ключ_сессии', None) для удаления конкретного ключа

    # Перенаправление на главную страницу
    return redirect(url_for('base'))  # Предполагая, что главная страница имеет маршрут 'index'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрировались!", "success")
        return redirect(url_for('base'))  # Перенаправление на главную страницу
    return render_template('register.html', form=form)


@app.route('/products')
def product():
    products = Product.query.all()  # Получение всех продуктов
    return render_template('product.html', products=products)


@app.route('/order', methods=['GET', 'POST'])
def order_view():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Если пользователь не авторизован, перенаправляем на страницу входа

    user_id = session['user_id']
    try:
        user = User.query.get(user_id)  # Получаем пользователя
        cart = session.get('cart', {})  # Получаем корзину из сессии

        # Получаем информацию о товарах в корзине
        order_items = []
        for product_id, quantity in cart.items():
            product = Product.query.get(product_id)  # Получаем продукт
            if product:
                order_items.append({'product': product, 'quantity': quantity})  # Добавляем товар в список

        return render_template('order_view.html', user=user, order_items=order_items)

    except NoResultFound:
        return redirect(url_for('login'))  # Если пользователь не найден, перенаправляем


@app.route('/order/create', methods=['POST'])
def order_create():
    if request.method == "POST":
        user_id = session.get('user_id')
        user = User.query.get(user_id)  # Получаем пользователя
        cart = session.get('cart', {})  # Получаем корзину из сессии

        if not cart:
            flash("Корзина пуста! Добавьте товары перед оформлением заказа.", "error")
            return redirect(url_for('product'))

        for product_id, quantity in cart.items():
            product = Product.query.get(product_id)  # Получаем продукт

            if product:
                # Создаем новый заказ
                order = Order(user=user, product=product, quantity=quantity, status='completed')
                order.save()

                # Уменьшаем количество товара после оформления заказа
                product.quantity -= quantity
                product.save()  # Сохранение обновленного количества товара

        # Очищаем корзину после оформления заказа
        session.pop('cart', None)
        flash("Ваш заказ оформлен! Спасибо за покупку.", "success")
        return redirect(url_for('order_success'))  # Перенаправляем на успешное оформление заказа

    return redirect(url_for('product'))  # Возвращаем, если метод не POST


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get(product_id)  # Получаем товар по ID

    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))  # Получаем количество из формы, по умолчанию 1
        if quantity > product.quantity:  # Проверка наличия товара
            flash(f"Недостаточно товара: {product.name}", "error")
            return redirect(url_for('product'))
        if quantity < 1:
            quantity = 1  # Убедимся, что количество положительное

        cart = session.get('cart', {})  # Получаем корзину из сессии или создаем новую
        if str(product_id) in cart:
            cart[str(product_id)] += quantity  # Увеличиваем количество, если товар уже есть в корзине
        else:
            cart[str(product_id)] = quantity  # Добавляем товар в корзину

        session['cart'] = cart  # Сохраняем корзину обратно в сессию

        flash(f'{product.name} добавлен в корзину!', "success")  # Сообщаем об успехе
        return redirect(url_for('product'))  # Возвращаем на страницу с товарами

    return redirect(url_for('product'))  # Если GET-запрос, возвращаем на страницу


@app.route('/order/success')
def order_success():
    return render_template('order_create.html')



