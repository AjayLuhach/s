from infrastructure.user_database import db 
from domain.model.user_model import user_model

class repositoryinterface:
    def __init__(self,session):
        self.session = session
        
    def create(self,first_name,last_name,email):
        newuser = user_model(first_name=first_name,last_name=last_name,email=email)
        self.session.add(newuser)
        self.session.commit()
        return newuser
    def alluser(self):
        return self.session.query(user_model).all()
    def auser(self,first_name):
        oneuser = self.session.query(user_model).filter_by(first_name=first_name).first()          
        return oneuser
        
    def deleteuser(self,theuser):
        self.session.delete(theuser)
        self.session.commit()
        return theuser
    def updateuser(self,theuser):
        self.session.commit()
    
    