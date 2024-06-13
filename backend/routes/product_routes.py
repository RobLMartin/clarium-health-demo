from flask import Blueprint, request, jsonify
from models import db, Product

product_bp = Blueprint("product_bp", __name__)


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