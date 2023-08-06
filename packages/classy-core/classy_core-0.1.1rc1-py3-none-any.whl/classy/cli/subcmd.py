from typing import Dict, Optional, Iterable, Type

from jsonargparse import ArgumentParser, namespace_to_dict


class BaseCommand:
    """
    a command of a given Application
    e.g. if name is "init", this command handles app init ...
    """

    name: str

    def run(self, config):
        raise NotImplemented

    def parser(self) -> Optional[ArgumentParser]:
        raise NotImplemented

    def fill_parser(self, subcommands):
        subcommands.add_subcommand(self.name, self.parser())

    def __repr__(self):
        return self.name


class Subcommand(BaseCommand):
    name: str
    description: Optional[str] = None

    def run(self, *args, **kwargs):
        raise NotImplemented

    def parser(self) -> Optional[ArgumentParser]:
        parser = ArgumentParser(description=self.description)
        parser.add_function_arguments(self.run, as_group=False, as_positional=True)
        return parser


class CommandWithSubcommands(BaseCommand):
    def __init__(self, name: str, subcommands: Optional[Dict[str, Subcommand]] = None):
        self.name = name
        self.subcommands: Dict[str, Subcommand] = subcommands or {}

    def add_subcommand(self, subcmd: Subcommand):
        self.subcommands[subcmd.name] = subcmd

    def fill_parser(self, parent_subcommands):
        parser = ArgumentParser()
        parent_subcommands.add_subcommand(self.name, parser)

        subcommands = parser.add_subcommands(dest="action")
        for name, subcmd in self.subcommands.items():
            subcommands.add_subcommand(name, subcmd.parser() or ArgumentParser())

    def run(self, config):
        action = config.action
        action_config = getattr(config, action, None)
        action_config = namespace_to_dict(action_config) if action_config is not None else {}
        self.subcommands[action].run(**action_config)

    @classmethod
    def create(cls, name: str, subcommands: Iterable[Type[Subcommand]]):
        subcmds = {}

        for subcommand in subcommands:
            instance = subcommand()
            subcmds[instance.name] = instance

        return cls(name, subcmds)
