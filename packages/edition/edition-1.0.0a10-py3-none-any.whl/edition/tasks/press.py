from pathlib import Path

from cline import CommandLineArguments, Task

from edition.presses import keys, make
from edition.tasks.arguments import PressArguments


class PressTask(Task[PressArguments]):
    @classmethod
    def make_args(cls, args: CommandLineArguments) -> PressArguments:
        args.assert_string("press", keys())
        return PressArguments(
            key=args.get_string("press"),
            source=Path(args.get_string("source")),
            output=Path(args.get_string("output")),
        )

    def invoke(self) -> int:
        with open(self.args.source, "r") as f:
            press = make(key=self.args.key, markdown_content=f.read())
        with open(self.args.output, "w") as f:
            press.press(writer=f)
        self.out.write("Pressed: ")
        self.out.write(self.args.output.as_posix())
        self.out.write("\n")
        return 0
