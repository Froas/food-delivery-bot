from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from typing import Literal

RestaurantType = Literal['RAMEN', 'CURRY', 'PIZZA', 'SUSHI']

NodeType = Literal['NODE', 'HOUSE', 'RESTAURANT', 'BOT_STATION']

class NodeBase(BaseModel):
    x: int = Field(..., ge=0, le=8)
    y: int = Field(..., ge=0, le=8)
    node_type: str = NodeType
    is_delivery_point: bool = False
    is_restaurant: bool = False
    is_bot_station: bool = False
    restaurant_type: RestaurantType  | None = None
    name: Optional[str] = Field(None, max_length=100)

class NodeCreate(NodeBase):
    pass

class NodeResponse(NodeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True