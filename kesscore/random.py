# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_random.ipynb (unless otherwise specified).

__all__ = ['RandomState']

# Cell
from .imports import *

# Cell
def _rangechoice(len,k=None,nprs=None,replace=None,cum_weights=None,p=None):
    pyrs = random.Random(nprs.random())
    if replace:
        assert p is None,'Should use cum_weights'
        if cum_weights is None: return nprs.randint(len,size=k)
        else:                   return pyrs.choices(range(len),k=k,cum_weights=cum_weights) # can use weight=p but performencewise not.
    else:
        assert cum_weights is None,'Should use p'
        if p is None: return pyrs.sample(range(len),k)
        else:         return nprs.choice(np.arange(len),size=k,replace=False,p=p)

@delegates(_rangechoice, but=['len'])
def _customrangechoice(rng, **kwargs):
    idx = _rangechoice(len(rng), **kwargs)
    return np.asarray(idx) * rng.step + rng.start

@delegates(_rangechoice, but=['k'])
def _choice(a, size=None, **kwargs):
    kwargs['k'] = ifnone(size, 1)
    if isinstance(a, typing.Dict):      a = list(a)
    if isinstance(a, numbers.Integral): a = range(a)
    if isinstance(a, slice):            a = range(a.start,a.stop,a.step)

    if   isinstance(a, range):                       a = _customrangechoice(a, **kwargs)
    elif isinstance(a, (list, tuple)):               a = [a[i] for i in _rangechoice(len(a),**kwargs)]
    elif isinstance(a, (np.ndarray,torch.Tensor,L)): a = a[_rangechoice(len(a),**kwargs)]
    else:                                            raise ValueError(f'unknown type {type(a)}')

    return a[0] if size is None else a

# Cell
@docs
class RandomState:
    def __init__(self, seed=None): self.rs=np.random.RandomState(seed=seed)
    def perm(self,a): return self.rs.permutation(range(a) if isinstance(a,numbers.Integral) else a)
    def choice(self,a,size=None,cum_weights=None): return _choice(a,size=size,nprs=self.rs,replace=True, cum_weights=cum_weights)
    def sample(self,a,size=None,p=None):           return _choice(a,size=size,nprs=self.rs,replace=False,p=p)
    def randn(self,size=None):return self.rs.randn(*size)
    def rand(self,size=None): return self.rs.random(size=size)
    def bool(self,size=None,p=0.5): return self.rand(size) < p
    def int(self,low,high=None,size=None,dtype=int): return self.rs.randint(low=low,high=high,size=size,dtype=dtype)
    _docs = dict(
        cls_doc = 'RandomState numpy\pythonic. if seed not given, randomly select one.',
        perm    = 'Return a random permutation',
        choice  = 'Get sample with replacements',
        sample  = 'Get sample w.o  replacements',
        randn   = 'Return floats in [0, 1)',
        rand    = 'Return floats from normal distribution N(0,1)',
        bool    = 'Return True with probability p',
        int     = 'Return int(ndarray) with in [low, high) ([0, low))',
    )