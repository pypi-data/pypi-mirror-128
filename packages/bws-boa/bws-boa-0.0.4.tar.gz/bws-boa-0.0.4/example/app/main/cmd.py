
from app import cmd, app
import click


@cmd.command("main__create")
@click.argument('arg')
def main__create(arg):
    app.logger.info(arg)

