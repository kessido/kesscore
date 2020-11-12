# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/08_script.ipynb (unless otherwise specified).

__all__ = []

# Cell
from .base import *

# Internal Cell
test_eq(f'{Param.__repr__!r}', "<slot wrapper '__repr__' of 'object' objects>")
#reason for need

# Internal Cell
def ParamRepr(self:Param):
    fields = get_all_public_attr(self)
    optstr = [f'{k}={v!r}'for k,v in fields.items() if v is not None
              and k not in ['type', 'set_default', 'kwargs']]
    if fields['type'] is not None:
        t = fields['type']
        if isinstance(t, type): s = f'type={t.__name__}'
        else: s = f'type=({", ".join((L(t).map(lambda x:x.__name__)))})'
        optstr = [s] + optstr
    return f'Param({", ".join(optstr)})'
Param.__repr__ = ParamRepr