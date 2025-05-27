from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.exceptions import ValidationException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_session
from app.infrastructure.producer import KafkaProducerSingleton
from app.infrastructure.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse, PartialUpdate
from app.use_cases.order_usecase import OrderUseCase

router = APIRouter()


def get_usecase(session: AsyncSession) -> OrderUseCase:
    return OrderUseCase(
        repo=OrderRepository(session),
        kafka_producer=KafkaProducerSingleton(),
    )


@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    return await usecase.list_orders(user=request.state.user)


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate, request: Request, session: AsyncSession = Depends(get_session)
):
    usecase = get_usecase(session=session)
    return await usecase.create_order(order=order, user=request.state.user)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    order = await usecase.get_order(order_id=order_id, user=request.state.user)
    if not order:
        raise HTTPException(status_code=404, detail="Order does not exist")

    return order


@router.put("/{order_id}")
async def update_order(
    order_id: int,
    request: Request,
    data_from_request: OrderCreate,
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    order_updated = await usecase.update_order(
        order_id=order_id, order=data_from_request, user=request.state.user
    )

    if not order_updated:
        raise HTTPException(status_code=404, detail="Order does not exist")

    return order_updated


@router.patch("/{order_id}")
async def partial_update_order(
    order_id: int,
    request: Request,
    data_from_request: PartialUpdate,
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    order_updated = await usecase.partial_update_order(
        order_id=order_id, order=data_from_request, user=request.state.user
    )

    if not order_updated:
        raise HTTPException(status_code=404, detail="Order does not exist")

    return order_updated


@router.delete("/{order_id}", status_code=204)
async def delete_order(
    order_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    # request.state.user
    usecase = get_usecase(session=session)
    try:
        deleted = await usecase.delete_order(order_id=order_id, user=request.state.user)
    except ValidationException as e:
        print(f"error: {e}")
        raise HTTPException(status_code=403, detail="Order not found")

    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")

    return
