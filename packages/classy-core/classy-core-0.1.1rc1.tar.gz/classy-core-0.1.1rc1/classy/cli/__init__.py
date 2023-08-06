from typing import Dict, Union, Type

from jsonargparse import ArgumentParser

from classy.cli.serve import ServeCommand
from classy.cli.subcmd import BaseCommand


class ClassyApplication:
    commands: Dict[str, BaseCommand] = {}

    def get_parser(self) -> ArgumentParser:
        parser = ArgumentParser()

        subcommands = parser.add_subcommands(dest="cmd")
        for command in self.commands.values():
            command.fill_parser(subcommands)

        return parser

    def run(self):
        args = self.get_parser().parse_args()
        command = args.cmd
        command_config = getattr(args, command)
        self.commands[command].run(command_config)

    @classmethod
    def create(cls, *commands: Union[Type[BaseCommand], BaseCommand]) -> "ClassyApplication":
        instance = cls()

        for command in commands:
            if not isinstance(command, BaseCommand):
                command = command()

            instance.commands[command.name] = command

        return instance


def run():
    ClassyApplication.create(ServeCommand).run()


if __name__ == "__main__":
    run()
