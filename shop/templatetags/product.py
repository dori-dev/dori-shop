from django import template

register = template.Library()


def chunks(array: list, n: int):
    for index in range(0, len(array), n):
        yield array[index:index+n]


def add_comma(number: int) -> str:
    return f"{number:,}".replace(',', '،')


def generate_rating(rating_info: tuple) -> str:
    stars, half_stars, empty_stars = rating_info
    html = '<i class="fa fa-star-o"></i>\n'*empty_stars
    html += '<i class="fa fa-star-half-o"></i>\n'*half_stars
    html += '<i class="fa fa-star"></i>\n'*stars
    return html


register.filter("chunks", chunks)
register.filter("comma", add_comma)
register.filter("generate_rating", generate_rating)
