from django import template

register = template.Library()

# @register.filter(nam='mult')


# def my_tag(a, b, *args, **kwargs):
#     warning = kwargs['warning']
#     profile = kwargs['profile']
#     ...
#     return ...
@register.simple_tag
def mul(a, b,*args, **kwargs):
    """
    Custom filter to multiply two values.
    """
    return a * b

@register.simple_tag
def divd(a, b,*args, **kwargs):
    """
    Custom filter to multiply two values.
    """
    return float(a)/float(b)
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