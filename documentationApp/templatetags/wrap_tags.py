from django import template

register = template.Library()

@register.filter
def wrap(value, tag):
    return f"<{tag}>{value}</{tag}>"