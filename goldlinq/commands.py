# -*- coding: utf-8 -*-
"""Click commands."""
from os import environ

import click

from flask import current_app
from flask.cli import with_appcontext


@click.command()
@with_appcontext
def cli():
    """Freeze the website before deploy."""
    from flask_frozen import Freezer

    freezer = Freezer(current_app)
    freezer.freeze()
