from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List, Optional, Tuple

from edition.html import to_anchor_id
from edition.metadata import Metadata

TAttribute = Tuple[str, Optional[str]]


@dataclass
class TocItem:
    children: List["TocItem"]
    data: str
    """
    Full HTML fragment of the item's title.
    """

    name: str
    """
    Anchorable name.
    """


class HtmlMetadataExtractor(HTMLParser):
    def __init__(self, html: str, metadata: Metadata) -> None:
        super().__init__()
        self._anchor = ""
        """
        Text to consider for the current TOC anchor.

        In other words, the TOC entry without child tags.
        """

        self._data = ""
        """
        Text to consider for the current TOC title content.

        In other words, the TOC entry including child tags.
        """

        self._html = html
        self._metadata = metadata
        self._path: List[str] = []
        self._toc: List[TocItem] = []

    def _toc_to_html(self, ti: List[TocItem]) -> str:
        if not ti:
            return ""
        wip = "<ol>"
        for t in ti:
            wip += f'<li><a href="#{to_anchor_id(t.name)}">{t.data}</a>'
            wip += self._toc_to_html(t.children)
            wip += "</li>"

        wip += "</ol>"
        return wip

    def append_metadata(self) -> None:
        self.feed(self._html)
        self.close()
        self._metadata["toc"] = f'<nav class="toc">{self._toc_to_html(self._toc)}</nav>'

    def handle_data(self, data: str) -> None:
        self._anchor += data
        self._data += data

    def handle_endtag(self, tag: str) -> None:
        popped = self._path.pop()
        if popped != tag:
            raise ValueError(f'expected to end "{popped}" but got "{tag}"')

        if tag == "h1":
            self._metadata["title"] = self._metadata.get("title", self._data.strip())

        if tag == "h2":
            self._toc.append(TocItem(name=self._anchor, data=self._data, children=[]))

        if tag == "h3":
            self._toc[-1].children.append(
                TocItem(
                    name=self._anchor,
                    data=self._data,
                    children=[],
                )
            )

        if "h2" in self._path or "h3" in self._path:
            self._data += f"</{tag}>"

    def handle_starttag(self, tag: str, attrs: Optional[List[TAttribute]]) -> None:
        self._path.append(tag)

        if tag in ["h2", "h3"]:
            self._anchor = ""
            self._data = ""
        elif "h2" in self._path or "h3" in self._path:
            self._data += f"<{tag}>"
