from datetime import datetime

from flask import Blueprint, jsonify, request
from pymongo.errors import PyMongoError
from returns.result import Success, Failure

from repository.accidents_repository import get_all_accidents_by_area, get_accidents_by_area_day, \
    get_accidents_by_area_week, get_accidents_by_area_month, get_all_accidents_by_area_cause, get_area_stats
from repository.csv_repository import init_accidents
from repository.index_repository import create_indexes, compare_performance
from utils.json_util import parse_json

accidents_blueprint = Blueprint("accidents", __name__)


@accidents_blueprint.route('/initialize-db', methods=['POST'])
def initialize_db():
    # init_accidents()
    create_indexes()
    compare_performance()
    return {'message': 'Database initialized successfully'}, 200


@accidents_blueprint.route("/accidents_by_area/<area>", methods=['GET'])
def get_accidents_by_area(area):
    result = get_all_accidents_by_area(area)
    if isinstance(result, Success):
        cars_json = [parse_json(r) for r in result]
        return jsonify(cars_json), 200
    else:
        return jsonify({"error": result.error}), 400


@accidents_blueprint.route("/accidents_by_area_day/<area>", methods=['GET'])
def get_all_accidents_by_area_day(area):
    date_str = request.args.get('date')
    try:
        date = datetime.fromisoformat(date_str)
        result = get_accidents_by_area_day(area, date)
        return jsonify(result.unwrap()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@accidents_blueprint.route("/accidents_by_area_week/<area>", methods=['GET'])
def get_all_accidents_by_area_week(area):
    date_str = request.args.get('date')
    try:
        date = datetime.fromisoformat(date_str)
        result = get_accidents_by_area_week(area, date)
        return jsonify(result.unwrap()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@accidents_blueprint.route("/accidents_by_area_month/<area>", methods=['GET'])
def get_all_accidents_by_area_month(area):
    date_str = request.args.get('date')
    try:
        date = datetime.fromisoformat(date_str)
        result = get_accidents_by_area_month(area, date)
        return jsonify(result.unwrap()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@accidents_blueprint.route("/accidents_by_area_cause/<area>", methods=['GET'])
def get_accidents_by_area_cause(area):
    result = get_all_accidents_by_area_cause(area)
    if isinstance(result, Success):
        cars_json = [parse_json(r) for r in result]
        return jsonify(cars_json), 200
    else:
        return jsonify({"error": result.error}), 400


@accidents_blueprint.route("/area_stats/<area>", methods=['GET'])
def get_area_stats_route(area):
    try:
        result = get_area_stats(area)
        if isinstance(result, Success):
            return jsonify(result.unwrap()), 200
        elif isinstance(result, Failure):
            return jsonify({"error": result.failure()}), 404
    except PyMongoError as e:
        return jsonify({"error": str(e)}), 500
