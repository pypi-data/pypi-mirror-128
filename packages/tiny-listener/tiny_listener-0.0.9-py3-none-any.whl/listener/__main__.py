import sys

import click

import listener


def show_version(ctx, *_) -> None:
    click.echo(f"tiny-listener {listener.__version__}")
    ctx.exit()


@click.command()
@click.option(
    "--app-dir",
    "app_dir",
    default=".",
    show_default=True,
    help="Your APP directory.",
)
@click.option(
    "--version",
    is_flag=True,
    callback=show_version,
    expose_value=False,
    is_eager=True,
    help="Display version info.",
)
@click.argument('app')
def main(app_dir, app):
    sys.path.insert(0, app_dir)
    try:
        app = listener.import_from_string(app)
    except BaseException as e:
        click.echo(e)
        sys.exit(1)
    else:
        app.run()


if __name__ == "__main__":
    main()
