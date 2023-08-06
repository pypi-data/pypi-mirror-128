from dataclasses import dataclass, field

from .volume import Volume
from .chapter import Chapter


@dataclass
class Book:
    """
    Module for a book model.
    """

    title: str = field(default="")
    authors: list[str] = field(default_factory=list)
    language: str = field(default="")
    cover: str = field(default="", repr=False)
    raw_content: str = field(default="", repr=False)
    massaged_content: str = field(default="", repr=False)
    parsed_content: list[tuple] = field(default_factory=list, repr=False)
    volumes: list[Volume] = field(default_factory=list, repr=False)
    chapters: list[Chapter] = field(default_factory=list, repr=False)
