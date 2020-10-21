# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/05_tensor.ipynb (unless otherwise specified).

__all__ = []

# Cell
from .imports import *
from functools import wraps

# Cell
@patch
def shape_is(self:Tensor,*size): return (*self.shape,)==(*size,)

# Cell
@patch
def asrt_sz(self:Tensor,*size): assert self.shape_is(*size), f'Expected tensor of shape {(*size,)} but got tensor of shape {(*self.shape,)}'; return self