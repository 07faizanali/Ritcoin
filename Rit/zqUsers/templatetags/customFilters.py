from django import template
from zqUsers.models import ROIDailyCustomer
from datetime import datetime,timedelta,timezone

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

@register.filter
def modulo(value,arg):
    """
    Returns True if the value is even, False otherwise.
    """
    return value % arg

@register.filter
def mul_3(a, b,c,*args, **kwargs):
    """
    Returns True if the value is even, False otherwise.
    """
    return a*b*c
@register.filter
def hasROIDistributed(setDate,*args, **kwargs):
    """
    Returns True if the value is even, False otherwise.
    """
    # print()
    user_date = datetime.strptime(str(setDate)[:10], "%Y-%m-%d")
    
    return ROIDailyCustomer.objects.filter(roi_date=user_date).count() or 0

@register.filter(name='add_days')
def add_days(value, days):
    """
    Adds the given number of days to the value.
    :param value: The initial date
    :param days: The number of days to add
    :return: The new date with the days added
    """
    try:
        return value - timedelta(days=int(days))
    except (TypeError, ValueError):
        return value
    
    
@register.filter
def to_range(value):
    return range(1, value + 1)