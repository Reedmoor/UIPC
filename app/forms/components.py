from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class MotherboardForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    form = SelectField('Форм-фактор', choices=[
        ('ATX', 'ATX'),
        ('Micro-ATX', 'Micro-ATX'),
        ('Mini-ITX', 'Mini-ITX'),
        ('E-ATX', 'E-ATX')
    ], validators=[DataRequired()])
    soket = StringField('Сокет', validators=[DataRequired()])
    type_member = SelectField('Тип памяти', choices=[
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5')
    ], validators=[DataRequired()])
    interface = StringField('Интерфейсы', validators=[DataRequired()])
    submit = SubmitField('Добавить материнскую плату')

class PowerSupplyForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    power = IntegerField('Мощность (Вт)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Мощность должна быть положительным числом')
    ])
    type = SelectField('Тип', choices=[
        ('ATX', 'ATX'),
        ('SFX', 'SFX'),
        ('SFX-L', 'SFX-L')
    ], validators=[DataRequired()])
    submit = SubmitField('Добавить блок питания')

class ProcessorForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    soket = StringField('Сокет', validators=[DataRequired()])
    frequancy = FloatField('Частота (ГГц)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Частота должна быть положительным числом')
    ])
    power_use = IntegerField('Потребляемая мощность (Вт)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Потребляемая мощность должна быть положительным числом')
    ])
    submit = SubmitField('Добавить процессор')

class GraphicsCardForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    frequancy = FloatField('Частота (МГц)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Частота должна быть положительным числом')
    ])
    soket = StringField('Разъемы', validators=[DataRequired()])
    power_use = IntegerField('Потребляемая мощность (Вт)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Потребляемая мощность должна быть положительным числом')
    ])
    submit = SubmitField('Добавить видеокарту')

class CoolerForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    speed = IntegerField('Скорость вращения (об/мин)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Скорость вращения должна быть положительным числом')
    ])
    power_use = IntegerField('Потребляемая мощность (Вт)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Потребляемая мощность должна быть положительным числом')
    ])
    submit = SubmitField('Добавить кулер')

class RAMForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    frequancy = IntegerField('Частота (МГц)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Частота должна быть положительным числом')
    ])
    type_member = SelectField('Тип памяти', choices=[
        ('DDR4', 'DDR4'),
        ('DDR5', 'DDR5')
    ], validators=[DataRequired()])
    power_use = IntegerField('Потребляемая мощность (Вт)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Потребляемая мощность должна быть положительным числом')
    ])
    submit = SubmitField('Добавить оперативную память')

class HardDriveForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    capacity = IntegerField('Объем (ГБ)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Объем должен быть положительным числом')
    ])
    recording = IntegerField('Скорость записи (МБ/с)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Скорость записи должна быть положительным числом')
    ])
    reading = IntegerField('Скорость чтения (МБ/с)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Скорость чтения должна быть положительным числом')
    ])
    submit = SubmitField('Добавить жесткий диск')

class CaseForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена (руб.)', validators=[
        DataRequired(),
        NumberRange(min=0, message='Цена должна быть положительным числом')
    ])
    form = StringField('Поддерживаемые форм-факторы', validators=[DataRequired()])
    submit = SubmitField('Добавить корпус') 