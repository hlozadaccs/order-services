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
