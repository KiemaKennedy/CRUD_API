from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from routes.productRoutes import product_blueprint
from models import db, ma
import os

# Initialize App
# app = Flask(__name__)

# # # Init database
# db = SQLAlchemy()

# # # Initialize Marshmallow
# ma = Marshmallow()
def create_app(config_name):
    app = Flask(__name__)

    # basedir = os.path.abspath(os.path.dirname(__file__))

    # Define SQLAlchemy configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(product_blueprint)

    return app


# Run Server
if __name__ == '__main__':
    #  Use the "development" configuration for local testing
    app = create_app(config_name='development')
    app.run(debug=True)
