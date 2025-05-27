from fastapi.exceptions import ValidationException

from app.infrastructure.producer import KafkaProducerSingleton
from app.infrastructure.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, PartialUpdate
from app.schemas.user import UserJWT


class OrderUseCase:
    def __init__(self, repo: OrderRepository, kafka_producer: KafkaProducerSingleton):
        self.repo = repo
        self.kafka = kafka_producer

    async def list_orders(self, user: UserJWT):
        is_admin = user.role == "ADMIN"
        if is_admin:
            return await self.repo.get_all()

        return await self.repo.filter_orders_by_user_id(user_id=user.user_id)

    async def get_order(self, order_id: int, user: UserJWT):
        is_admin = user.role == "ADMIN"
        if is_admin:
            return await self.repo.get_order_by_id(order_id=order_id)

        return await self.repo.get_order_by_user_and_order_id(
            user_id=user.user_id, order_id=order_id
        )

    async def create_order(self, order: OrderCreate, user: UserJWT):
        is_admin = user.role == "ADMIN"
        if not is_admin:
            order.user_id = user.user_id

        new_order = await self.repo.create(data_from_api=order)

        order_dict = {
            "order_id": new_order.id,
            "order_type": new_order.order_type,
            "status": new_order.status,
            "created_at": new_order.created_at.isoformat(),
            "order_items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "notes": item.notes,
                }
                for item in new_order.orderitems
            ],
        }

        await self.kafka.send("kitchen-new-orders", order_dict)

        return new_order

    async def update_order(self, order_id: int, order: OrderCreate, user: UserJWT):
        is_admin = user.role == "ADMIN"
        order_obj = await self.repo.get_order_by_user_and_order_id(
            user_id=user.user_id, order_id=order_id
        )
        if is_admin or order_obj:
            return await self.repo.update(order_id=order_id, data_from_api=order)

        raise ValidationException("Unable to update")

    async def partial_update_order(
        self, order_id: int, order: PartialUpdate, user: UserJWT
    ):
        is_admin = user.role == "ADMIN"
        order_obj = await self.repo.get_order_by_user_and_order_id(
            user_id=user.user_id, order_id=order_id
        )
        if is_admin or order_obj:
            return await self.repo.partial_update(
                order_id=order_id, data_from_api=order
            )

        raise ValidationException("Unable to update")

    async def delete_order(self, order_id: int, user: UserJWT):
        is_admin = user.role == "ADMIN"
        was_deleted = await self.repo.delete(
            order_id=order_id, user_id=user.user_id, is_admin=is_admin
        )
        if was_deleted:
            return was_deleted

        raise ValidationException("Imposible eliminar")
