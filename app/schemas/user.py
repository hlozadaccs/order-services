from typing import Optional

from pydantic import BaseModel


class UserJWT(BaseModel):
    user_id: int
    token_type: str
    exp: int
    iat: int
    jti: str
    role: Optional[str] = None
