# -*- coding: utf-8 -*-
"""Application configuration."""
from pathlib import Path


class Config:
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

    PER_PAGE = 20

    # GitHub Repository URL
    GITHUB_REPO = "https://github.com/myles/myles.photo"

    # Paths
    APP_PATH = Path(__file__).parents[0]
    ROOT_PATH = Path(__file__).parents[1]

    STATIC_PATH = ROOT_PATH.joinpath("static")

    GALLERIES_PATH = ROOT_PATH.joinpath("data")

    # Frozen-Flask Config
    # FREEZER_STATIC_IGNORE = ()
    FREEZER_DESTINATION = ROOT_PATH.joinpath("build")
