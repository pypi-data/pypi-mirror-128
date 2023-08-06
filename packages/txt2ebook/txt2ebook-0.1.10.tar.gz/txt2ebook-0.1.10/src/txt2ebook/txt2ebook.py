# pylint: disable=no-value-for-parameter
"""
Main module for txt2ebook console app.
"""

import logging
from pathlib import Path

import click
from bs4 import UnicodeDammit

from txt2ebook import __version__
from txt2ebook.parsers import create_parser
from txt2ebook.formatters import create_formatter


logger = logging.getLogger(__name__)


@click.command(no_args_is_help=True)
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path(), required=False)
@click.option(
    "--format",
    "-f",
    default="epub",
    show_default=True,
    help="Set the export format ebook.",
)
@click.option(
    "--title",
    "-t",
    default=None,
    show_default=True,
    help="Set the title of the ebook.",
)
@click.option(
    "--language",
    "-l",
    default=None,
    help="Set the language of the ebook.",
)
@click.option(
    "--author",
    "-a",
    default=None,
    multiple=True,
    help="Set the author of the ebook.",
)
@click.option(
    "--cover",
    "-c",
    type=click.Path(exists=True),
    default=None,
    help="Set the cover of the ebook.",
)
@click.option(
    "--debug",
    "-d",
    is_flag=True,
    flag_value=logging.DEBUG,
    show_default=True,
    help="Enable debugging log.",
)
@click.option(
    "--no-backup",
    "-nb",
    is_flag=True,
    flag_value=True,
    show_default=True,
    help="Do not backup source txt file.",
)
@click.option(
    "--no-wrapping",
    "-nw",
    is_flag=True,
    show_default=True,
    help="Remove word wrapping.",
)
@click.option(
    "--width",
    "-w",
    type=click.INT,
    show_default=True,
    help="Set the width for line wrapping.",
)
@click.option(
    "--delete-regex",
    "-dr",
    multiple=True,
    help="Regex to delete word or phrase.",
)
@click.option(
    "--replace-regex",
    "-rr",
    nargs=2,
    multiple=True,
    help="Regex to replace word or phrase.",
)
@click.option(
    "--delete-line-regex",
    "-dlr",
    multiple=True,
    help="Regex to delete whole line.",
)
@click.version_option(prog_name="txt2ebook", version=__version__)
def main(**kwargs):
    """
    Console tool to convert txt file to different ebook format.
    """
    logging.basicConfig(
        level=kwargs["debug"] or logging.INFO,
        format="[%(levelname).1s] %(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        filename = Path(kwargs["input_file"])
        logger.info("Processing txt file: '%s'.", filename.resolve())

        with open(filename, "rb") as file:
            unicode = UnicodeDammit(file.read())
            logger.info("Encoding detected: '%s'.", unicode.original_encoding)
            content = unicode.unicode_markup

            if not content:
                raise RuntimeError(f"Empty file content in '{filename}'!")

            parser = create_parser(content, kwargs)
            book = parser.parse()
            logger.debug(repr(book))

            if book.parsed_content:
                writer = create_formatter(book, kwargs)
                writer.write()

            # We write to txt for debugging purpose if output format is not
            # txt.
            if kwargs["format"] != "txt":
                kwargs["format"] = "txt"
                txt_writer = create_formatter(book, kwargs)
                txt_writer.write()

    except RuntimeError as error:
        click.echo(f"[E] {str(error)}!", err=True)


if __name__ == "__main__":
    main()
