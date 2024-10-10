from database.connect import daily, weakly, monthly, areas


def create_indexes():
    daily.create_index([('area', 1), ('date', 1)])
    print("Index created on 'daily' collection: ['area', 'date']")

    weakly.create_index([('area', 1), ('week_start', 1), ('week_end', 1)])
    print("Index created on 'weakly' collection: ['area', 'week_start', 'week_end']")

    monthly.create_index([('area', 1), ('year', 1), ('month', 1)])
    print("Index created on 'monthly' collection: ['area', 'year', 'month']")

    areas.create_index([('area', 1)])
    print("Index created on 'areas' collection: ['area']")


def compare_performance():
    executionStats_without_index = (daily
    .find({'area': '883'})
    .hint({'$natural': 1})
    .explain()['executionStats'])

    executionStats_with_index = (daily
    .find({'area': '883', 'date': {'$gte': '2024-01-01'}})
    .hint([('area', 1), ('date', 1)])
    .explain()['executionStats'])

    print("Execution stats without index on 'daily':")
    print(executionStats_without_index)

    print("\nExecution stats with index on 'daily':")
    print(executionStats_with_index)


