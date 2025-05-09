from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.models.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(
            select(Order).order_by(Order.created_at.desc())
        )
        return result.scalars().all()
