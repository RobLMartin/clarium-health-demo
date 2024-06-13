from flask import Blueprint, request, jsonify
from models import db, HistoricalInventory
import csv
from datetime import datetime

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


@historical_inventory_bp.route("/upload_historical_inventory", methods=["POST"])
def upload_historical_inventory():
    file = request.files["file"]
    product_id = request.form["product_id"]
    csv_reader = csv.DictReader(file.read().decode("utf-8").splitlines())
    for row in csv_reader:
        date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        quantity = float(row["quantity"])
        new_record = HistoricalInventory(
            product_id=product_id, date=date, quantity=quantity
        )
        db.session.add(new_record)
    db.session.commit()
    return jsonify({"message": "Historical inventory data uploaded successfully"}), 201


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
