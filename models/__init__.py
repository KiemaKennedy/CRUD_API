from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize Flask extensions
db = SQLAlchemy()
ma = Marshmallow()

# Import your models here
from .productModel import Product
