from flask import Blueprint, request, jsonify
from models import db, PredictedInventory, HistoricalInventory
from datetime import datetime, timedelta
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

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


@predicted_inventory_bp.route("/predict_inventory", methods=["POST"])
def predict_inventory():
    data = request.get_json()
    product_id = data["productId"]
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
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df["day_of_year"] = df.index.dayofyear
    current_day_of_year = datetime.now().timetuple().tm_yday
    seasonal_data = df[df["day_of_year"] == current_day_of_year]
    for offset in range(1, 8):
        seasonal_data = pd.concat(
            [
                seasonal_data,
                df[df["day_of_year"] == ((current_day_of_year - offset) % 365)],
            ]
        )
    seasonal_data = seasonal_data.sort_index()

    seasonal_data = seasonal_data.drop(columns=["day_of_year"])

    model = ExponentialSmoothing(
        seasonal_data["quantity"], seasonal="add", seasonal_periods=7
    ).fit()

    predictions = model.forecast(30)

    noise = np.random.normal(0, seasonal_data["quantity"].std() * 0.2, len(predictions))
    predictions = predictions + noise

    predicted_records = []
    last_date = df.index.max()
    for i, quantity in enumerate(predictions):
        prediction_date = last_date + timedelta(days=i + 1)
        predicted_record = PredictedInventory(
            product_id=product_id,
            date=prediction_date,
            predicted_quantity=round(quantity),
        )
        db.session.add(predicted_record)
        predicted_records.append(predicted_record)

    db.session.commit()
    return jsonify([record.to_json() for record in predicted_records]), 201
