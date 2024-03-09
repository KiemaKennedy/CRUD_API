from flask import Blueprint, request, jsonify
from models.productModel import Product, product_schema, products_schema
from models import db

product_blueprint = Blueprint('products', __name__)

# CREATE PRODUCT ROUTES
# create a product
# NOTE: use request.json.get() for optional fields
@product_blueprint.route('/product', methods=['POST'])
def add_a_product():
    productName = request.json["productName"]
    supplierID = request.json["supplierID"]
    categoryID = request.json["categoryID"]
    unit = request.json["unit"]
    price = request.json["price"]

    new_product = Product(productName, supplierID, categoryID, unit, price)
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
def get_one_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# Update a Product
@product_blueprint.route("/product/<id>", methods=["PUT"])
def update_product(id):

    # Gets an existing product - specified by ID
    product = Product.query.get(id)
    productName = request.json["productName"]
    supplierID = request.json["supplierID"]
    categoryID = request.json["categoryID"]
    unit = request.json["unit"]
    price = request.json["price"]

    # Use get the new values from the request and assign them to our product
    product.productName = productName
    product.supplierID = supplierID
    product.categoryID = categoryID
    product.unit = unit
    product.price = price

    db.session.commit()

    return product_schema.jsonify(product)

# Delete a product
@product_blueprint.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)
