from app.infrastructure.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, PartialUpdate


class OrderUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def list_orders(self):
        return await self.repo.get_all()

    async def get_order(self, order_id: int):
        return await self.repo.get_order_by_id(order_id=order_id)

    async def create_order(self, order: OrderCreate):
        return await self.repo.create(data_from_api=order)

    async def update_order(self, order_id: int, order: OrderCreate):
        return await self.repo.update(order_id=order_id, data_from_api=order)

    async def partial_update_order(self, order_id: int, order: PartialUpdate):
        return await self.repo.partial_update(order_id=order_id, data_from_api=order)

    async def delete_order(self, order_id: int):
        return await self.repo.delete(order_id=order_id)
