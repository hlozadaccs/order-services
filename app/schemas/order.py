from datetime import datetime

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from app.domain.models.order import OrderStatus, OrderType


class OrderItem(BaseModel):
    product_id: int = Field(..., description="ID del producto")
    quantity: int = Field(..., description="Cantidad", gt=0)
    notes: str | None = Field(None, description="Notas extras")


class DatesFieldsModel(BaseModel):
    created_at: datetime
    updated_at: datetime


class BaseOrder(BaseModel):
    user_id: int
    status: OrderStatus
    order_type: OrderType

    orderitems: list[OrderItem] = []


class OrderCreate(BaseOrder):
    model_config = {"from_attributes": True}


class PartialUpdate(BaseModel):
    user_id: int | SkipJsonSchema[None]
    status: OrderStatus | SkipJsonSchema[None]
    order_type: OrderType | SkipJsonSchema[None]

    orderitems: list[OrderItem] | SkipJsonSchema[None] = None


class OrderResponse(DatesFieldsModel, BaseOrder):
    id: int


class OrderItemEnriched(OrderItem):
    name: str
    price: float
    available: bool
    description: str


class OrderResponseEnriched(OrderResponse):
    orderitems: list[OrderItemEnriched] = []


def to_response(order_orm) -> OrderResponseEnriched:
    return OrderResponseEnriched(
        id=order_orm.id,
        user_id=order_orm.user_id,
        status=order_orm.status,
        order_type=order_orm.order_type,
        created_at=order_orm.created_at,
        updated_at=order_orm.updated_at,
        orderitems=[
            OrderItemEnriched(
                product_id=item.product_id,
                name=item.name,
                price=item.price,
                available=item.available,
                quantity=item.quantity,
                notes=item.notes,
                description=item.description,
            )
            for item in order_orm.orderitems
        ],
    )
