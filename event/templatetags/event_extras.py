from  django import template

register = template.Library()


@register.filter
def in_category(masters, category):
    return masters.filter(category=category)