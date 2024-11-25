# Веб-приложение для ветеринарной аптеки

Это веб-приложение предназначено для ветеринарной аптеки, позволяющее пользователям регистрироваться, просматривать продукты и оформлять заказы. Проект разработан с использованием фреймворка Django и Django ORM.

## Содержание

- [Описание](#описание)
- [Функциональность](#функциональность)
- [Технологии](#технологии)
- [Установка](#установка)
- [Использование](#использование)
- [Вклад](#вклад)
- [Лицензия](#лицензия)

## Описание

Веб-приложение предоставляет пользователям возможность:

- Регистрация и авторизация по электронной почте
- Просмотр доступных товаров в аптеке
- Оформление заказов на покупку продуктов

Проект разработан с акцентом на удобство использования и простоту навигации.

## Функциональность

- **Регистрация пользователей**: Пользователи могут создать учетную запись, указав адрес электронной почты и пароль.
- **Авторизация**: Упрощенная система входа для пользователей.
- **Просмотр продуктов**: Пользователи могут просматривать список доступных товаров с описаниями и ценами.
- **Оформление заказов**: Возможность добавления товаров в корзину и оформления заказа.

## Технологии

- **Фреймворк**: Django
- **База данных**: SQLite (можно легко заменить на другую СУБД)
- **Язык программирования**: Python
- **HTML/CSS**: Для фронтенда
- **JavaScript**: Для интерактивности (если используется)

## Установка

1. Клонируйте репозиторий:


      bash
      git clone https://github.com/ваш_пользователь/ваш_репозиторий.git
      cd ваш_репозиторий
   
 
2. Создайте виртуальное окружение и активируйте его:

   
    python -m venv venv
    source venv/bin/activate   Для Linux/Mac
   
    venv\Scripts\activate   Для Windows
   
   
4. Установите зависимости:

    pip install -r requirements.txt
   
5. Примените миграции:

    python manage.py migrate
   
6. Запустите сервер:

    python manage.py runserver

7. Откройте браузер и перейдите по адресу http://127.0.0.1:8000/.

8. Использование
После запуска сервера вы можете зарегистрироваться и войти в систему, чтобы начать использовать приложение. Ознакомьтесь с доступными продуктами и попробуйте оформить заказ.

