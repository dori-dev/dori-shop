from django import template

register = template.Library()


def chunks(array: list, n: int):
    for index in range(0, len(array), n):
        yield array[index:index+n]


def add_comma(number: int) -> str:
    return f"{number:,}".replace(',', '،')


register.filter("chunks", chunks)
register.filter("comma", add_comma)
