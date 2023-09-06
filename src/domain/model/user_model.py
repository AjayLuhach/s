from infrastructure.user_database import db 
class user_model(db.Model):
    __tablename__ = 'userapi'
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(255),nullable = False)
    last_name = db.Column(db.String(255),nullable = True)
    email = db.Column(db.String(255),nullable =False)
    __table_args__ = {'extend_existing': True}
    
    
