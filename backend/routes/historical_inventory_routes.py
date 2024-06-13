from flask import Blueprint, request, jsonify
from models import db, HistoricalInventory

historical_inventory_bp = Blueprint("historical_inventory_bp", __name__)


@historical_inventory_bp.route("/historical_inventory", methods=["POST"])
def create_historical_inventory():
    data = request.get_json()
    new_record = HistoricalInventory(
        product_id=data["product_id"], date=data["date"], quantity=data["quantity"]
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_json()), 201


@historical_inventory_bp.route("/historical_inventory", methods=["GET"])
def get_historical_inventory():
    records = HistoricalInventory.query.all()
    return jsonify([record.to_json() for record in records])


@historical_inventory_bp.route("/historical_inventory/<int:id>", methods=["GET"])
def get_historical_inventory_record(id):
    record = HistoricalInventory.query.get_or_404(id)
    return jsonify(record.to_json())


@historical_inventory_bp.route("/historical_inventory/<int:id>", methods=["PUT"])
def update_historical_inventory(id):
    record = HistoricalInventory.query.get_or_404(id)
    data = request.get_json()
    record.product_id = data["product_id"]
    record.date = data["date"]
    record.quantity = data["quantity"]
    db.session.commit()
    return jsonify(record.to_json())


@historical_inventory_bp.route("/historical_inventory/<int:id>", methods=["DELETE"])
def delete_historical_inventory(id):
    record = HistoricalInventory.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully"})
