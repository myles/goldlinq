from pathlib import Path

import pytest

from goldlinq.models import microformats2
from goldlinq.models.core import Gallery, Photo

FIXTURE_PATH = Path(__file__).parents[1].joinpath("fixtures")

PHOTO_PATH = FIXTURE_PATH.joinpath(
    "2000-01-01-new-years-day/photos/IMG-001.toml"
)
PHOTO_LIST_PATH = FIXTURE_PATH.joinpath("2000-01-01-new-years-day/photos")

GALLERY_PATH = FIXTURE_PATH.joinpath("2000-01-01-new-years-day")
GALLERY_LIST_PATH = FIXTURE_PATH


@pytest.fixture
def photo():
    return Photo.parse(PHOTO_PATH)


@pytest.fixture
def photo_list():
    return Photo.parse_directory(PHOTO_LIST_PATH)


@pytest.fixture
def gallery():
    return Gallery.parse(GALLERY_PATH)


@pytest.fixture
def gallery_list():
    return Gallery.parse_directory(GALLERY_PATH)


def test_photo_initialisation(photo):
    assert photo.path == PHOTO_PATH


def test_photo_list_initialisation(photo_list):
    assert len(photo_list) == 3


def test_photo_name(photo):
    assert "Photo One" == photo.name


def test_photo_gallery(photo):
    assert isinstance(photo.gallery, Gallery)


def test_photo_location(photo):
    assert isinstance(photo.location, microformats2.HGeo)


def test_photo_to_h_object(photo):
    assert photo.to_h_object()["properties"]["name"] == ["Photo One"]


def test_photo_list_path(photo_list):
    assert sorted(photo_list.paths) == sorted(PHOTO_LIST_PATH.glob("*.toml"))


def test_photo_list_order_by(photo_list):
    photo_list.order_by()

    assert photo_list.names == ["Photo Three", "Photo Two", "Photo One"]


def test_gallery_initialisation(gallery):
    assert gallery.path == GALLERY_PATH


def test_gallery_name(gallery):
    assert gallery.name == "A New Millennium"


def test_gallery_list_initialisation(gallery_list):
    assert len(gallery_list) == 1


def test_gallery_photos(gallery):
    assert len(gallery.list_photo()) == 3
