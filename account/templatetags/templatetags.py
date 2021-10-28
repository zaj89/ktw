from django import template
from event.models import Event

register = template.Library()


@register.filter
def minus(value1, value2):
    return value1 - value2


@register.filter
def plus(value1, value2):
    return value1 + value2


register.tag('limit_wyczerpany', Event.limit_wyczerpany)