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

# End point to return fields for use in the frontend
@product_blueprint.route('/product/fields')
def get_product_fields():
    fields = Product.__table__.columns.keys()
    return jsonify({'fields': fields})

@product_blueprint.route("/product/search", methods=["GET"])
def search_products():
    query_field = request.args.get("field")
    query_value = request.args.get("value")

    # Handle search based on the specified field
    if query_field == "productName":
        products = Product.query.filter(Product.productName.ilike(f"%{query_value}%")).all()
    elif query_field == "supplierID":
        products = Product.query.filter_by(supplierID=query_value).all()
    elif query_field == "categoryID":
        products = Product.query.filter_by(categoryID=query_value).all()
    elif query_field == "productID":
        products = Product.query.filter_by(productID=query_value).all()
    elif query_field == "price":
        products = Product.query.filter_by(price=query_value).all()
    else:
        # Return an error response if the specified field is not supported
        return jsonify({"error": "Invalid search field"}), 400

    # Serialize the search results
    result = products_schema.dump(products)
    return jsonify(result)