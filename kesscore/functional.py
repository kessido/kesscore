# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_functional.ipynb (unless otherwise specified).

__all__ = ['lmap', 'lzip', 'lfilter']

# Cell
from .imports import *
from functools import wraps

# Cell
def _listify(f=None):
    if f==None: return lisitify_decorator
    @wraps(f)
    def _inner(*args, **kwargs): return list(f(*args, **kwargs))
    return _inner

# Cell
lmap = _listify(map)
lzip = _listify(zip)
lfilter = _listify(filter)