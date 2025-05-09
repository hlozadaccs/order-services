from enum import Enum

from pydantic import BaseModel, Field

from app.domain.models.order import OrderStatus, OrderType


class OrderItem(BaseModel):
    product_id: int = Field(..., description="ID del producto")
    quantity: int = Field(..., description="Cantidad")
    notes: str | None = Field(None, description="Notas extras")


class OrderCreate(BaseModel):
    user_id: int = Field(..., description="ID del usuario")
    status: OrderStatus = Field(..., description="Estado de la orden")
    order_type: OrderType = Field(
        ..., description="Tipo de orden (DINE_IN, TIKEAWAY, DELIVERY)"
    )
    notes: str | None = Field(None, description="Notas extras")
    items: list[OrderItem] = []
