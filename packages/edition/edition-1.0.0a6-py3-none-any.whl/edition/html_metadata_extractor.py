from dataclasses import dataclass
from html.parser import HTMLParser
from typing import List, Optional, Tuple

from edition.html import to_anchor_id
from edition.metadata import Metadata

TAttribute = Tuple[str, Optional[str]]


@dataclass
class TocItem:
    name: str
    children: List["TocItem"]


class HtmlMetadataExtractor(HTMLParser):
    def __init__(self, html: str, metadata: Metadata) -> None:
        super().__init__()
        self._html = html
        self._metadata = metadata
        self._path: List[str] = []
        self._toc: List[TocItem] = []

    def _toc_to_html(self, ti: List[TocItem]) -> str:
        if not ti:
            return ""
        wip = "<ol>"
        for t in ti:
            wip += f'<li><a href="#{to_anchor_id(t.name)}">{t.name}</a>'
            wip += self._toc_to_html(t.children)
            wip += "</li>"

        wip += "</ol>"
        return wip

    def append_metadata(self) -> None:
        self.feed(self._html)
        self.close()
        self._metadata["toc"] = f'<nav class="toc">{self._toc_to_html(self._toc)}</nav>'

    def handle_data(self, data: str) -> None:
        if self._path and self._path[-1].lower() == "h1":
            self._metadata["title"] = self._metadata.get("title", data.strip())
        if self._path and self._path[-1].lower() == "h2":
            self._toc.append(TocItem(name=data.strip(), children=[]))
        if self._path and self._path[-1].lower() == "h3":
            self._toc[-1].children.append(TocItem(name=data.strip(), children=[]))

    def handle_endtag(self, tag: str) -> None:
        popped = self._path.pop()
        if popped != tag:
            raise ValueError(f'expected to end "{popped}" but got "{tag}"')

    def handle_starttag(self, tag: str, attrs: Optional[List[TAttribute]]) -> None:
        self._path.append(tag)
