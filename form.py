from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

# Třída pro formulář
class TaskForm(FlaskForm):
    title = StringField(
        "Název úkolu",
        validators=[DataRequired(message="Toto pole je povinné."), Length(min=3, max=100)],
        render_kw={"placeholder": "Název úkolu"},
    )
    details = TextAreaField(
        "Podrobnosti", 
        validators=[Length(max=1000)],
        render_kw={"placeholder": "Podrobnosti"},
    )
    priority = SelectField(
        "Priorita",
        choices=[("high", "Vysoká priorita"), ("medium", "Střední priorita"), ("low", "Nízká priorita")],
        default="medium",
        validators=[DataRequired()],
    )


class LoginForm(FlaskForm):
    username = StringField("Uživatelské jméno", validators=[DataRequired()])
    password = PasswordField("Heslo", validators=[DataRequired()])


class RegistrationForm(LoginForm):
    confirm_password = PasswordField('Potvrďte heslo', validators=[DataRequired(), EqualTo('password')])
