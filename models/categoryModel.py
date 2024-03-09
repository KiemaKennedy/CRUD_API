from . import db, ma

# Create a Product Class/Model
class Category(db.Model):
    categoryID = db.Column(db.Integer, primary_key=True) #autoincrement by default
    categoryName = db.Column(db.String(100), unique=True)
    categoryDescription = db.Column(db.String(200))

    def  __init__(self, categoryName, categoryDescription):
        self.categoryName = categoryName
        self.categoryDescription = categoryDescription

# Product Schema
class  CategorySchema(ma.Schema):
    class Meta:
        fields = ('categoryID', 'categoryName', 'categoryDescription')

# Init Schema
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)