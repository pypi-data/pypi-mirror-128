from typing import List

import toml


def shrink_dependencies(dependencies: List[str]) -> List[str]:
    return list(map(lambda a: a.replace(" ", ""), dependencies))


def load_config():
    return toml.load("pyproject.toml")["tools"]["piter"]
