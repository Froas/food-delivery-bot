from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


BotStatus = Literal['IDLE', 'BUSY', 'MAINTENANCE']


class BotBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    current_x: int = Field(default=0, ge=0, le=8)
    current_y: int = Field(default=0, ge=0, le=8)
    max_capacity: int = Field(default=3, ge=1, le=5)

class BotCreate(BotBase):
    pass

class BotUpdate(BaseModel):
    current_x: Optional[int] = Field(None, ge=0, le=8)
    current_y: Optional[int] = Field(None, ge=0, le=8)
    status: Optional[str] = BotStatus
    current_orders: Optional[int] = Field(None, ge=0, le=5)
    battery_level: Optional[int] = Field(None, ge=0, le=100)

class BotResponse(BotBase):
    id: int
    status: str
    current_orders: int
    battery_level: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True