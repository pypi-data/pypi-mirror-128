from dataclasses import dataclass, field

from .chapter import Chapter


@dataclass
class Volume:
    """
    Module for a volume of a book model.
    """

    title: str = field(default="")
    chapters: list[Chapter] = field(default_factory=list, repr=False)
    raw_content: str = field(default="", repr=False)
