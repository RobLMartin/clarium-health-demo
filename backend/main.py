from config import app, db
from routes.product_routes import product_bp
from routes.historical_inventory_routes import historical_inventory_bp
from routes.predicted_inventory_routes import predicted_inventory_bp
from routes.inventory_alert_routes import inventory_alert_bp

app.register_blueprint(product_bp, url_prefix="/api")
app.register_blueprint(historical_inventory_bp, url_prefix="/api")
app.register_blueprint(predicted_inventory_bp, url_prefix="/api")
app.register_blueprint(inventory_alert_bp, url_prefix="/api")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
