from pymongo.errors import PyMongoError
from returns.result import Success, Failure

from database.connect import areas


def get_all_accidents_by_area(area):
    try:
        all_accidents = areas.find_one({'area': area})
        return Success(all_accidents)
    except PyMongoError as e:
        return Failure(str(e))
