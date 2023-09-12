from flask import Flask
from services.crud_service import crud_service
from flask import request, jsonify, url_for, session, redirect
from domain.model.user_model import user_model
from infrastructure.user_database import db
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from functools import wraps
from flask_login import current_user
from flask_oauthlib.client import OAuth
import random
import string

# create a Flask app instance
app = Flask(__name__)

# initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# load configuration from a 'config' object
app.config.from_object('config')

# set a secret key for the application (used for session management)
app.secret_key = 'ajay'

# initialize the database
db.init_app(app)

# create all database tables (if they don't exist)
with app.app_context():
    db.create_all()

# initialize Flask-Login for user session management
login_manager = LoginManager()
login_manager.init_app(app)

# user loader function for Flask-Login
@login_manager.user_loader
def load_user(username):
    return user_model.query.get(username)

# custom decorator to require authentication for certain routes
def custom_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'authentication required'}), 401
        return func(*args, **kwargs)
    return decorated_view

# initialize a service for CRUD operations on the database
service = crud_service(db.session)

# Google OAuth configuration
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key='600241584403-4heepbpsj6e18mu1s5qa7g57l4b2m9v3.apps.googleusercontent.com',  # replace with your client ID
    consumer_secret='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',  # replace with your client secret
    request_token_params={
        'scope': 'openid profile email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
# Flask route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return 'hello'  # a simple response for the home page

# Flask route for initiating the Google OAuth login
@app.route('/google/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True, _scheme='http'))  # start Google OAuth

# Flask route for handling Google OAuth authorization callback
@app.route('/login/google/callback')
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )  # Handle access denial or errors

    session['google_token'] = (resp['access_token'], '')  # Store Google access token in the session
    user_info = google.get('userinfo')  # Get user information from Google

    # Extract user information from the Google response
    username = user_info.data.get('email')  # Use email as the username
    first_name = user_info.data.get('given_name')
    last_name = user_info.data.get('family_name')
    email = user_info.data.get('email')

    # Generate a random password for the user (you can change this logic)
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    # check for already exisitng user 
    user = service.auser(username)
    if not user:
        # If the user does not exist, create a new user in the system
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = service.create(username, first_name, last_name, email, password_hash)
        login_user(new_user)  # Log in the new user
    else:
        login_user(user)  # Log in the existing user

    return redirect('/alluser')  # Redirect the user to a desired page

# OAuth token getter function for Flask-OAuthlib
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

# Flask route for creating a new user
@app.route('/create', methods=['POST'])
def register_user():
    username = request.args.get('username')
    password1 = request.args.get('password1')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email')
    password2 = bcrypt.generate_password_hash(password1).decode('utf-8')
    
    # Create a new user with provided information
    new_user = service.create(username, first_name, last_name, email, password2)
    
    return f"created user: %s" % new_user.first_name  # Return a message indicating successful user creation

# Flask route for user login
@app.route('/login', methods=['POST'])
def login_new_user():
    username = request.args.get('username')
    password = request.args.get('password')

    # Retrieve the user from the database
    user = service.auser(username)

    if bcrypt.check_password_hash(user.password1, password):
        login_user(user)  # Log in the user if password matches
        return jsonify({'message': 'login successful'})
    else:
        # Return an error message for invalid username or password
        return jsonify({'error': 'invalid username or password'}), 401

# Flask route for user logout
@app.route("/logout")
def logout():
    logout_user()  # Log out the user
    return jsonify({'message': 'logout successful'})

# Flask route to retrieve a list of all users (authentication required)
@app.route('/alluser')
@custom_login_required  # Require authentication for this route
def all_user():
    users = service.alluser()  # Retrieve all users from the database
    user_list = [{"username": user.username, "first_name": user.first_name,
                  "last_name": user.last_name, "email": user.email} for user in users]

    return jsonify(user_list)  # Return the list of users in JSON format

# Flask route to search for a specific user by username
@app.route('/search', methods=['GET'])
def search_user():
    username = request.args.get('username')
    user = service.auser(username)  # Search for a user by username in the database
    if user:
        user_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }
        return jsonify(user_data)  # Return user information if found
    else:
        return jsonify({"error": "user not found"}), 404  # Return an error if user is not found

# Flask route to delete a user by username
@app.route('/delete', methods=['DELETE'])
def delete_user():
    username = request.args.get('username')
    deleted = service.deleteuser(username)  # Delete a user by username from the database

    if deleted:
        return jsonify({'message': 'user deleted successfully'})  # Return success message
    else:
        return jsonify({'error': 'user not found'}), 404  # Return an error if user is not found

# Flask route to update user information
@app.route('/update', methods=['PUT'])
def update_user():
    username = request.args.get('username')
    new_first_name = request.args.get('first_name')
    new_last_name = request.args.get('last_name')
    new_email = request.args.get('email')
    new_password = request.args.get('password')

    updated = service.updateuser(username, new_first_name, new_last_name, new_email, new_password)

    if updated:
        return jsonify({'message': 'user updated successfully'})  # Return success message
    else:
        return jsonify({'error': 'user not found'}),  # Return an error if user is not found

# Run the Flask application on host 0.0.0.0 and port 80
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
