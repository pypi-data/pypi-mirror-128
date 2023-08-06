import sys

import click

from pyevent import import_from_string


@click.command(help="run pyevent")
@click.argument('app')
def run(app):
    import os
    print(os.path.abspath(__file__))

    try:
        app = import_from_string(app)
    except BaseException as e:
        click.echo(e)
        sys.exit(1)
    else:
        app.run()


if __name__ == "__main__":
    run()
