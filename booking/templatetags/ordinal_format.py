from django import template

register = template.Library()

@register.filter
def ordinal_format(num):
    # https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    return "%d%s" % (num,"tsnrhtdd"[(num//10%10!=1)*(num%10<4)*num%10::4])