from flask import Blueprint, request, jsonify
from models.supplierModel import Supplier, supplier_schema, suppliers_schema
from models import db

supplier_blueprint = Blueprint('suppliers', __name__)

# CREATE SUPPLIER ROUTES
# create a supplier
# NOTE: use request.json.get() for optional fields

@supplier_blueprint.route('/supplier', methods=['POST'])
def add_a_supplier():
    supplierName = request.json['supplierName']
    contactname = request.json['contactName']
    supplierAddress = request.json['supplierAddress']
    supplierCity = request.json.get('supplierCity')
    supplierPostalCode = request.json.get('supplierPostalCode')
    supplierCountry = request.json.get('supplierCountry')
    phoneNumber = request.json.get( 'phoneNumber') 

    new_supplier = Supplier(supplierName, contactname, supplierAddress, supplierCity, supplierPostalCode, supplierCountry, phoneNumber)
    db.session.add(new_supplier)
    db.session.commit()

    return supplier_schema.jsonify(new_supplier)

# Get All suppliers
@supplier_blueprint.route('/supplier', methods=['GET' ])
def get_all_suppliers():  
    all_suppliers = Supplier.query.all()
    result = suppliers_schema.dump(all_suppliers)
    return jsonify(result)

# Get one supplier by ID
@supplier_blueprint.route("/supplier/<id>", methods=['GET'])
def get_one_supplier(id):
    supplier = Supplier.query.get(id)
    return supplier_schema.jsonify(supplier)

# Update a supplier
@supplier_blueprint.route("/supplier/<id>", methods=["PUT"])
def update_supplier(id):

    # Gets an existing supplier - specified by ID
    
    supplier = Supplier.query.get(id)
    supplierName = request.json['supplierName']
    contactName = request.json['contactName']
    supplierAddress = request.json['supplierAddress']
    supplierCity = request.json.get('supplierCity')
    supplierPostalCode = request.json.get('supplierPostalCode')
    supplierCountry = request.json.get('supplierCountry')
    phoneNumber = request.json.get( 'phoneNumber')

    # Use the new values from the request and assign them to our supplier
    supplier.supplierName = supplierName
    supplier.contactName = contactName
    supplier.supplierAddress = supplierAddress
    supplier.supplierCity = supplierCity
    supplier.supplierPostalCode = supplierPostalCode
    supplier.supplierCountry = supplierCountry
    supplier.phoneNumber = phoneNumber

    db.session.commit()

    return supplier_schema.jsonify(supplier)

# Delete a supplier
@supplier_blueprint.route("/supplier/<id>", methods=["DELETE"])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    db.session.delete(supplier)
    db.session.commit()

    return supplier_schema.jsonify(supplier)
