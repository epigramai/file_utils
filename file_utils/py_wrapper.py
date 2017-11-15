import importlib
import os
import sys
import time

from functools import wraps
from itertools import groupby
from operator import itemgetter
from types import MethodType


def identity(x):
    return x


def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg
    return inner


def get_or(dct, k):
    return dct.get(k, k)


def left_outer_compose(dct2, dct1):
    if not dct2:
        return dct1
    return {k: get_or(dct2, v) for k, v in dct1.items()}


def full_outer_compose(dct2, dct1):
    if not dct1 or not dct2:
        return dct2 or dct1 # the order matters: None or {} -> {}; {} or None -> None
    return {k: get_or(dct2, get_or(dct1, k)) for k in dct1.keys() | dct2.keys()}


def aggregate(st, aggregator=set, key_wrapper=identity, value_wrapper=identity):
    return {k: aggregator(value_wrapper(v) for v in grp) for k, grp in groupby(sorted(st, key=key_wrapper), key=key_wrapper)}


def aggregate_keys(dct, aggregator=set, key_wrapper=identity, value_wrapper=identity):
    return aggregate(dct.items(), aggregator, compose(value_wrapper, itemgetter(1)), compose(key_wrapper, itemgetter(0)))


def aggregate_values(dct, aggregator=set, key_wrapper=identity, value_wrapper=identity):
    return aggregate(dct.items(), aggregator, compose(key_wrapper, itemgetter(0)), compose(value_wrapper, itemgetter(1)))


#TODO: convert dict_keys objects to set in a principled manner
def separate(iterable_object, test):
    wheat = []
    chaff = []
    for x in iterable_object:
        if test(x):
            wheat.append(x)
        else:
            chaff.append(x)
    return iterable_object.__class__(wheat), iterable_object.__class__(chaff)


def lstrip(strng, prefix):
    return strng[len(prefix):] if prefix and strng.startswith(prefix) else strng


def rstrip(strng, suffix):
    return strng[:-len(suffix)] if suffix and strng.endswith(suffix) else strng


def get_class_from_module_path(path):

    folder_path, filename = os.path.split(path)
    module_name = os.path.splitext(filename)[0]
    class_name = module_name.capitalize()

    # more targeted way of loading module that avoids adding folder_path to the system path,
    # but then how does one import sibling modules in module_at_path?
    # spec = importlib.util.spec_from_file_location(module_name, path)
    # module_at_path = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module_at_path)

    sys.path.append(folder_path)
    module_at_path = importlib.import_module(module_name)
    class_at_path = getattr(module_at_path, class_name)

    return class_at_path


def is_instance_method(cls, attribute):
    return hasattr(attribute, '__self__') and isinstance(getattr(attribute, '__self__'), cls)


def decorate_all_instance_methods(method_decorator):
    def class_decorator(cls):
        orig_init = cls.__init__
        def __init__(self, *args, **kwargs):
            self._method_times = []
            orig_init(self, *args, **kwargs)
        cls.__init__ = __init__
        
        orig_getattribute = cls.__getattribute__
        def __getattribute__(self, s):
            x = orig_getattribute(self, s)
            if is_instance_method(cls, x):
                x = MethodType(method_decorator(x.__func__), x.__self__)
            return x
        cls.__getattribute__ = __getattribute__
        
        return cls
    return class_decorator


def store_time(m):
    @wraps(m)
    def m_timed(self, *args, **kwargs):
        if not hasattr(self, '_method_times'):
            self._method_times = []
        start_time = time.time()
        r = m(self, *args, **kwargs)
        self._method_times.append((m.__name__, time.time() - start_time))
        return r
    return m_timed