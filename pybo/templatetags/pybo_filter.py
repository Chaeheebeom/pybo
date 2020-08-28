from django import template
import time
register = template.Library()

@register.filter
def sub(value, arg):
    return value-arg

@register.filter
def datetime(time):
    return time.strftime('%Y-%m-%d, %H:%M')