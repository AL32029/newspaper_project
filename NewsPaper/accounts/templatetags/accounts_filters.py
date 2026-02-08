import datetime

from django import template

register = template.Library()


@register.filter
def format_date(datetime_str, format_str="%d.%m.%Y %H:%M:%S"):
    """
    Форматирование даты
    """
    return datetime.datetime.strftime(datetime_str, format_str)
