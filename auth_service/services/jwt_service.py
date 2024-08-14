
import logging
from datetime import datetime, timedelta

import jwt
import pytz

from ..models.user import User

class JwtService:

    SECRET_KEY = "random_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_jwt(self, user: User):
        to_encode = user.model_dump()
        expire = datetime.now(pytz.UTC) + timedelta(minutes=JwtService.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JwtService.SECRET_KEY, algorithm=JwtService.ALGORITHM)
        return encoded_jwt

    def is_valid_jwt(self, token: str):
        try:
            jwt.decode(token, JwtService.SECRET_KEY, algorithms=[JwtService.ALGORITHM])
            return True
        except jwt.ExpiredSignatureError as e:
            self.logger.error(e)
            return False
        except jwt.InvalidTokenError as e:
            self.logger.error(e)
            return False
