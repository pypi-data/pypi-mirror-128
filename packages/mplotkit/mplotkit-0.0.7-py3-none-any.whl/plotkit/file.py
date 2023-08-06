import inspect
import os
import sys
from typing import Optional


def get_invoker_dir(follow_symlinks=True):
    if getattr(sys, "frozen", False):  # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        try:
            path = sys.modules["__main__"].__file__
        except AttributeError:
            return os.getcwd()
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


def expand_relative(path: str, relative_to: Optional[str] = None):
    if os.path.isabs(path):
        return path
    if not relative_to:
        return os.path.abspath(path)
    return os.path.normpath(os.path.join(relative_to, path))


def split_fname(path: str):
    path, basename = os.path.split(path)
    name, ext = os.path.splitext(basename)
    return path, name, ext
