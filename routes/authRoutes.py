from flask import Blueprint, request, jsonify
from models.authModel import User, Session, session_schema, sessions_schema, user_schema, users_schema
from models import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(
        Name=data['Name'],
        Phone=data['Phone'],
        Email=data['Email'],
        Position=data['Position'],
        Department=data['Department'],
        Password=data['Password'],
        Role=data['Role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['Email']
    password = data['Password']
    user = User.query.filter_by(Email=email).first()
    if user and user.Password == password:
        return jsonify({'message': 'Login successful', 'user': {
            'UserID': user.UserID,
            'Name': user.Name,
            'Phone': user.Phone,
            'Email': user.Email,
            'Position': user.Position,
            'Department': user.Department,
            'Role': user.Role
        }}), 200
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
    user.Password = data.get('Password', user.Password)
    user.Role = data.get('Role', user.Role)

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
