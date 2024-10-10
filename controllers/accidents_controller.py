from datetime import datetime

from flask import Blueprint, jsonify, request
from returns.result import Success

from repository.accidents_repository import get_all_accidents_by_area, get_accidents_by_area_day, \
    get_accidents_by_area_week, get_accidents_by_area_month, get_all_accidents_by_area_cause
from utils.json_util import parse_json

accidents_blueprint = Blueprint("accidents", __name__)


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
