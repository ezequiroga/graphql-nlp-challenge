import requests
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from ..config.envs import Envs

OAUTH_SERVICE_URL = Envs.get_oauth_service_url()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def validate_jwt_with_oauth_service(token: str):
    response = requests.get(f"{OAUTH_SERVICE_URL}/validate", params={"token": token})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return validate_jwt_with_oauth_service(token)
