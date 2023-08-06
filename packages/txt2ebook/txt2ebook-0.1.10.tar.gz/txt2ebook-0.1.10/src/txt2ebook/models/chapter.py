from dataclasses import dataclass, field


@dataclass
class Chapter:
    """
    Module for a book model.
    """

    title: str = field(default="")
    raw_content: str = field(default="", repr=False)
    paragraphs: list[str] = field(default_factory=list, repr=False)
