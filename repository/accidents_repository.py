from datetime import timedelta

from returns.result import Success, Failure

from database.connect import areas, daily


def get_all_accidents_by_area(area):
    try:
        all_accidents = areas.find_one({'area': area})
        return Success({"total_accidents": all_accidents['total_accidents']})
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


from pymongo.errors import PyMongoError


def get_area_stats(area_name):
    try:
        area_data = areas.find_one({'area': area_name})
        if not area_data:
            return Failure({'error': 'Area not found'}), 404

        total_accidents = area_data.get('total_accidents', 0)
        total_injuries = area_data.get('injuries', {}).get('total', 0)
        fatal_injuries = area_data.get('injuries', {}).get('fatal', 0)
        non_fatal_injuries = area_data.get('injuries', {}).get('non_fatal', 0)

        events = daily.find({'area': area_name}, {'_id': 0, 'date': 1, 'injuries': 1, 'contributing_factors': 1})
        fatal_events = []
        non_fatal_events = []
        for event in events:
            if event['injuries']['fatal'] > 0:
                fatal_events.append(event)
            elif event['injuries']['non_fatal'] > 0:
                non_fatal_events.append(event)

        result = {
            'area': area_name,
            'total_accidents': total_accidents,
            'total_injuries': total_injuries,
            'fatal_injuries': fatal_injuries,
            'non_fatal_injuries': non_fatal_injuries,
            'fatal_events': fatal_events,
            'non_fatal_events': non_fatal_events
        }
        return Success(result)
    except PyMongoError as e:
        return Failure(str(e))
