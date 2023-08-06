"""
Subpackage for all Parsers.
"""

import logging

from langdetect import detect

from ..helpers import to_classname, load_class
from .zhcn import ZhCnParser
from .zhtw import ZhTwParser
from .en import EnParser

logger = logging.getLogger(__name__)


def create_parser(content, kwargs):
    """
    Factory function to create parser by language.
    """
    kwargs["language"] = detect_language(content, kwargs["language"])
    class_name = to_classname(kwargs["language"], "Parser")
    klass = load_class("txt2ebook.parsers", class_name)
    parser = klass(content, kwargs)
    return parser


def detect_language(content, default):
    """
    Detect the language (ISO 639-1) of the content of the txt file.
    """
    language = default or detect(content)
    logger.info("Language detected: '%s'.", language)
    return language
