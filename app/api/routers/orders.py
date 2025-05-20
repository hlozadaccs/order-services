from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse, PartialUpdate
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


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate, session: AsyncSession = Depends(get_session)
):
    usecase = get_usecase(session=session)
    return await usecase.create_order(order=order)


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


@router.put("/{order_id}")
async def update_order(
    order_id: int,
    data_from_request: OrderCreate,
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    order_updated = await usecase.update_order(
        order_id=order_id, order=data_from_request
    )

    if not order_updated:
        raise HTTPException(status_code=404, detail="Order does not exist")

    return order_updated


@router.patch("/{order_id}")
async def partial_update_order(
    order_id: int,
    data_from_request: PartialUpdate,
    session: AsyncSession = Depends(get_session),
):
    usecase = get_usecase(session=session)
    order_updated = await usecase.partial_update_order(
        order_id=order_id, order=data_from_request
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
    usecase = get_usecase(session=session)
    deleted = await usecase.delete_order(order_id=order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")

    return
