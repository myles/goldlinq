from pathlib import PosixPath

import pytest

from goldlinq.models.meta import Model, ResultSet


@pytest.fixture
def result_set():
    results = ResultSet()

    model_a = Model("./A/")
    model_a.name = "A"
    results.append(model_a)

    model_c = Model("./C/")
    model_c.name = "C"
    results.append(model_c)

    model_b = Model("./B/")
    model_b.name = "B"
    results.append(model_b)

    return results


@pytest.fixture
def model():
    _model = Model("./Hi/")
    _model.name = "Hi"
    return _model


def test_result_set_paths(result_set):
    assert result_set.paths == [
        PosixPath("./A/"),
        PosixPath("./C/"),
        PosixPath("./B/"),
    ]


def test_result_set_names(result_set):
    assert result_set.names == ["A", "C", "B"]


def test_result_set_order_by(result_set):
    result_set.order_by("name", direction=None)
    assert result_set.names == ["A", "B", "C"]

    result_set.order_by("name", direction="descending")
    assert result_set.names == ["C", "B", "A"]

    result_set.order_by("name", direction="ascending")
    assert result_set.names == ["A", "B", "C"]


def test_model___str__(model):
    assert model.__str__() == "Hi"
