"""Docker Dev Environment, easily develop your programs using containers"""

__version__ = "0.0.1"

import docker
import typer


def info():
    client = docker.from_env()
    typer.echo(client.version())


def main():
    typer.run(info)
