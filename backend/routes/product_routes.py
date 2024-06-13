from flask import Blueprint, request, jsonify
from models import db, Product, HistoricalInventory, PredictedInventory
from datetime import datetime, timedelta
import logging

product_bp = Blueprint("product_bp", __name__)
logging.basicConfig(level=logging.DEBUG)


@product_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = Product(name=data["name"], description=data["description"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_json()), 201


@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_json() for product in products])


@product_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_json())


@product_bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data["name"]
    product.description = data["description"]
    db.session.commit()
    return jsonify(product.to_json())


@product_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})


@product_bp.route("/products/<int:id>/inventory_data", methods=["GET"])
def get_product_inventory_data(id):
    product = Product.query.get_or_404(id)

    current_date = datetime.utcnow().date()
    start_of_today = datetime.combine(current_date, datetime.min.time())
    end_of_today = datetime.combine(current_date, datetime.max.time())
    one_week_ago = start_of_today - timedelta(days=7)
    one_week_later_end_of_day = end_of_today + timedelta(days=7)

    logging.debug(f"Current Date: {current_date}")
    logging.debug(f"One Week Ago: {one_week_ago}")
    logging.debug(f"One Week Later End of Day: {one_week_later_end_of_day}")

    historical_data_query = HistoricalInventory.query.filter(
        HistoricalInventory.product_id == id,
        HistoricalInventory.date >= one_week_ago,
        HistoricalInventory.date <= end_of_today,
    )
    predicted_data_query = PredictedInventory.query.filter(
        PredictedInventory.product_id == id,
        PredictedInventory.date >= one_week_ago,
        PredictedInventory.date <= one_week_later_end_of_day,
    )

    logging.debug("Historical Data SQL: %s", historical_data_query.statement)
    logging.debug("Predicted Data SQL: %s", predicted_data_query.statement)

    historical_data = historical_data_query.all()
    predicted_data = predicted_data_query.all()

    logging.debug(f"Historical Data Count: {len(historical_data)}")
    for record in historical_data:
        logging.debug(f"Historical Data: {record.date} - {record.quantity}")

    logging.debug(f"Predicted Data Count: {len(predicted_data)}")
    for record in predicted_data:
        logging.debug(f"Predicted Data: {record.date} - {record.predicted_quantity}")

    historical_dates = [record.date for record in historical_data]
    predicted_dates = [record.date for record in predicted_data]
    logging.debug(f"Historical Dates: {historical_dates}")
    logging.debug(f"Predicted Dates: {predicted_dates}")

    return jsonify(
        {
            "product": product.to_json(),
            "historicalData": [record.to_json() for record in historical_data],
            "predictedData": [record.to_json() for record in predicted_data],
        }
    )
