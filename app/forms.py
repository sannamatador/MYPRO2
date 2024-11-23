from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from models import User


class RegistrationForm(FlaskForm):
    first_name = StringField("Имя", validators=[DataRequired()])
    last_name = StringField("Фамилия", validators=[DataRequired()])
    email = StringField("Электронная почта", validators=[DataRequired(), Email()])

    submit = SubmitField("Зарегистрироваться")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Этот адрес электронной почты уже используется.")
