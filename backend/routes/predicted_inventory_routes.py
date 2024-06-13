from flask import Blueprint, request, jsonify
from models import db, PredictedInventory, HistoricalInventory
from datetime import timedelta
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

predicted_inventory_bp = Blueprint("predicted_inventory_bp", __name__)


@predicted_inventory_bp.route("/predicted_inventory", methods=["POST"])
def create_predicted_inventory():
    data = request.get_json()
    new_record = PredictedInventory(
        product_id=data["product_id"],
        date=data["date"],
        predicted_quantity=data["predicted_quantity"],
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_json()), 201


# Use a time series model that accounts for trends and seasonality called Holt-Winters exponential smoothing.
@predicted_inventory_bp.route("/predict_inventory", methods=["POST"])
def predict_inventory():
    data = request.get_json()
    product_id = data["product_id"]
    historical_data = HistoricalInventory.query.filter_by(product_id=product_id).all()

    if len(historical_data) < 3:
        return (
            jsonify({"message": "Not enough historical data to make a prediction"}),
            400,
        )

    dates = [record.date for record in historical_data]
    quantities = [record.quantity for record in historical_data]

    df = pd.DataFrame({"date": dates, "quantity": quantities})
    df.set_index("date", inplace=True)
    df = df.sort_index()

    model = ExponentialSmoothing(
        df["quantity"], seasonal="add", seasonal_periods=7
    ).fit()
    prediction = model.forecast(1)

    prediction_date = df.index[-1] + timedelta(days=1)
    predicted_quantity = prediction.iloc[0]

    predicted_record = PredictedInventory(
        product_id=product_id,
        date=prediction_date,
        predicted_quantity=predicted_quantity,
    )
    db.session.add(predicted_record)
    db.session.commit()
    return jsonify(predicted_record.to_json()), 201


@predicted_inventory_bp.route("/predicted_inventory", methods=["GET"])
def get_predicted_inventory():
    records = PredictedInventory.query.all()
    return jsonify([record.to_json() for record in records])


@predicted_inventory_bp.route("/predicted_inventory/<int:id>", methods=["GET"])
def get_predicted_inventory_record(id):
    record = PredictedInventory.query.get_or_404(id)
    return jsonify(record.to_json())


@predicted_inventory_bp.route("/predicted_inventory/<int:id>", methods=["PUT"])
def update_predicted_inventory(id):
    record = PredictedInventory.query.get_or_404(id)
    data = request.get_json()
    record.product_id = data["product_id"]
    record.date = data["date"]
    record.predicted_quantity = data["predicted_quantity"]
    db.session.commit()
    return jsonify(record.to_json())


@predicted_inventory_bp.route("/predicted_inventory/<int:id>", methods=["DELETE"])
def delete_predicted_inventory(id):
    record = PredictedInventory.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully"})
