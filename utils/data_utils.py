from datetime import timedelta, datetime


def get_week_range(date):
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start.date(), end.date()


def parse_date(date_str: str):
    has_seconds = len(date_str.split(' ')) > 2
    date_format = '%m/%d/%Y %H:%M:%S %p' if has_seconds else '%m/%d/%Y %H:%M'
    return datetime.strptime(date_str, date_format)


def safe_int(value) -> int | None:
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return 0
    elif value is None or value == "":
        return 0
    else:
        return value
