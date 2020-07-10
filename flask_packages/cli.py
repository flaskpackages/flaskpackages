"""Console script for flask_packages."""
import sys
import click

from flask_packages.web import app


@click.command()
def main(args=None):
    app.run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
