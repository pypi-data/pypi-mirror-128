"""
Module for parsing English language txt file.
"""
import logging

logger = logging.getLogger(__name__)


class EnParser:
    """
    Module for parsing txt format in en.
    """

    def __init__(self, content, opts):
        self.raw_content = content
        self.opts = opts

    def parse(self):
        """
        Parse the content into volumes (optional) and chapters.
        """
        logger.info("Parsed 0 volumes.")
        logger.error("Parsed 0 chapters.")
        return (self.raw_content, self.raw_content)
