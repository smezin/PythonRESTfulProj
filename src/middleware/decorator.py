from functools import wraps
from flask import request

def middleware_decorator():
    """Defining a decorator to use as middleware for specific route '/decorator'"""
    def _middleware_decorator(f):
        @wraps(f)
        def __middleware_decorator(*args, **kwargs):
            # 'before' logic goes here'
            print('decorator wrapper: before endpoint action')
            result = f(*args, **kwargs)
            print('nested f result: {}'.format(result))
            # 'after' logic goes here
            print('decorator wrapper : after endpoint action')
            return result
        return __middleware_decorator
    return _middleware_decorator