from typing import Optional

from jsonargparse import ArgumentParser

from classy.cli import BaseCommand
from classy.cli.inference import InferenceCommand


class ServeCommand(BaseCommand, InferenceCommand):
    name = "serve"

    def parser(self) -> Optional[ArgumentParser]:
        return ArgumentParser(self.name, self.description)

    def run(self, config):
        pass
