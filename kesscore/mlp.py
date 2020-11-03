# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_mlp.ipynb (unless otherwise specified).

__all__ = ['MultiActs', 'Linear', 'MLP']

# Cell
from .base import *
import copy

# Cell
class MultiActs(Module):
    '''Given acts=[a0,a1] and v=[v0,v1] returns [a0(v0),a1(v0),a0(v1),a1(v1)]'''
    def __init__(self, *acts): self.acts = nn.ModuleList(acts)
    def forward(self, x):
        if len(self.acts)==1: return self.acts[0](x)
        return interleaved(*[f(x) for f in self.acts], dim=1)

# Cell
def _listify(x): return x if isinstance(x, list) else [x]
def _init_acts(acts, acts_params):
    '''Init act using act_params. and combine using MultiActs

    _init_acts(nn.ReLU, {'inplace':True})
    _init_acts([nn.ReLU,nn.ReLU], {'inplace':True})       #two relu with inplace
    _init_acts([nn.ReLU,nn.ReLU], [{'inplace':True}, {}]) #two relu, first with inplace
    _init_acts(nn.ReLU,           [{'inplace':True}, {}]) #two relu, first with inplace
    '''
    acts,acts_params = map(_listify, [acts, acts_params])

    if len(acts)==0: return nn.Identity(),1

    n1,n2 = map(len, [acts, acts_params])
    assert n1==n2 or 1 in [n1,n2], f'either equal or can be broadcast {[n1,n2]}'
    acts = [act(**params) for act,params in zip_cycle_longest(acts,acts_params)]

    return MultiActs(*acts),len(acts)

# Cell
class Linear(Module):
    __repr__=basic_repr('in_channels,out_channels,bias,groups')
    def __init__(self, in_channels, out_channels, bias=True, groups=1):
        store_attr()
        if groups == 1: self._m = nn.Linear(in_channels, out_channels, bias)
        else:           self._m = nn.Conv2d(in_channels, out_channels, 1, bias=bias, groups=groups)
    def forward(self, x):
        test_eq(x.ndim, 2)
        def to2d(x): return x.view(*x.shape[:2])
        def to4d(x): return x.view(*x.shape[:2], 1, 1)
        fs = [to4d, self._m, to2d] if self.groups != 1 else [self._m]
        return compose(*fs)(x)

# Cell
def _linear_act_norm(c_in, c_out, *, groups, is_final=False, bias=True, bn=nn.BatchNorm1d, bn_params={}, acts=[nn.LeakyReLU], acts_params={}):
    model = Linear(c_in, c_out, bias, groups)
    if is_final: return model, c_in, c_out
    acts, expansion = _init_acts(acts=acts, acts_params=acts_params)
    bn = bn(c_out * expansion, **bn_params)
    return nn.Sequential(model, acts, bn), c_in, c_out * expansion

# Cell
def _build_channels(*, c_in, c_mid, c_out, n_layers):
    assert n_layers >= 1
    return [c_in] + [c_mid]*(n_layers-1) + [c_out]
def _build_heads(*, channels, heads, groups, in_groups):
    assert groups == in_groups == 1,'if you use head, dont touch groups'
    channels = channels[:1] + [c*heads for c in channels[1:]]
    groups = heads
    return channels,groups

# Cell
@delegates(_linear_act_norm, but='groups')
def MLP(*, c_in=None, c_mid=None, c_out=None, n_layers=None, channels=None, groups=1, in_groups=1, heads=None, bias_last=True, **kwargs):
    test_all_eq(c_in, c_mid, c_out, n_layers, map=isinstance(NoneType))
    assert (c_in is None) != (channels is None),'either channels of in\\mid\\out\\nlayers'
    if in_groups != 1: assert in_groups == groups, 'unexpected usage'
    if c_in is not None: channels = _build_channels(c_in=c_in, c_mid=c_mid, c_out=c_out, n_layers=n_layers)
    if heads is not None: channels,groups = _build_heads(channels=channels, heads=heads, groups=groups, in_groups=in_groups)
    assert len(channels) >= 2

    kw=kwargs
    blocks = OrderedDict(); c_in = channels[0]; kw['groups'] = in_groups
    for i,c_out in enumerate(channels[1:-1]):
        blocks[f'block_{i}'],_,c_in = _linear_act_norm(c_in,c_out,**kw)
        kw['groups'] = groups
    kw['is_final'] = True
    if bias_last is not None: kw['bias'] = bias_last
    blocks['head'],*_ = _linear_act_norm(c_in,channels[-1],**kw)
    return nn.Sequential(blocks)