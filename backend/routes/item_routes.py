from flask import Blueprint, request, jsonify
from models import db  # ,MyModel

my_route_bp = Blueprint("item_bp", __name__)


@my_route_bp.route("/my_route", methods=["POST"])
def create_my_item():
    data = request.get_json()
    # new_item = MyModel(

    # )
    # db.session.add(new_item)
    # db.session.commit()
    # return jsonify(new_item.to_json()), 201
    return 200
