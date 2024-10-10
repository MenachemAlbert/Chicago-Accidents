from returns.result import Success

from repository.area_repository import get_all_accidents_by_area


def test_all_accidents_by_area():
    res = get_all_accidents_by_area('222')
    assert isinstance(res, Success)
    assert len(res.unwrap()) > 0


