# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01_images.ipynb (unless otherwise specified).

__all__ = ['show_image', 'show_images']

# Cell
from .imports import *
from .functional import *
from functools import wraps

# Cell
@typedispatch
def _convert(im:(str,Path)):     return load_image(im)
@typedispatch
def _convert(im:(torch.Tensor)): return to_image(im)

def _converts(im): return L(list(im)).map(_convert)

def _a2f(f, g):
    'apply `g` to first arguments of `f`'
    @wraps(f)
    def _inner(x, *args, **kwargs): return f(g(x),*args,**kwargs)
    return _inner

show_image        = _a2f(show_image,        _convert)
show_images       = _a2f(show_images,       _converts)