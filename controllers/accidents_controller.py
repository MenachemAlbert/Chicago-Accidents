from datetime import datetime

from flask import Blueprint, jsonify, request
from returns.result import Success

from repository.area_repository import get_all_accidents_by_area, get_accidents_by_area_day
from utils.json_util import parse_json

accidents_blueprint = Blueprint("accidents", __name__)


@accidents_blueprint.route("/accidents_by_area/<area>", methods=['GET'])
def get_accidents_by_area(area):
    result = get_all_accidents_by_area(area)
    if isinstance(result, Success):
        cars_json = [parse_json(car) for car in result]
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
