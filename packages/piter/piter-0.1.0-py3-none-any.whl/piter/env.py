import venv
import os
import subprocess
import platform
from typing import List

from piter.config import config


def env_path_by_name(name: str):
    return os.path.join(config.env_root, name, "venv")


def env_lockfile_by_name(name: str):
    return os.path.join(config.env_root, name, "dependencies.lock")


def env_execs_path(name: str):
    return os.path.join(
        env_path_by_name(name), "Scripts" if platform.system() == "Windows" else "bin"
    )


def env_execs(name: str) -> List[str]:
    return [
        file
        for file in os.listdir(env_execs_path(name))
        if os.path.isfile(os.path.join(env_execs_path(name), file))
    ]


def generate_lockfile(name: str):
    dependencies: bytes = subprocess.check_output(
        [os.path.join(env_execs_path(name), "python"), "-m", "pip", "freeze"]
    )
    lock_file = open(env_lockfile_by_name(name), "w")
    lock_file.write(dependencies.decode("utf-8"))
    lock_file.close()


def install_dependencies(name: str, dependencies: List[str] = None):
    if not dependencies:
        dependencies: list[str] = []

        try:
            lockfile = open(env_lockfile_by_name(name))
            dependencies = lockfile.readlines()
        except FileNotFoundError:
            dependencies = config.env[name].dependencies

    if dependencies and len(dependencies) > 0:
        subprocess.check_call(
            [os.path.join(env_execs_path(name), "python"), "-m", "pip", "install",]
            + dependencies
        )


def create_env(name: str):
    # TODO: all params must be configurable
    new_venv = venv.EnvBuilder(
        system_site_packages=config.env[name].system_site_packages,
        clear=config.env[name].clear,
        symlinks=config.env[name].symlinks,
        upgrade=config.env[name].upgrade,
        with_pip=config.env[name].with_pip,
        prompt=config.env[name].prompt,
        # TODO: weird error here https://github.com/mishankov/crazy-imports/runs/4278770282?check_suite_focus=true#step:5:156
        # upgrade_deps=config.env[name].upgrade_deps,
    )
    new_venv.create(env_path_by_name(name))
