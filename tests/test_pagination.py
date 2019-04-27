import pytest

from goldlinq.pagination import (
    EmptyPage,
    InvalidPage,
    Page,
    PageNotAnInteger,
    Paginator,
    UnorderedObjectListWarning,
)


@pytest.fixture
def paginator():
    return Paginator(range(0, 999), per_page=10)


@pytest.fixture
def page(paginator):
    return Page(range(0, 10), 1, paginator)


@pytest.fixture
def page_2(paginator):
    return Page(range(10, 20), 2, paginator)


def test_page_has_next(page):
    assert page.has_next == True


def test_page_has_previous(page):
    assert page.has_previous == False


def test_page_has_other_pages(page):
    assert page.has_other_pages == True


def test_page_next_page_number(page):
    assert page.next_page_number == 2


def test_page_previous_page_number(page, page_2):
    with pytest.raises(EmptyPage):
        page.previous_page_number()

    assert page_2.previous_page_number == 1


def test_page_start_index(page):
    assert page.start_index == 1


def test_page_end_index(page):
    assert page.end_index == 10


def test_paginator_validate_number(paginator):
    assert paginator.validate_number(1) == 1


def test_paginator_get_page(paginator, page):
    assert paginator.get_page(1).number == page.number
