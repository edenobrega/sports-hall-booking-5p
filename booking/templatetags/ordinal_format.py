from django import template

register = template.Library()


@register.filter
def ordinal_format(num):
    # https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    num = int(num)
    if 11 <= (num % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(num % 10, 4)]
    return str(num) + suffix
