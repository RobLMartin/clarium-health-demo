from config import app, db
from routes.product_routes import product_bp

app.register_blueprint(product_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
