# -*- coding: utf-8 -*-
"""Click commands."""
import datetime
import click

import toml

from flask import current_app
from flask.cli import with_appcontext


@click.group()
def cli():
    pass


@click.command()
@with_appcontext
def freeze():
    """Freeze the website before deploy."""
    from flask_frozen import Freezer

    freezer = Freezer(current_app)
    freezer.freeze()


@click.command()
@click.option("--published", "-p", default=datetime.datetime.now().isoformat())
@click.option("--slug", "-s", default="untitled")
@click.option("--name", "-n")
@with_appcontext
def create_gallery(published, slug, name=None):
    """Create a new gallery."""
    gallery_path = current_app.config.GALLERIES_PATH.joinpath(
        f"{published.date}-{slug}"
    )

    if gallery_path.exists():
        return click.echo("Gallery already exists.", err=True)

    # Create the gallery and photos directory.
    gallery_path.mkdir()
    gallery_path.joinpath("photos").mkdir()

    meta_file_path = gallery_path.joinpath("meta.toml")

    meta_defaults = {"dt_published": published}

    if name:
        meta_defaults["name"] = name

    meta_file_contents = click.edit(toml.dumps(meta_defaults))

    with meta_file_path.open("w") as meta_file_obj:
        meta_file_obj.write(meta_file_contents)


cli.add_command(create_gallery)
cli.add_command(freeze)
