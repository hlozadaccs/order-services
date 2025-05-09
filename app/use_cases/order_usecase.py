from app.infrastructure.repositories.order_repository import OrderRepository


class OrderUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def list_orders(self):
        return await self.repo.get_all()
