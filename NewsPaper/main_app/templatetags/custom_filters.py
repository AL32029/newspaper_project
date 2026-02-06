import datetime

from django import template

from news.models import Post

register = template.Library()
forbidden_words = [
    "автосалоне",
    "представлена",
    "нового",
    "бренд",
    "технологии"
]


@register.filter
def censor(value):
    value_split = value.split()

    for index, value_str in enumerate(value_split):
        if value_str.lower() in forbidden_words:
            value_split[index] = value_str[0] + "*" * (len(value_str) - 1)

    return " ".join(value_split)


@register.filter
def format_date(datetime_str, format_str="%d.%m.%Y %H:%M:%S"):
    return datetime.datetime.strftime(datetime_str, format_str)

@register.filter()
def get_absolute_url_post(post: Post):
    return post.get_absolute_url()
