from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[DataRequired()])
    description = TextAreaField('Опис', validators=[DataRequired()])
    price = FloatField('Ціна ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    image = FileField('Зображення товару', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Дозволені лише зображення (jpg, png, jpeg, webp)!')
    ])
    submit = SubmitField('Зберегти товар')