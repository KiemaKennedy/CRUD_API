from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from routes.productRoutes import product_blueprint

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

# Rgeister blueprint
app.register_blueprint(product_blueprint)

# Run Server
if __name__ ==  '__main__':
    app.run(debug=True)