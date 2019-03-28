from pathlib import Path

import pytest

from goldlinq.models.microformats2 import HGeo, HAdr, HCard, HEvent, HObject


@pytest.fixture
def hobject():
    return HObject.parse({"test": 123})


@pytest.fixture
def hgeo():
    return HGeo.parse({"latitude": 43.6426, "longitude": -79.3871})


def test_to_h_object(hobject):
    assert hobject.to_h_object()["properties"] == {"test": [123]}


def test_hgeo_repr(hgeo):
    assert hgeo.__repr__() == "HGeo(43.6426, -79.3871)"
