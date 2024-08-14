
from ..daos.auth_dao import AuthDAO

class AuthService:

    def __init__(self):
        self.dao = AuthDAO()

    def authenticate(self, email, password):
        user = self.dao.get_user_by_email(email)

        if not user:
            return False
        
        if not self.dao.get_hashed_password(email) == password:
            return False
        
        return user
