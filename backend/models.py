from config import db
from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class HistoricalInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    product = db.relationship("Product", backref="historical_inventory")

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "date": self.date.isoformat(),
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class PredictedInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    predicted_quantity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    product = db.relationship("Product", backref="predicted_inventory")

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "date": self.date.isoformat(),
            "predicted_quantity": self.predicted_quantity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class InventoryAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # 'overstock' or 'shortage'
    alert_message = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    product = db.relationship("Product", backref="inventory_alerts")

    def to_json(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "alert_type": self.alert_type,
            "alert_message": self.alert_message,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
