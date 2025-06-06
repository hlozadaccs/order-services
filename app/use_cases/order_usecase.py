from fastapi.exceptions import ValidationException

from app.infrastructure.clients.menu_client import MenuClientSingleton
from app.infrastructure.kafka.producer import KafkaProducerSingleton
from app.infrastructure.logging.logger import setup_logger
from app.infrastructure.prometheus.metrics import (
    order_creation_duration_seconds,
    orders_created_counter,
)
from app.infrastructure.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, PartialUpdate
from app.schemas.user import UserJWT

logger = setup_logger(__name__)


class OrderUseCase:
    def __init__(
        self,
        repo: OrderRepository,
        kafka_producer: KafkaProducerSingleton,
        menu_client: MenuClientSingleton,
    ):
        self.repo = repo
        self.kafka = kafka_producer
        self.menu_client = menu_client

    async def list_orders(self, user: UserJWT):
        is_admin = user.role == "ADMIN"
        if is_admin:
            orders = await self.repo.get_all()
        else:
            orders = await self.repo.filter_orders_by_user_id(user_id=user.user_id)

        for order in orders:
            enriched_items = []
            for item in order.orderitems:
                info = self.menu_client.get_menu_item(item.product_id)  # <- Damelo

                item.name = info.name
                item.category = info.category
                item.price = info.price
                item.available = info.available
                item.description = info.description
                enriched_items.append(item)  # <-

            order.orderitems = enriched_items

        return orders

    async def get_order(self, order_id: int, user: UserJWT):
        is_admin = user.role == "ADMIN"
        if is_admin:
            return await self.repo.get_order_by_id(order_id=order_id)

        return await self.repo.get_order_by_user_and_order_id(
            user_id=user.user_id, order_id=order_id
        )

    async def create_order(self, order: OrderCreate, user: UserJWT):
        order_type = order.order_type.value
        with order_creation_duration_seconds.time():
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
            logger.info("Creating new order", extra={"user_id": user.user_id})
            orders_created_counter.labels(order_type=order_type).inc()

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
