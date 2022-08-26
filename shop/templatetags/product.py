from django import template

register = template.Library()


def chunks(array: list, n: int):
    for index in range(0, len(array), n):
        yield array[index:index+n]


register.filter("chunks", chunks)
