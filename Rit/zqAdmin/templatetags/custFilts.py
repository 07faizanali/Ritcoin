from django import template

register = template.Library()

@register.simple_tag
def isEq(a, b,*args, **kwargs):
    """
    Custom filter to multiply two values.
    """
    return a==b
@register.simple_tag
def isNotEq(a, b,*args, **kwargs):
    """
    Custom filter to multiply two values.
    """
    return a!=b