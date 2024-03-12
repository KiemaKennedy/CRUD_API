from flask import Blueprint, request, jsonify
from models.authModel import User, Session, session_schema, sessions_schema, user_schema, users_schema
from models import db
import re
from datetime import datetime
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)
login_cache = {}

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['Email']):
        return jsonify({'message': 'Invalid email format'}), 400
    
    # Check if the email is already registered
    existing_user = User.query.filter_by(Email=data['Email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400
    
    # Validate password strength
    password = data['Password']
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400
    if not any(char.isupper() for char in password):
        return jsonify({'message': 'Password must contain at least one uppercase letter'}), 400
    if not any(char.islower() for char in password):
        return jsonify({'message': 'Password must contain at least one lowercase letter'}), 400
    if not any(char.isdigit() for char in password):
        return jsonify({'message': 'Password must contain at least one digit'}), 400
    if not any(char in '!@#$%^&*()-_=+[{]}\|;:\'",<.>/?' for char in password):
        return jsonify({'message': 'Password must contain at least one special character'}), 400
    
    new_user = User(
        Name=data['Name'],
        Phone=data['Phone'],
        Email=data['Email'],
        Position=data['Position'],
        Department=data['Department'],
        Role=data['Role']
    )
    new_user.set_password(data['Password'])  # Hash the password

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['Email']
    password = data['Password']
    # user = User.query.filter_by(Email=email).first()
     # Check if the email and password combination has already been checked
    if (email, password) in login_cache:
        user = login_cache[(email, password)]
    else:
        # Check if the email exists in the user table
        user = User.query.filter_by(Email=email).first()
        
        # Cache the result
        login_cache[(email, password)] = user
    if user and check_password_hash(user.Password, password):
        # Create a new session record
        new_session = Session(
            UserID=user.UserID,
            Name=user.Name,
            # Email=user.Email,
            IPAddress=request.remote_addr,  # Get IP address of the client
            Timestamp=datetime.now()  # Current timestamp
        )
        db.session.add(new_session)
        db.session.commit()

        return jsonify({
            'message': 'Login successful',
            'user': {
                'UserID': user.UserID,
                'Name': user.Name,
                'Phone': user.Phone,
                'Email': user.Email,
                'Position': user.Position,
                'Department': user.Department,
                'Role': user.Role
            }
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
# Get all users
@auth_bp.route('/users', methods=['GET' ])
def get_all_users():  
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

# Get a user by ID
@auth_bp.route("/users/<id>", methods=['GET'])
def get_one_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User does not exist '}), 404
    return user_schema.jsonify(user)

# Update a User
@auth_bp.route("/users/<id>", methods=["PUT"])
def update_user(id):
    # Gets an existing user - specified by ID
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    # Update user attributes from request data
    user.Name = data.get('Name', user.Name)
    user.Phone = data.get('Phone', user.Phone)
    user.Email = data.get('Email', user.Email)
    user.Position = data.get('Position', user.Position)
    user.Department = data.get('Department', user.Department)
    user.Role = data.get('Role', user.Role)

    # Check if the user wants to update the password
    new_password = data.get('Password')
    if new_password:
        user.set_password(new_password)  # Hash the new password

    db.session.commit()

    # return user_schema.jsonify(user)
    return jsonify({'message': f'User {user.UserID} updated successfully'}), 201

# Delete a user
@auth_bp.route("/users/<id>", methods=["DELETE"])
def delete_product(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
