from infrastructure.user_database import db  
from flask_login import UserMixin
 
class user_model(UserMixin,db.Model):
    __tablename__ = 'userapi'
    username = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False)
    password1  = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return self.username
    
