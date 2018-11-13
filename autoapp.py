# -*- coding: utf-8 -*-
"""Create an application instance."""
from goldlinq.app import create_app
from goldlinq.config import Config

APP = create_app(Config)
