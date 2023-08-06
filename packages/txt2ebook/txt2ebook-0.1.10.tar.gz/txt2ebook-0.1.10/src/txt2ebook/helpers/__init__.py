"""
Subpackage for helper function
"""

import logging
import sys
from importlib import import_module

logger = logging.getLogger(__name__)


def to_classname(words, suffix):
    """
    Generate class name from words.
    """
    return words.replace("-", " ").title().replace(" ", "") + suffix


def load_class(package_name, class_name):
    """
    Load class dynamically.
    """
    try:
        package = import_module(package_name)
        klass = getattr(package, class_name)
        logger.info("Loading %s.%s", package_name, class_name)
        return klass
    except AttributeError:
        logger.error("Fail to load %s.%s", package_name, class_name)
        sys.exit()
