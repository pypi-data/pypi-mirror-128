from typing import List, Optional

import yaml
from clicasso import Slug

from apparatus.core import Command, read_repo_config
from apparatus.config import Config


class Get(Command):
    env: Optional[str] = None
    key: Optional[str] = None

    @classmethod
    def slug(cls) -> Slug:
        return ("config", "get")

    def run(self, config: Config, remainder: List[str]) -> None:
        # pylint: disable-unused-argument
        repo_config = read_repo_config(config, self.env)
        if self.key is not None:
            print(yaml.dump(repo_config[self.key]))
        else:
            print(yaml.dump(repo_config))
