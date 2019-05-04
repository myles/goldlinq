# -*- coding: utf-8 -*-
"""Application configuration."""
from os import environ
from pathlib import Path


class Config:
    DEBUG = environ.get("DEBUG", True)
    SEND_FILE_MAX_AGE_DEFAULT = 0

    # Site Config
    PER_PAGE = environ.get("PRE_PAGE", 20)
    SITE_TITLE = environ.get("SITE_TITLE", "Goldinq")
    DATETIME_FORMAT = environ.get("DATETIME_FORMAT", "%-d %B %Y, %-I:%M %p")

    # GitHub Repository URL
    GITHUB_REPO_URL = environ.get(
        "GITHUB_REPO_URL", "https://github.com/myles/myles.photo"
    )

    # Paths
    APP_PATH = Path(__file__).parents[0]
    ROOT_PATH = Path(__file__).parents[1]

    STATIC_PATH = environ.get("STATIC_PATH", APP_PATH / "static")
    TEMPLATE_PATH = environ.get("TEMPLATE_PATH", APP_PATH / "templates")

    GALLERIES_PATH = environ.get(
        "GALLERIES_PATH", ROOT_PATH.joinpath("tests/fixtures")
    )

    # Frozen-Flask Config
    # FREEZER_STATIC_IGNORE = ()
    FREEZER_DESTINATION = environ.get("BUILD_DIR", ROOT_PATH.joinpath("build"))


config = Config()
