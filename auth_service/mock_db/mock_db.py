from ..models.user import User

class MockDB:
    def __init__(self):
        self.users_db = {
            "challenge@user.com": {
                "username": "challenge@user.com",
                "email": "challenge@user.com",
                "hashed_password": "fakehashedsecret"
            }
        }

    def get_user_by_email(self, email):
        if email in self.users_db:
            user_dict = self.users_db[email]
            return User(**user_dict)
        
    def get_hashed_password(self, email):
        if email in self.users_db:
            return self.users_db[email]["hashed_password"]
