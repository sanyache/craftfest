from  django import template
from django.core.paginator import Page

register = template.Library()


@register.filter
def in_category(masters, category):
    if isinstance(masters, Page):
        return masters
    return masters.filter(category=category)
