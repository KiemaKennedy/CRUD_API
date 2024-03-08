from flask import Blueprint, request, jsonify
from app import db
from models.productModel import Product, product_schema, products_schema

product_blueprint = Blueprint('products', __name__)

# CREATE ROUTES
# create a product
@product_blueprint.route('/product', methods=['POST'])
def add_a_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json.get('qty')

    new_product = Product(name, description, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Get All products
@product_blueprint.route('/product', methods=['GET' ])
def get_all_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get one product by ID
@product_blueprint.route("/product/<id>", methods=['GET'])
def  get_one_product(id):
    product = Product.query.get(id)
    return  product_schema.jsonify(product)

# Update a Product
@product_blueprint.route("/product/<id>", methods=["PUT"])
def update_product(id):

    # Gets an existing product - specified by ID
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json.get("description")
    price = request.json['price']
    qty = request.json['qty']

    # Use get the new  values from the request and assign them to our product
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return  product_schema.jsonify(product)

# Delete a product
@product_blueprint.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)