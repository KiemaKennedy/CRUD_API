from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize App
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Create a Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init database
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Create a Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) #autoincrement by default
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def  __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema
class  ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# CREATE ROUTES
# create a product
@app.route('/product', methods=['POST'])
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
@app.route('/product', methods=['GET' ])
def get_all_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

# Get one product by ID
@app.route("/product/<id>", methods=['GET'])
def  get_one_product(id):
    product = Product.query.get(id)
    return  product_schema.jsonify(product)

# Update a Product
@app.route("/product/<id>", methods=["PUT"])
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
@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)

# Run Server
if __name__ ==  '__main__':
    app.run(debug=True)