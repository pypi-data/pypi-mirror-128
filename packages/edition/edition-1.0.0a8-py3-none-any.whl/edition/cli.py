from argparse import ArgumentParser
from enum import IntEnum, auto, unique
from pathlib import Path
from typing import IO, List

from edition import __version__
from edition.presses import keys, make_from_file


@unique
class CliTask(IntEnum):
    HELP = auto()
    MAKE = auto()
    VERSION = auto()


class Cli:
    def __init__(self, args: List[str]) -> None:
        self._parser = ArgumentParser(
            description="Lightweight documentation generator",
            epilog="Made with love by Cariad Eccleston: https://github.com/cariad/edition",
        )

        self._parser.add_argument("source", help="source document", nargs="?")
        self._parser.add_argument(
            "output",
            help="output document (will emit to stdout if omitted)",
            nargs="?",
        )

        self._parser.add_argument(
            "--press",
            help="output format",
            metavar=f"{{{','.join(keys())}}}",
        )

        self._parser.add_argument(
            "--version",
            help="show version and exit",
            action="store_true",
        )

        self._task = CliTask.HELP
        parsed = self._parser.parse_args(args)

        if parsed.version:
            self._task = CliTask.VERSION
        elif parsed.source and parsed.press:
            self._task = CliTask.MAKE

        self._output = parsed.output
        self._press = (
            make_from_file(key=parsed.press, path=Path(parsed.source))
            if parsed.press and parsed.source
            else None
        )

    def invoke(self, writer: IO[str]) -> int:
        """
        Invokes the prescribed task.

        Returns the shell exit code.
        """

        if self._task == CliTask.VERSION:
            writer.write(__version__)
            writer.write("\n")
            return 0

        if self._press:
            render = open(self._output, "w") if self._output else writer
            self._press.press(writer=render)
            if self._output:
                render.close()
                print(f"Pressed: {self._output}")
            return 0

        writer.write(self._parser.format_help())
        return 1

    @property
    def task(self) -> CliTask:
        """Gets the task that this CLI invocation will perform."""

        return self._task
