from io import StringIO
from typing import IO

from dinject.enums import Content, Host
from dinject.types import ParserOptions
from markdown import markdown
from mdcode import get_blocks
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer

from edition.html import get_html_template
from edition.html_metadata_extractor import HtmlMetadataExtractor
from edition.html_renderer import EditionHtmlRenderer
from edition.pre_html_renderer import PreHtmlRenderer
from edition.presses.press import Press


class HtmlPress(Press):
    @property
    def injection_options(self) -> ParserOptions:
        return ParserOptions(force_content=Content.HTML, force_host=Host.TERMINAL)

    def _replace_blocks_with_pygments(self, body: str) -> str:
        writer = StringIO()
        lines = body.splitlines()

        index = 0
        blocks = get_blocks(body)
        for block in blocks:
            # Copy over the lines until this block:
            if not block.source_index:
                raise Exception()
            while index < block.source_index:
                writer.write(lines[index])
                writer.write("\n")
                index += 1

            script = "\n".join(block.lines)
            lexer = get_lexer_by_name(block.lang) if block.lang else guess_lexer(script)

            formatter = HtmlFormatter()
            highlight(script, lexer, formatter, writer)
            index = block.source_index + block.source_length

        # Copy all remaining lines:
        while index < len(lines):
            writer.write(lines[index])
            writer.write("\n")
            index += 1

        return writer.getvalue().rstrip()

    def _post_injection(self) -> None:
        self._markdown_body = self._replace_blocks_with_pygments(self._markdown_body)

    def _press(self, writer: IO[str]) -> None:
        html_body = markdown(
            self._markdown_body,
            extensions=["markdown.extensions.tables"],
            output_format="html",
        )
        HtmlMetadataExtractor(html_body, self._metadata).append_metadata()

        processed_html = StringIO()

        # This initial run adds anchors to headers. This could probably be added
        # to EditionHtmlRenderer, but remember to feed in just the body here:
        PreHtmlRenderer().render(html_body, processed_html)

        processed_html.seek(0)

        html_body_writer = StringIO()

        edition_renderer = EditionHtmlRenderer(metadata=self._metadata)
        edition_renderer.render(reader=processed_html, writer=html_body_writer)

        self._metadata["body"] = html_body_writer.getvalue()

        with get_html_template() as f:
            edition_renderer.render(reader=f, writer=writer)
