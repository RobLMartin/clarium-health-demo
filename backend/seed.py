from datetime import datetime, timedelta
import random
from models import db, Product, HistoricalInventory
from config import app


def seed_products():
    products = [
        {"name": "Surgical Gloves", "description": "Disposable surgical gloves"},
        {"name": "Sterile Syringes", "description": "Sterile syringes for injections"},
        {"name": "IV Solution", "description": "Intravenous saline solution"},
    ]

    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()


def seed_historical_inventory():
    products = Product.query.all()
    start_date = datetime.now() - timedelta(days=3 * 365)
    for product in products:
        current_date = start_date
        while current_date <= datetime.now():
            quantity = random.randint(50, 200)  # Random quantity between 50 and 200
            record = HistoricalInventory(
                product_id=product.id, date=current_date.date(), quantity=quantity
            )
            db.session.add(record)
            current_date += timedelta(days=1)

    db.session.commit()


def main():
    with app.app_context():
        db.create_all()
        seed_products()
        seed_historical_inventory()
        print("Database seeded successfully.")


if __name__ == "__main__":
    main()
