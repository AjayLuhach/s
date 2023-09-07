from flask import Blueprint, request, jsonify
from infrastructure.user_database import db
from services.crud_service import crud_service


# create blueprint for app
uc = Blueprint('uc', __name__)

# intialize service
service = crud_service(db.session)


@uc.route('/')
def home():
    return 'hello'

# to create a new user


@uc.route('/create', methods=['POST'])
def register_user():
    username = request.args.get('username')
    password1 = request.args.get('password1')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    print(username, password1)

    new_user = service.create(username, first_name,
                              last_name, email, password1)
    return f"created user: %s" % new_user.first_name

@uc.route('/login', methods=['POST'])
def login():
    # gget username and password from the request
    username = request.args.get('username')
    password = request.args.get('password')

    # eertrieve the user from the database
    user = service.auser(username)

    if user and user.password1==password:
        
        return jsonify({'message': 'Login successful'})
    else:
        # Invalid username or password
        return jsonify({'error': 'Invalid credentials'}), 401
    
    
# to see all users
@uc.route('/alluser')
def all_user():
    users = service.alluser()
    user_list = [{"username": user.username, "first_name": user.first_name,
                  "last_name": user.last_name, "email": user.email} for user in users]

    return jsonify(user_list)

# to search a specific user


@uc.route('/search', methods=['GET'])
def search_user():
    username = request.args.get('username')
    user = service.auser(username)
    if user:
        user_data = {
            "id": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        return jsonify(user_data)
    else:

        return jsonify({"error": "User not found"}), 404
# to delete a user


@uc.route('/delete', methods=['DELETE'])
def delete_user():

    username = request.args.get('username')
    deleted = service.deleteuser(username)

    if deleted:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

# to update a user


@uc.route('/update', methods=['PUT'])
def update_user():
    username = request.args.get('username')
    new_first_name = request.args.get('first_name')
    new_last_name = request.args.get('last_name')
    new_email = request.args.get('email')
    new_password = request.args.get('password')

    updated = service.updateuser(
        username, new_first_name, new_last_name, new_email, new_email, new_password)

    if updated:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}),
