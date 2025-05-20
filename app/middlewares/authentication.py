# app/middleware.py

import asyncio

import httpx
from async_lru import alru_cache
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from app.infrastructure.security.jwt import decode_jwt_token

DJANGO_BASE_URL = "http://127.0.0.1:8000"
TOKEN_VERIFY = f"{DJANGO_BASE_URL}/api/v1/token/verify/"
USERS_URL = f"{DJANGO_BASE_URL}/api/v1/users"


@alru_cache(maxsize=1024)
async def fetch_user_from_django(user_id: int, token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{USERS_URL}/{user_id}/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5.0,
        )
        response.raise_for_status()
        return response.json()


async def validate_token(token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_VERIFY, json={"token": token})
        if response.status_code != 200:
            response.raise_for_status()
            return response.json()


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Excepciones
        if request.url.path in ["/docs", "/openapi.json", "/health"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Authorization header missing or malformed"},
                status_code=HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]

        try:
            await validate_token(token=token)
        except httpx.HTTPStatusError:
            return JSONResponse(
                {"detail": "Invalid token"},
                status_code=HTTP_401_UNAUTHORIZED,
            )
        except httpx.RequestError:
            return JSONResponse(
                {"detail": "Auth server unreachable"},
                status_code=HTTP_401_UNAUTHORIZED,
            )

        try:
            user = await decode_jwt_token(token=token)
            user_info = await fetch_user_from_django(user_id=user.user_id, token=token)
            user.role = user_info["display_role"]
            request.state.user = user
        except httpx.HTTPStatusError:
            return JSONResponse(
                {"detail": "Invalid token"},
                status_code=HTTP_401_UNAUTHORIZED,
            )
        except httpx.RequestError:
            return JSONResponse(
                {"detail": "Auth server unreachable"},
                status_code=HTTP_401_UNAUTHORIZED,
            )

        return await call_next(request)
