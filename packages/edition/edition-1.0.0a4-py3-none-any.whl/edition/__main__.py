from sys import argv, stdout

from edition.cli import Cli


def cli_entry() -> None:
    exit(Cli(argv[1:]).invoke(stdout))


if __name__ == "__main__":
    cli_entry()
