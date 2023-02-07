import datetime as dt
import re

from django.core import exceptions

from rest_framework.serializers import ValidationError


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


def username_validation(value):
    """
    Нельзя использовать имя пользователя me.
    Допускается использовать только буквы, цифры и символы @ . + - _.
    """
    if value == 'me':
        raise ValidationError('Нельзя использовать "me" как имя пользователя')
    checked_value = re.match('^[\\w.@+-]+', value)
    if checked_value is None or checked_value.group() != value:
        forbidden_simbol = value[0] if (
            checked_value is None
        ) else value[checked_value.span()[1]]
        raise ValidationError(f'Нельзя использовать символ {forbidden_simbol} '
                              'в username. Имя пользователя может содержать '
                              'только буквы, цифры и символы @ . + - _.')
    return value
