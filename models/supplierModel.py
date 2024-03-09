from . import db, ma

# Create a Product Class/Model
class Supplier(db.Model):
    supplierID = db.Column(db.Integer, primary_key=True) #autoincrement by default
    supplierName = db.Column(db.String(100), unique=True)
    contactName = db.Column(db.String(100))
    supplierAddress = db.Column(db.String(100))
    supplierCity = db.Column(db.String(50))
    supplierPostalCode = db.Column(db.String(20))
    supplierCountry = db.Column(db.String(60))
    phoneNumber = db.Column(db.String(30)) 

    def  __init__(self, supplierName, contactName, supplierAddress, supplierCity, supplierPostalCode, supplierCountry, phoneNumber):
        self.supplierName = supplierName
        self.contactName = contactName
        self.supplierAddress = supplierAddress
        self.supplierCity = supplierCity
        self.supplierPostalCode = supplierPostalCode
        self.supplierCountry = supplierCountry
        self.phoneNumber = phoneNumber

# Product Schema
class  SupplierSchema(ma.Schema):
    class Meta:
        fields = ('supplierID', 'supplierName', 'contactName', 'supplierAddress', 'supplierCity', 'supplierPostalCode', 'supplierCountry', 'phoneNumber')

# Init Schema
supplier_schema = SupplierSchema()
suppliers_schema = SupplierSchema(many=True)