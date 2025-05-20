import enum
from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import relationship

from app.domain.models.base import Base


class OrderType(str, enum.Enum):
    DINE_IN = "DINE_IN"
    TAKEAWAY = "TAKEAWAY"
    DELIVERY = "DELIVERY"


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class Order(Base):
    __tablename__ = "services_order"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    status = sqlalchemy.Column(
        sqlalchemy.String,
        default=OrderStatus.PENDING.value,
    )
    order_type = sqlalchemy.Column(sqlalchemy.String, default=OrderType.DINE_IN.value)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    orderitems = relationship("OrderItem", back_populates="order", cascade="all")


class OrderItem(Base):
    __tablename__ = "services_orderitem"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("services_order.id")
    )
    quantity = sqlalchemy.Column(sqlalchemy.Integer)
    notes = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer)

    order = relationship("Order", back_populates="orderitems")
