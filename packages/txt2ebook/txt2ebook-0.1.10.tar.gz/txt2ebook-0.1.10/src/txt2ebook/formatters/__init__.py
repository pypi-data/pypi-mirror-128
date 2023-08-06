"""
Subpackages for writing different ebook format.
"""
from ..helpers import to_classname, load_class
from .epub import EpubWriter
from .txt import TxtWriter


def create_formatter(book, kwargs):
    """
    Factory method to create ebook formatter by format.
    """
    class_name = to_classname(kwargs["format"], "Writer")
    klass = load_class("txt2ebook.formatters", class_name)
    formatter = klass(book, kwargs)
    return formatter
