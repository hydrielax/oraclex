#percentage.py

from django import template

register = template.Library()

@register.filter(name="percentage")
def percentage(value):
    if value:
        return str(round(value *100))+' %'
    else:
        return None