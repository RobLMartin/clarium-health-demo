from flask import Blueprint, request, jsonify
from models import db, InventoryAlert

inventory_alert_bp = Blueprint("inventory_alert_bp", __name__)


@inventory_alert_bp.route("/inventory_alerts", methods=["POST"])
def create_inventory_alert():
    data = request.get_json()
    new_alert = InventoryAlert(
        product_id=data["product_id"],
        alert_type=data["alert_type"],
        alert_message=data["alert_message"],
    )
    db.session.add(new_alert)
    db.session.commit()
    return jsonify(new_alert.to_json()), 201


@inventory_alert_bp.route("/inventory_alerts", methods=["GET"])
def get_inventory_alerts():
    alerts = InventoryAlert.query.all()
    return jsonify([alert.to_json() for alert in alerts])


@inventory_alert_bp.route("/inventory_alerts/<int:id>", methods=["GET"])
def get_inventory_alert(id):
    alert = InventoryAlert.query.get_or_404(id)
    return jsonify(alert.to_json())


@inventory_alert_bp.route("/inventory_alerts/<int:id>", methods=["PUT"])
def update_inventory_alert(id):
    alert = InventoryAlert.query.get_or_404(id)
    data = request.get_json()
    alert.product_id = data["product_id"]
    alert.alert_type = data["alert_type"]
    alert.alert_message = data["alert_message"]
    db.session.commit()
    return jsonify(alert.to_json())


@inventory_alert_bp.route("/inventory_alerts/<int:id>", methods=["DELETE"])
def delete_inventory_alert(id):
    alert = InventoryAlert.query.get_or_404(id)
    db.session.delete(alert)
    db.session.commit()
    return jsonify({"message": "Alert deleted successfully"})
