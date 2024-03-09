from . import db, ma
from models.categoryModel import Category

# Create a Product Class/Model
class Product(db.Model):
    productID = db.Column(db.Integer, primary_key=True) #autoincrement by default
    productName = db.Column(db.String(100), unique=True)
    supplierID = db.Column(db.Integer, db.ForeignKey('supplier.supplierID'))
    categoryID = db.Column(db.Integer, db.ForeignKey('category.categoryID'))
    unit = db.Column(db.String(100))
    price = db.Column(db.Float)

    # create foreign keys for supplierID and categoryID
    supplier = db.relationship('Supplier', foreign_keys=[supplierID])
    category = db.relationship('Category', foreign_keys=[categoryID])

    def  __init__(self, productName, supplierID, categoryID, unit, price):
        self.productName = productName
        self.supplierID = supplierID
        self.categoryID = categoryID
        self.unit = unit
        self.price = price

# Product Schema
class  ProductSchema(ma.Schema):
    class Meta:
        fields = ('productID', 'productName', 'supplierID', 'categoryID', 'unit', 'price')

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)