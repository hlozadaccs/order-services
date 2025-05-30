import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routers import orders as orders_router
from app.config import settings
from app.infrastructure.kafka.producer import KafkaProducerSingleton
from app.infrastructure.logging.logger import setup_logger
from app.middlewares.authentication import JWTAuthMiddleware

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", settings.KAFKA_URL)


logger = setup_logger("app")
kafka_producer = KafkaProducerSingleton(bootstrap_servers)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    await kafka_producer.start()

    yield

    logger.info("Shutting down application...")
    await kafka_producer.stop()


def create_application() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
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

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"message": f"POD: {settings.POD_NAME} healthy"}


@app.get("/protected")
def protected():
    return {"message": "JWT válido, acceso concedido"}
