# utils.py

def int_to_base36(num):
    """Convert an integer to a base36 string."""
    chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    sign = ''
    if num < 0:
        sign = '-'
        num = -num
    result = []
    while num > 0:
        num, remainder = divmod(num, 36)
        result.append(chars[remainder])
    return sign + ''.join(reversed(result)) or '0'

def base36_to_int(base36):
    """Convert a base36 string to an integer."""
    return int(base36, 36)
