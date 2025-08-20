from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from typing import Literal


RestaurantType = Literal['RAMEN', 'CURRY', 'PIZZA', 'SUSHI']
Status = Literal['PENDING', 'ASSIGNED', 'PICKED_UP', 'DELIVERED', 'CANCELLED']


class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    customer_phone: Optional[str] = Field(None, max_length=20)
    restaurant_type: str = RestaurantType
    pickup_x: int = Field(..., ge=0, le=8)
    pickup_y: int = Field(..., ge=0, le=8)
    delivery_x: int = Field(..., ge=0, le=8)
    delivery_y: int = Field(..., ge=0, le=8)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[str] = Status
    bot_id: Optional[int] = None
    estimated_distance: Optional[int] = None
    estimated_time: Optional[int] = None

class OrderResponse(OrderBase):
    id: int
    status: str
    bot_id: Optional[int] = None
    estimated_distance: Optional[int] = None
    estimated_time: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

