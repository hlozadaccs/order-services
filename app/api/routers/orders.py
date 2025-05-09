from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse
from app.use_cases.order_usecase import OrderUseCase

router = APIRouter()


def get_usecase(session: AsyncSession) -> OrderUseCase:
    return OrderUseCase(OrderRepository(session))


@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    return await usecase.list_orders()


@router.post("/")  # <- Aquí el método POST
async def create_order(data: OrderCreate):
    print(data)
    return {}  # Retorna un diccionario


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    order = await usecase.get_order(order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist")

    return order
