from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.models.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(
            select(Order)
            .options(selectinload(Order.orderitems))
            .order_by(Order.created_at.desc())
        )
        return result.scalars().all()

    async def get_order_by_id(self, order_id: int):
        result = await self.session.execute(
            select(Order)
            .options(selectinload(Order.orderitems))
            .where(Order.id == order_id)
        )
        return result.scalar_one_or_none()
