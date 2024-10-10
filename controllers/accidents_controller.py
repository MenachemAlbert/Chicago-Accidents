from flask import Blueprint, jsonify
from returns.result import Success

from repository.area_repository import get_all_accidents_by_area
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
