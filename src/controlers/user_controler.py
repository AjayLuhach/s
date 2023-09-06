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
def create_user():    
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')

    new_user =  service.create(first_name,last_name,email)
    return f"created user: %s" % first_name

 
# to see all users
@uc.route('/alluser')
def all_user():
    users = service.alluser()

    
    user_list = [{"id": user.id,"first_name":user.first_name,"last_name":user.last_name,"email":user.email} for user in users]

    return jsonify(user_list)

# to search a specific user
@uc.route('/search', methods=['GET'])
def search_user_by_first_name():     
    first_name = request.args.get('first_name') 
    user = service.auser(first_name) 
    if user: 
        user_data = {
            "id": user.id,
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
     
    first_name = request.args.get('first_name') 
    deleted = service.deleteuser(first_name)

    if deleted:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

# to update a user
@uc.route('/update', methods=['PUT'])
def update_user():
     
    first_name = request.args.get('first_name')    
    new_last_name = request.args.get('last_name')
    new_email = request.args.get('email')

    updated = service.updateuser(first_name, new_email, new_last_name)


    if updated:
        return jsonify({'message': 'User updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404