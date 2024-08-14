
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..services.auth_service import AuthService
from ..services.jwt_service import JwtService
from ..models.token import Token


router = APIRouter()

service = AuthService()
jwt_service = JwtService()

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = service.authenticate(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    jwt = jwt_service.generate_jwt(user)
    
    return Token(access_token=jwt, token_type="bearer")

@router.get("/validate")
async def validate_token(token: str):
    is_valid = jwt_service.is_valid_jwt(token)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid token")

