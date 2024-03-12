from flask import Flask
from routes.productRoutes import product_blueprint
from routes.supplierRoutes import supplier_blueprint
from routes.categoryRoutes import category_blueprint
from routes.authRoutes import auth_bp
from flask_cors import CORS
from models import db, ma
import os


app = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))

# Define SQLAlchemy configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

app.register_blueprint(product_blueprint)
app.register_blueprint(supplier_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(auth_bp)

CORS(app)

    # Function to create or update tables/models in the db on app startup
def create_or_update_tables():
    with app.app_context():
        db.create_all()

# Call the function to create or update tables
create_or_update_tables()

# Run Server
if __name__ == '__main__':
    #  Use the "development" configuration for local testing
    app.run(debug=True)