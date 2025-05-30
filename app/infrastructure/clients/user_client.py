import httpx
from async_lru import alru_cache

from app.config import settings

TOKEN_VERIFY = f"{settings.MONOLITHIC_PROJECT_URL}/api/v1/token/verify/"
USERS_URL = f"{settings.MONOLITHIC_PROJECT_URL}/api/v1/users"


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
