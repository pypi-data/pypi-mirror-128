"""
Module for generating txt file.
"""
import logging
import os
from datetime import datetime
from pathlib import Path


logger = logging.getLogger(__name__)


class TxtWriter:
    """
    Module for writing ebook in txt format.
    """

    def __init__(self, book, opts):
        self.book = book
        self.filename = opts["input_file"]
        self.no_backup = opts["no_backup"]

    def write(self):
        """
        Optionally backup and overwrite the txt file.
        """
        if not self.no_backup:
            self._backup_file()

        self._overwrite_file()

    def _backup_file(self):
        txt_filename = Path(self.filename)

        ymd_hms = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = Path(
            txt_filename.resolve().parent.joinpath(
                txt_filename.stem + "_" + ymd_hms + ".bak.txt"
            )
        )
        os.rename(txt_filename, backup_filename)
        logger.info("Backup txt file: '%s'.", backup_filename)

    def _overwrite_file(self):
        txt_filename = Path(self.filename)

        with open(txt_filename, "w") as file:
            file.write(self.book.massaged_content)
            logger.info("Overwrite txt file: '%s'.", txt_filename.resolve())
