from config import app, db
from routes.product_routes import product_bp
from routes.historical_inventory_routes import historical_inventory_bp

app.register_blueprint(product_bp)
app.register_blueprint(historical_inventory_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
