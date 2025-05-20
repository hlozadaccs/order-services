from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.models.order import Order as OrderModel
from app.domain.models.order import OrderItem as OrderItemModel
from app.schemas.order import OrderCreate, PartialUpdate


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.orderitems))
            .order_by(OrderModel.created_at.desc())
        )
        return result.scalars().all()

    async def get_order_by_id(self, order_id: int):
        result = await self.session.execute(
            select(OrderModel)
            .options(selectinload(OrderModel.orderitems))
            .where(OrderModel.id == order_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data_from_api: OrderCreate):
        order = OrderModel(
            user_id=data_from_api.user_id,
            status=data_from_api.status,
            order_type=data_from_api.order_type,
        )

        self.session.add(order)
        await self.session.flush()

        for item in data_from_api.orderitems:
            order_item = OrderItemModel(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                notes=item.notes,
            )
            self.session.add(order_item)

        await self.session.commit()
        await self.session.refresh(order)

        order_from_db = await self.get_order_by_id(order_id=order.id)  # type: ignore
        return order_from_db

    async def update(self, order_id: int, data_from_api: OrderCreate):
        order = await self.get_order_by_id(order_id=order_id)
        if not order:
            return None

        order.user_id = data_from_api.user_id
        order.status = data_from_api.status
        order.order_type = data_from_api.order_type
        order.updated_at = datetime.utcnow()

        await self.session.execute(
            OrderItemModel.__table__.delete().where(OrderItemModel.order_id == order.id)
        )

        for item in data_from_api.orderitems:
            order_item = OrderItemModel(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                notes=item.notes,
            )
            self.session.add(order_item)

        await self.session.commit()
        await self.session.refresh(order)

        order_from_db = await self.get_order_by_id(order_id=order.id)  # type: ignore
        return order_from_db

    async def partial_update(self, order_id: int, data_from_api: PartialUpdate):
        order = await self.get_order_by_id(order_id=order_id)
        if not order:
            return None

        for field, value in data_from_api.items():
            if hasattr(order, field):
                db_value = getattr(order, field)
                if value is not None:
                    new_value = value
                else:
                    new_value = db_value
                setattr(order, field, new_value)

        await self.session.commit()
        await self.session.refresh(order)

        return order

    async def delete(self, order_id: int) -> bool:
        order = await self.get_order_by_id(order_id=order_id)
        if not order:
            return False

        await self.session.delete(order)
        await self.session.commit()

        return True
