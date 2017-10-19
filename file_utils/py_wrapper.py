import importlib
import os
import sys

from itertools import groupby
from operator import itemgetter


def identity(x):
    return x


def compose(*functions):
    def inner(arg):
        for f in reversed(functions):
            arg = f(arg)
        return arg
    return inner


def get_or(dict1, key):
    return dict1.get(key, key)


def left_outer_compose(dict2, dict1):
    if not dict2:
        return dict1
    return {k: get_or(dict2, v) for k, v in dict1.items()}


def full_outer_compose(dict2, dict1):
    if not dict1 or not dict2:
        return dict2 or dict1 # the order matters: None or {} -> {}; {} or None -> None
    return {k: get_or(dict2, get_or(dict1, k)) for k in dict1.keys() | dict2.keys()}


def aggregate_keys(dictionary, aggregator=set, key_wrapper=identity, value_wrapper=identity):
    return {value: aggregator(key_wrapper(key) for key, _ in group) for value, group in groupby(sorted(dictionary.items()), key=compose(value_wrapper, itemgetter(1)))}


def aggregate_values(dictionary, aggregator=set, key_wrapper=identity, value_wrapper=identity):
    return {key: aggregator(value_wrapper(value) for _, value in group) for key, group in groupby(sorted(dictionary.items()), key=compose(key_wrapper, itemgetter(0)))}


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