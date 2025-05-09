from app.infrastructure.repositories.order_repository import OrderRepository


class OrderUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def list_orders(self):
        return await self.repo.get_all()

    async def get_order(self, order_id: int):
        return await self.repo.get_order_by_id(order_id=order_id)
