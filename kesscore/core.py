# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['upfl', 'upfls', 'say_hello']

# Cell
def upfl(w:str):'Upper First Letter'; return w[:1].upper() + w[1:]
def upfls(ws:str):'Upper First Letters'; return ' '.join(map(upfl,ws.split(' ')))
def say_hello(to:str):"Say hello to somebody"; return f'Hello {upfls(to)}!'