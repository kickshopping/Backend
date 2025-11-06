from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.auth import validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user = await validate_token(token)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No tiene permisos para acceder a este recurso",
            headers={"WWW-Authenticate": "Bearer"},
        )