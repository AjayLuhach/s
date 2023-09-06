from infrastructure.repository_interface import repositoryinterface
from domain.entities.user_entity import user_entitiy


class crud_service():
    def __init__(self, session):
        self.repo = repositoryinterface(session)

    def create(self, first_name, last_name, email):
        newuser = user_entitiy(first_name=first_name,
                               last_name=last_name, email=email)
        return self.repo.create(first_name,last_name,email)

    def alluser(self):
        return self.repo.alluser()
    def auser(self,first_name):
        return self.repo.auser(first_name)
    def deleteuser(self,first_name):
        theuser = self.auser(first_name)
        if theuser:
            self.repo.deleteuser(theuser)
            return True
        return False
    def updateuser(self,first_name,last_name,email):
        theuser = self.auser(first_name)
        if theuser:
            theuser.email = email
            theuser.last_name = last_name
            self.repo.updateuser(theuser)
        return theuser