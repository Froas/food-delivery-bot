from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from core.database import Base

class Bot(Base):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    current_x = Column(Integer, nullable=False, default=0)
    current_y = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False, default="IDLE")
    max_capacity = Column(Integer, nullable=False, default=3)   
    current_orders = Column(Integer, nullable=False, default=0)
    battery_level = Column(Integer, nullable=False, default=100)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
