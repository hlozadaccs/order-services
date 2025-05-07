from enum import Enum

from pydantic import BaseModel, Field


class OrderType(str, Enum):
    DINE_IN = "DINE_IN"
    TAKEAWAY = "TAKEAWAY"
    DELIVERY = "DELIVERY"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class OrderItem(BaseModel):
    product_id: int = Field(..., description="ID del producto")
    quantity: int = Field(..., description="Cantidad")
    notes: str | None = Field(None, description="Notas extras")


# Type Hinting

# notes: str | None = None
# notes: str = "Hola Mundo"
# notes: str = Field(..., description="Hola Mundo")


class OrderCreate(BaseModel):
    user_id: int = Field(..., description="ID del usuario")
    status: OrderStatus = Field(..., description="Estado de la orden")
    order_type: OrderType = Field(
        ..., description="Tipo de orden (DINE_IN, TIKEAWAY, DELIVERY)"
    )
    notes: str | None = Field(None, description="Notas extras")
    items: list[OrderItem] = []


# {
#   "user_id": 0,
#   "status": "PENDING",
#   "order_type": "DINE_IN",
#   "notes": "string",  <-------
#   "items": [
#    {
#      "product_id": 123,
#      "quantity": 1,
#      "notes": "test"
#    },
#    {
#      "product_id": 1234,
#      "quantity": 2,
#      "notes": "test2"
#    }
#  ]
# }
