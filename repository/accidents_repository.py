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


def get_accidents_by_area_week(area, date):
    try:
        start_date = date - timedelta(days=date.weekday())
        end_date = start_date + timedelta(days=7)
        query = {
            'area': area,
            'date': {
                '$lt': end_date,
                '$gte': start_date
            }
        }
        total_accidents = daily.count_documents(query)
        return Success({"total_accidents": total_accidents})

    except PyMongoError as e:
        return Failure(str(e))


def get_accidents_by_area_month(area, date):
    try:
        start_date = date.replace(day=1)
        next_month = start_date.month % 12 + 1
        end_date = start_date.replace(month=next_month, day=1)
        query = {
            'area': area,
            'date': {
                '$lt': end_date,
                '$gte': start_date
            }
        }
        total_accidents = daily.count_documents(query)
        return Success({"total_accidents": total_accidents})

    except PyMongoError as e:
        return Failure(str(e))


def get_all_accidents_by_area_cause(area):
    try:
        all_accidents = areas.find({'area': area}, {'contributing_factors': 1, '_id': 0})
        return Success(all_accidents[0]["contributing_factors"])
    except PyMongoError as e:
        return Failure(str(e))
