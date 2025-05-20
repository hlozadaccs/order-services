from fastapi import FastAPI

from app.api.routers import orders as orders_router
from app.middlewares.authentication import JWTAuthMiddleware


def create_application() -> FastAPI:
    app = FastAPI(
        title="Order Service API",
        description="Microervicio para la gestión de órdenes en una "
        "arquitectura desacoplada.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    return app


app = create_application()
app.include_router(orders_router.router, prefix="/api/v1/orders")  # URLS.py

app.add_middleware(JWTAuthMiddleware)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"message": "healthy"}


@app.get("/protected")
def protected():
    return {"message": "JWT válido, acceso concedido"}
