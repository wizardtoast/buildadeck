from types import SimpleNamespace

def simple_repr(instance, **kwargs):
    '''helper function to simplify class repr
    ...'''
    return repr(SimpleNamespace(**kwargs)).replace('namespace', instance.__class__.__name__, 1)
