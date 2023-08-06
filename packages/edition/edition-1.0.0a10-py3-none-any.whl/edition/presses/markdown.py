from typing import IO

from dinject.enums import Content, Host
from dinject.types import ParserOptions

from edition.presses.press import Press


class MarkdownPress(Press):
    @property
    def injection_options(self) -> ParserOptions:
        return ParserOptions(force_content=Content.MARKDOWN, force_host=Host.SHELL)

    def _press(self, writer: IO[str]) -> None:
        writer.write(self._markdown_body.strip())
        writer.write("\n")
