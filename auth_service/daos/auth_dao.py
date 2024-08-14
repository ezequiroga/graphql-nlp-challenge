
from ..mock_db.mock_db import MockDB

class AuthDAO:

    def __init__(self):
        self.ds = MockDB()

    def get_user_by_email(self, email):
        return self.ds.get_user_by_email(email)
    
    def get_hashed_password(self, password):
        return self.ds.get_hashed_password(password)
