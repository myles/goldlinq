# -*- coding: utf-8 -*-
"""The app module."""
from flask import Flask

from . import commands
from .views import BLUEPRINT


def create_app(config="goldlinq.config.Config"):
    app = Flask(__name__)

    app.config.from_object(config)

    app.cli.add_command(commands.freeze)

    app.register_blueprint(BLUEPRINT)

    return app
