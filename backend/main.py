from config import app, db

# from routes.item_routes import my_bp
# app.register_blueprint(my_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
