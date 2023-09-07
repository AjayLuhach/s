from infrastructure.repository_interface import repositoryinterface
from domain.entities.user_entity import user_entitiy


class crud_service():
    def __init__(self, session):
        self.repo = repositoryinterface(session)

    def create(self,username,first_name, last_name, email,password1):
        newuser = user_entitiy(username=username,first_name=first_name,last_name=last_name, email=email,password1=password1)
        return self.repo.create(username ,first_name,last_name,email,password1)

    def alluser(self):
        return self.repo.alluser()
    def auser(self,username):
        return self.repo.auser(username)
    def deleteuser(self,username):
        theuser = self.auser(username)
        if theuser:
            self.repo.deleteuser(theuser)
            return True
        return False
    def updateuser(self,username,first_name,last_name,email,password):
        theuser = self.auser(username)
        if theuser:
            theuser.first_name = first_name            
            theuser.last_name = last_name
            theuser.email = email
            theuser.password = password
            self.repo.updateuser(theuser)
        return theuser