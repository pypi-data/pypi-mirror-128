from pathlib import Path
from typing import Dict, List, Tuple, Type, cast

import frontmatter  # pyright: reportMissingTypeStubs=false

from edition.exceptions import NoPressError
from edition.metadata import Metadata
from edition.presses.html import HtmlPress
from edition.presses.markdown import MarkdownPress
from edition.presses.press import Press

registered: Dict[str, Type[Press]] = {}


def keys() -> List[str]:
    return [k for k in registered]


def make(key: str, markdown_content: str) -> "Press":
    press = registered.get(key, None)
    if not press:
        raise NoPressError(key)

    metadata, markdown_body = cast(
        Tuple[Metadata, str],
        frontmatter.parse(markdown_content),
    )  # pyright: reportUnknownMemberType=false

    return press(markdown_body=markdown_body, metadata=metadata)


def make_from_file(key: str, path: Path) -> "Press":
    with open(path, "r") as f:
        return make(key=key, markdown_content=f.read())


def register(key: str, press: Type[Press]) -> None:
    registered[key] = press


register("html", HtmlPress)
register("markdown", MarkdownPress)

__all__ = [
    "HtmlPress",
    "MarkdownPress",
    "Press",
]
