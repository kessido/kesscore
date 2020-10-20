# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/04_random.ipynb (unless otherwise specified).

__all__ = ['RandomState']

# Cell
from .imports import *
from .functional import *

# Cell
def _rangechoice(len,size=None,nprs=None,replace=None,cum_weights=None,p=None):
    k,pyrs = ifnone(size,1),random.Random(nprs.random())
    if replace:
        assert p is None,'Should use cum_weights'
        if cum_weights is None: idx = nprs.randint(len,size=k)
        else:                   idx = pyrs.choices(range(len),k=k,cum_weights=cum_weights)
                                     # ^ here can also provide weight=p but performencewise not.
    else:
        assert cum_weights is None,'Should use p'
        if p is None: idx = pyrs.sample(range(len),k)
        else:         idx = nprs.choice(np.arange(len),size=k,replace=False,p=p)
    return idx[0] if size == None else idx

@delegates(_rangechoice, but=['len'])
def _customrangechoice(rng,**kwargs):
    idx = _rangechoice(len(rng),**kwargs)
    if not isinstance(idx, Iterable): return rng[idx]
    else: return np.asarray(idx) * rng.step + rng.start

@typedispatch
def _choicedsp(a,**kwargs):                  raise ValueError(f'unknown type {type(a)}')
@typedispatch
def _choicedsp(a:typing.Dict,**kwargs):      return _choicedsp(list(a), **kwargs)
@typedispatch
def _choicedsp(a:numbers.Integral,**kwargs): return _choicedsp(range(a),**kwargs)
@typedispatch
def _choicedsp(a:slice,**kwargs):            return _choicedsp(range(a.start,a.stop,a.step),**kwargs)
@typedispatch
def _choicedsp(a:range,**kwargs):            return _customrangechoice(a,**kwargs)
@typedispatch
def _choicedsp(a:(np.ndarray,torch.Tensor,L),**kwargs): idx=_rangechoice(len(a),**kwargs); return a[idx]
@typedispatch
def _choicedsp(a:(list, tuple),**kwargs):
    idx = _rangechoice(len(a),**kwargs);
    return a[idx] if kwargs['size'] is None else lmap(lambda i:a[i], idx)

@delegates(_rangechoice)
def _choice(a,nprs,size=None,**kwargs): return _choicedsp(a,nprs=nprs,size=size,**kwargs)

# Cell
@docs
class RandomState:
    def __init__(self, seed=None): self.rs=np.random.RandomState(seed=seed)
    def perm(self,a): return self.rs.permutation(range(a) if isinstance(a,numbers.Integral) else a)
    def choice(self,a,size=None,cum_weights=None): return _choice(a,self.rs,size=size,replace=True, cum_weights=cum_weights)
    def sample(self,a,size=None,p=None):           return _choice(a,self.rs,size=size,replace=False,p=p)
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