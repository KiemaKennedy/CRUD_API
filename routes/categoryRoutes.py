from flask import Blueprint, request, jsonify
from models.categoryModel import Category, category_schema, categories_schema
from models import db

category_blueprint = Blueprint('category', __name__)

# CREATE CATEGORY ROUTES
# create a category
# NOTE: use request.json.get() for optional fields

@category_blueprint.route('/category', methods=['POST'])
def add_a_category():
    categoryName = request.json['categoryName']
    categoryDescription = request.json['categoryDescription']
    

    new_category = Category(categoryName, categoryDescription)
    db.session.add(new_category)
    db.session.commit()

    return category_schema.jsonify(new_category)

# Get All categories
@category_blueprint.route('/category', methods=['GET' ])
def get_all_categorys():  
    all_categories = Category.query.all()
    result = categories_schema.dump(all_categories)
    return jsonify(result)

# Get one category by ID
@category_blueprint.route("/category/<id>", methods=['GET'])
def get_one_category(id):
    category = Category.query.get(id)
    return category_schema.jsonify(category)

# Update a category
@category_blueprint.route("/category/<id>", methods=["PUT"])
def update_category(id):

    # Gets an existing category - specified by ID
    
    category = category.query.get(id)
    categoryName = request.json['categoryName']
    categoryDescription = request.json['categoryDescription']
    

    # Use the new values from the request and assign them to our category
    category.categoryName = categoryName
    category.Description = categoryDescription
    
    db.session.commit()

    return category_schema.jsonify(category)

# Delete a category
@category_blueprint.route("/category/<id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()

    return category_schema.jsonify(category)
