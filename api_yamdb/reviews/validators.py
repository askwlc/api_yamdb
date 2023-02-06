import datetime as dt
from django.core import exceptions


def validate_year(year):
    now_year = dt.date.today()
    if year > now_year.year:
        raise ValueError(f'Некорректный год {year}')


def me_user(value):
    if value == 'me':
        raise exceptions.ValidationError(
            'Имя пользователя "me" не разрешено.'
        )
    return value
