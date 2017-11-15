import os
from abc import ABC
from operator import itemgetter

from file_utils.py_wrapper import aggregate, compose, separate


class Folder(ABC):
    def __init__(self):
        self.filenames = set()
        self.files = set()
        self.path = None
        self.subfolders = {}

    @classmethod
    def with_subfolders(cls, path):
        folder = cls()
        folder.path = path
        subfolder_names, folder.filenames = separate(set(os.listdir(path)), lambda x: os.path.isdir(os.path.join(path, x)))
        folder.filetypes = aggregate(folder.filenames, set, compose(itemgetter(1), os.path.splitext), compose(itemgetter(0), os.path.splitext))
        folder.subfolders = {name: cls.with_subfolders(os.path.join(path, name)) for name in subfolder_names}
        return folder