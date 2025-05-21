from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.schemas.user import UserJWT

# pip install python-jose
# pip install -r requirements.txt


SECRET_KEY = "django-insecure-z9c%+(7k)cbi+p))9k=)t=x!*4k7-(_dlw4o0o0v-gb9ar^5+z"
ALGORITHM = "HS256"


async def decode_jwt_token(token: str) -> UserJWT:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return UserJWT(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado"
        )
