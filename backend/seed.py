from datetime import datetime, timedelta
import random
from models import db, Product, HistoricalInventory, PredictedInventory
from config import app
import logging

logging.basicConfig(level=logging.DEBUG)


def seed_products():
    products = [
        {"name": "Surgical Gloves", "description": "Disposable surgical gloves"},
        {"name": "Sterile Syringes", "description": "Sterile syringes for injections"},
        {"name": "IV Solution", "description": "Intravenous saline solution"},
        {
            "name": "Antiseptic Wipes",
            "description": "Wipes for cleaning and disinfecting surfaces",
        },
        {"name": "Medical Masks", "description": "Protective masks for medical use"},
        {"name": "Bandages", "description": "Adhesive bandages for minor wounds"},
    ]

    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)

    db.session.commit()


def seed_inventory():
    products = Product.query.all()
    start_date = datetime.now() - timedelta(days=3 * 365)
    for product in products:
        current_date = start_date
        while current_date <= datetime.now():
            quantity = random.randint(50, 200)
            historical_record = HistoricalInventory(
                product_id=product.id, date=current_date, quantity=quantity
            )

            if random.random() < 0.1:
                predicted_quantity = quantity
            else:
                predicted_quantity = int(quantity * random.uniform(0.8, 1.2))

            predicted_record = PredictedInventory(
                product_id=product.id,
                date=current_date,
                predicted_quantity=predicted_quantity,
            )
            db.session.add(historical_record)
            db.session.add(predicted_record)
            logging.debug(
                f"HistoricalInventory: {product.id}, Date: {current_date}, Quantity: {quantity}"
            )
            logging.debug(
                f"PredictedInventory: {product.id}, Date: {current_date}, Predicted Quantity: {predicted_quantity}"
            )
            current_date += timedelta(days=1)

    db.session.commit()


def main():
    with app.app_context():
        db.create_all()
        seed_products()
        seed_inventory()
        print("Database seeded successfully.")


if __name__ == "__main__":
    main()
