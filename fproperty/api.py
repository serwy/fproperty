import builtins

__all__ = ['fproperty', 'property']


_property = builtins.property


def fproperty(func):
    """Decorator for a function that returns (fget, fset, fdel, doc)"""
    return _property(*func())


fproperty.apply = fproperty


class property(_property):
    def apply(func):
        return fproperty(func)
