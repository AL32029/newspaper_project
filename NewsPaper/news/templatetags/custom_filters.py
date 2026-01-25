from django import template

register = template.Library()
forbidden_words = [
    "автосалоне",
    "представлена",
    "нового",
    "бренд",
    "технологии"
]

@register.filter()
def censor(value):

    value_split = value.split()

    for index, value_str in enumerate(value_split):
        if value_str.lower() in forbidden_words:
            value_split[index] = value_str[0] + "*" * (len(value_str) - 1)

    return " ".join(value_split)