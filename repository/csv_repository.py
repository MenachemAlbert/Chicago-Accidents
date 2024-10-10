import csv
import os

from utils.data_utils import parse_date, get_week_range, safe_int
from database.connect import daily, weakly, monthly, areas


def read_csv(path: str):
    with open(path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def init_accidents():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv')
    for row in read_csv(data_path):

        crash_date = parse_date(row['CRASH_DATE'])
        area = row['BEAT_OF_OCCURRENCE']

        daily_doc = {
            'date': crash_date,
            'area': area,
            '$inc': {
                'total_accidents': 1,
                'injuries.total': safe_int(row['INJURIES_TOTAL']),
                'injuries.fatal': safe_int(row['INJURIES_FATAL']),
                'injuries.non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL']),
                f'contributing_factors.{row["PRIM_CONTRIBUTORY_CAUSE"]}': 1
            }
        }
        daily.update_one({'date': crash_date, 'area': area}, {'$inc': daily_doc['$inc']}, upsert=True)

        week_start, week_end = get_week_range(crash_date)
        weekly_doc = {
            'week_start': str(week_start),
            'week_end': str(week_end),
            'area': area,
            '$inc': {
                'total_accidents': 1,
                'injuries.total': safe_int(row['INJURIES_TOTAL']),
                'injuries.fatal': safe_int(row['INJURIES_FATAL']),
                'injuries.non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL']),
                f'contributing_factors.{row["PRIM_CONTRIBUTORY_CAUSE"]}': 1
            }
        }
        weakly.update_one({'week_start': str(week_start), 'week_end': str(week_end), 'area': area}, {'$inc': weekly_doc['$inc']}, upsert=True)

        monthly_doc = {
            'year': str(crash_date.year),
            'month': str(crash_date.month),
            'area': area,
            '$inc': {
                'total_accidents': 1,
                'injuries.total': safe_int(row['INJURIES_TOTAL']),
                'injuries.fatal': safe_int(row['INJURIES_FATAL']),
                'injuries.non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL']),
                f'contributing_factors.{row["PRIM_CONTRIBUTORY_CAUSE"]}': 1
            }
        }
        monthly.update_one({'year': str(crash_date.year), 'month': str(crash_date.month), 'area': area}, {'$inc': monthly_doc['$inc']}, upsert=True)

        # עדכון מסמכי areas
        update_query = {'area': area}
        update_area = {
            '$inc': {
                'total_accidents': 1,
                'injuries.total': safe_int(row['INJURIES_TOTAL']),
                'injuries.fatal': safe_int(row['INJURIES_FATAL']),
                'injuries.non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL']),
                f'contributing_factors.{row["PRIM_CONTRIBUTORY_CAUSE"]}': 1
            }
        }
        areas.update_one(update_query, update_area, upsert=True)


init_accidents()
