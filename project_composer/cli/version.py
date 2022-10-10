import click

from .. import __pkgname__, __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo("{name} {version}".format(name=__pkgname__, version=__version__))
