from typing import Optional

from argcomplete import FilesCompleter
from jsonargparse import ArgumentParser

from classy.cli import BaseCommand
from classy.scripts.cli.utils import checkpoint_path_from_user_input, autocomplete_model_path


class InferenceCommand(BaseCommand):
    @classmethod
    def add_inference_parameters(cls, parser: ArgumentParser):
        parser.add_argument("model_path", type=checkpoint_path_from_user_input).completer = autocomplete_model_path
        parser.add_argument("file_path").completer = FilesCompleter()
        parser.add_argument("-d", "--device", default="gpu")

    def fill_parser(self, subcommands):
        parser = self.parser()
        self.add_inference_parameters(parser)
        subcommands.add_subcommand(self.name, parser)
