from datetime import datetime

from returns.result import Success

from repository.accidents_repository import get_all_accidents_by_area, get_accidents_by_area_day, \
    get_accidents_by_area_week, get_accidents_by_area_month, get_all_accidents_by_area_cause


def test_all_accidents_by_area():
    res = get_all_accidents_by_area('222')
    assert isinstance(res, Success)
    assert len(res.unwrap()) > 0


def test_get_accidents_by_area_day():
    res = get_accidents_by_area_day('1650', datetime(2023, 9, 22))
    assert isinstance(res, Success)
    total_accidents = res.unwrap()["total_accidents"]
    assert total_accidents > 0


def test_get_accidents_by_area_week():
    res = get_accidents_by_area_week('1650', datetime(2023, 9, 22))
    assert isinstance(res, Success)
    total_accidents = res.unwrap()["total_accidents"]
    assert total_accidents > 0


def test_get_accidents_by_area_month():
    res = get_accidents_by_area_month('1650', datetime(2023, 9, 22))
    assert isinstance(res, Success)
    total_accidents = res.unwrap()["total_accidents"]
    assert total_accidents > 0


def test_all_accidents_by_area_cause():
    res = get_all_accidents_by_area_cause('222')
    assert isinstance(res, Success)
    assert len(res.unwrap()) > 0
