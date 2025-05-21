import httpx
from async_lru import alru_cache

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
