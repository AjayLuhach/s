from infrastructure.user_database import db 
from domain.model.user_model import user_model

class repositoryinterface:
    def __init__(self,session):
        self.session = session
        
    def create(self,username,first_name,last_name,email,password1):
        newuser = user_model(username=username,first_name=first_name,last_name=last_name,email=email,password1=password1)
        self.session.add(newuser)
        self.session.commit()
        return newuser
    def alluser(self):
        return self.session.query(user_model).all()
    def auser(self,username):
        oneuser = self.session.query(user_model).filter_by(username=username).first()          
        return oneuser
        
    def deleteuser(self,theuser):
        self.session.delete(theuser)
        self.session.commit()
        return theuser
    def updateuser(self,theuser):
        self.session.commit()
    
    