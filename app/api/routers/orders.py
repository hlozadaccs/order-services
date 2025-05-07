from fastapi import APIRouter

from app.schemas.order import OrderCreate

router = APIRouter()


@router.post("/")  # <- Aquí el método POST
async def create_order(data: OrderCreate):
    print(data)
    return {}  # Retorna un diccionario


# @router.get("/")  # <- Aquí el método GET
# async def list_all_orders():
#     return []  # Retorna un listado


# @router.get("/{order_id}")  # <- Aquí el método GET
# async def get_order_by_id(order_id: int):
#     print(order_id)
#     return {}  # Retorna un diccionario
