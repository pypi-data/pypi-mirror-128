"""
Module for generating epub file.
"""
import logging
import uuid
from pathlib import Path

from ebooklib import epub

SPACE = "\u0020"

logger = logging.getLogger(__name__)


class EpubWriter:
    """
    Module for writing ebook in epub format.
    """

    def __init__(self, book, opts):
        self.book = book
        self.content = book.parsed_content
        self.input_file = opts["input_file"]
        self.output_file = opts["output_file"]

    def write(self):
        """
        Optionally backup and overwrite the txt file.
        """
        book = epub.EpubBook()

        if self.book.title:
            book.set_title(self.book.title)
            book.set_identifier(self._gen_id(self.book))

        if self.book.language:
            book.set_language(self.book.language)

        if self.book.authors:
            book.add_author(", ".join(self.book.authors))

        if self.book.cover:
            with open(self.book.cover, "rb") as image:
                book.set_cover("cover.jpg", image.read())
                book.spine += ["cover"]

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        book.spine += ["nav"]
        if self.book.volumes:
            logger.debug("Generating %d epub volumes", len(self.book.volumes))

            for volume in self.book.volumes:
                logger.debug(volume.title)

                html_chapters = []
                for chapter in volume.chapters:
                    html_chapter = EpubWriter._build_chapter(chapter, volume)
                    book.add_item(html_chapter)
                    book.spine += [html_chapter]
                    html_chapters.append(html_chapter)

                book.toc += [(epub.Section(volume.title), html_chapters)]
        else:
            logger.debug(
                "Generating %d epub chapters", len(self.book.chapters)
            )

            for chapter in self.book.chapters:
                html_chapter = EpubWriter._build_chapter(chapter)
                book.add_item(html_chapter)
                book.spine += [html_chapter]
                book.toc += [html_chapter]

        output_filename = self._gen_output_filename()
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        epub.write_epub(output_filename, book, {})
        logger.info("Generating epub file: '%s'.", output_filename)

    def _gen_id(self, book):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, book.title))

    def _gen_output_filename(self):
        """
        Determine the output epub filename.
        """
        return Path(
            self.output_file
            or Path(self.book.title or self.input_file).stem + ".epub"
        )

    @staticmethod
    def _build_chapter(chapter, volume=None):
        """
        Generates the whole chapter to HTML.
        """
        if volume:
            filename = f"{volume.title}_{chapter.title}"
            logger.debug("%s%s", SPACE * 2, chapter.title)
        else:
            filename = chapter.title
            logger.debug(chapter.title)

        filename = filename.replace(SPACE, "_")

        html = f"<h2>{chapter.title}</h2>"
        for paragraph in chapter.paragraphs:
            paragraph = paragraph.replace(SPACE, "").replace("\n", "")
            html = html + f"<p>{paragraph}</p>"

        return epub.EpubHtml(
            title=chapter.title,
            content=html,
            file_name=filename + ".xhtml",
        )
