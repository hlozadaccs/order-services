from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.config import settings
from app.schemas.user import UserJWT


async def decode_jwt_token(token: str) -> UserJWT:
    try:
        payload = jwt.decode(
            token,
            settings.MONOLITHIC_PROJECT_SECRET,
            algorithms=[settings.MONOLITHIC_PROJECT_ALGORITHM],
        )
        return UserJWT(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado"
        )
