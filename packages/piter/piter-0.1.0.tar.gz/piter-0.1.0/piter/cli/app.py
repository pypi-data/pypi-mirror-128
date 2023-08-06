import shutil
import os
import sys
import subprocess
from typing import List

import typer

import piter.env
from piter.cli.utils import check_path_is_dir
import piter.cli.output as output
from piter.config import config

app = typer.Typer()


@app.command("config")
def print_config():
    typer.echo(f"{config.to_toml()}")
    for warning in config.get_warnings():
        output.warning(warning.line, warning.env, warning.script)


@app.command()
def env(
    name: str,
    install: bool = typer.Option(False, "--install", "-i"),
    remove: bool = typer.Option(False, "--remove", "-r"),
    reinstall: bool = typer.Option(False, "--reinstall", "-ri"),
):
    if remove or reinstall:
        try:
            shutil.rmtree(piter.env.env_path_by_name(name))
        except FileNotFoundError:
            output.info(f"Environment not found", name)
        else:
            output.info(f"Environment removed", name)

    if install or not check_path_is_dir(piter.env.env_path_by_name(name)):
        piter.env.create_env(name)
        output.info(f"Environment created", name)

    if install or reinstall:
        piter.env.install_dependencies(name)
        output.info(f"Dependencies installed", name)
        piter.env.generate_lockfile(name)
        output.info(f"Lockfile generated", name)


# TODO: if environment does not exists, create it and install dependencies
# TODO: error like this (pytest was already installed and has executable): [piter][ci][ERROR] - Script line finished with error: piter_envs/ci/venv/bin/pip install piter_envs/ci/venv/bin/pytest pyyaml
# TODO: error like this (pip was already installed): [piter][ci][ERROR] - Script line finished with error: piter_envs/ci/venv/bin/pip install --upgrade piter_envs/ci/venv/bin/pip
# TODO: run scripts from file like "./install.sh" is not working
@app.command("run")
def execute_script(
    script: str, environment: str = typer.Option("", "--environment", "-e")
):
    exec_status = 0

    if not environment:
        env_candidates: list[str] = []
        for env_name, env in config.env.items():
            if script in env.scripts.keys():
                env_candidates.append(env_name)

        if len(env_candidates) == 1:
            environment = env_candidates[0]
        elif len(env_candidates) == 0:
            output.error(f"No environment has script {output.script(script)}")
            return
        else:
            output.error(
                f"Multiple environments {env_candidates} have script {output.script(script)}. Please specify environment with --environment (-e) option"
            )
            return

    for script_line in config.env[environment].scripts[script]:
        env_execs = piter.env.env_execs(environment)
        command = []
        for command_part in script_line.split(" "):
            if command_part in env_execs:
                command_part = os.path.join(
                    piter.env.env_path_by_name(environment), "bin", command_part
                )
            command.append(command_part)

        try:
            subprocess.check_call(command)
            output.success(
                f"Script line executed successfully: {output.script(script_line)}",
                environment,
                script,
            )
        except subprocess.CalledProcessError:
            output.error(
                f"Script line finished with error: {output.script(script_line)}",
                environment,
                script,
            )
            exec_status = 1

    sys.exit(exec_status)


@app.command("install")
def install(
    dependencies: List[str], environment: str = typer.Option("", "--environment", "-e")
):
    dependencies = list(dependencies)
    piter.env.install_dependencies(environment, dependencies)
    output.info(f"Dependencies installed", environment)
    piter.env.generate_lockfile(environment)
    output.info(f"Lockfile generated", environment)
