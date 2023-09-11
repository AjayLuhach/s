from flask import Flask
from services.crud_service import crud_service
from flask import request, jsonify,url_for,session,redirect 
from domain.model.user_model import user_model
from infrastructure.user_database import db 
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_login import current_user
from flask_oauthlib.client import OAuth
from authlib.integrations.flask_client import OAuth
import os
app= Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object('config')
app.secret_key = 'ajay'
app.config['SERVER_NAME'] = 'localhost:80'
oauth = OAuth(app)

db.init_app(app)
with app.app_context():
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return user_model.query.get(username)



def custom_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        return func(*args, **kwargs)
    return decorated_view


# intialize service
service = crud_service(db.session)

@app.route('/')
def home():
    return 'hello jessie'


@app.route('/google/')
def google():
   
    # Google Oauth Config
    # Get client_id and client_secret from environment variables
    # For developement purpose you can directly put it
    # here inside double quotes
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
     
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id='600241584403-4heepbpsj6e18mu1s5qa7g57l4b2m9v3.apps.googleusercontent.com',
        client_secret='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',
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
     
    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
 
@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print(" Google User ", user)
    return redirect('/')





@app.route('/create', methods=['POST'])
def register_user():
     
    username = request.args.get('username')
    password1 = request.args.get('password1')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    password2 = bcrypt.generate_password_hash(password1).decode('utf-8')
    new_user = service.create(username, first_name,
                              last_name, email, password2)
    return f"created user: %s" % new_user.first_name




# @app.route('/login', methods=['POST'])
# def login():
#     # gget username and password from the request
#     username = request.args.get('username')
#     password = request.args.get('password')

#     # eertrieve the user from the database
#     user = service.auser(username)
 
 

#     if bcrypt.check_password_hash(user.password1, password):
#             login_user(user)
#             return jsonify({'message': 'Login successful'})
#     else:
#         # Invalid username or password
#         return jsonify({'error': 'Invalid username or password'}), 401

    
    
@app.route("/logout")
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})


# to see all users
@app.route('/alluser')
 
def all_user():
    users = service.alluser()
    user_list = [{"username": user.username, "first_name": user.first_name,
                  "last_name": user.last_name, "email": user.email} for user in users]

    return jsonify(user_list)

# to search a specific user


@app.route('/search', methods=['GET'])
def search_user():
    username = request.args.get('username')
    user = service.auser(username)
    if user:
        user_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        return jsonify(user_data)
    else:

        return jsonify({"error": "User not found"}), 404
# to delete a user


@app.route('/delete', methods=['DELETE'])
def delete_user():

    username = request.args.get('username')
    deleted = service.deleteuser(username)

    if deleted:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

# to update a user


@app.route('/update', methods=['PUT'])
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



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
 