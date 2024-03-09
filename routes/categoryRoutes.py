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

# End point to return fields for use in the frontend
@category_blueprint.route('/category/fields')
def get_category_fields():
    fields = Category.__table__.columns.keys()
    return jsonify({'fields': fields})

@category_blueprint.route("/category/search", methods=["GET"])
def search_categories():
    query_field = request.args.get("field")
    query_value = request.args.get("value")

    # Handle search based on the specified field
    if query_field == "categoryName":
        category = Category.query.filter(Category.categoryName.ilike(f"%{query_value}%")).all()
    elif query_field == "categoryID":
        category = Category.query.filter_by(categoryID=query_value).all()
    elif query_field == "categoryDescription":
        category = Category.query.filter_by(Category.categoryDescription.ilike(f"%{query_value}%")).all()
    else:
        # Return an error response if the specified field is not supported
        return jsonify({"error": "Invalid search field"}), 400

    # Serialize the search results
    result = categories_schema.dump(category)
    return jsonify(result)
