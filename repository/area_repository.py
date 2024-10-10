from datetime import timedelta

from pymongo.errors import PyMongoError
from returns.result import Success, Failure

from database.connect import areas, daily


def get_all_accidents_by_area(area):
    try:
        all_accidents = areas.find_one({'area': area})
        return Success(all_accidents)
    except PyMongoError as e:
        return Failure(str(e))


def get_accidents_by_area_day(area, date):
    try:
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        query = {'area': area,
                 'date': {
                     '$lt': end_date,
                     '$gte': start_date}
                 }
        total_accidents = daily.count_documents(query)
        return Success({"total_accidents": total_accidents})

    except PyMongoError as e:
        return Failure(str(e))
