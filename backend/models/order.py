from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_type = Column(String(50), nullable=False)  
    restaurant_name = Column(String(100), nullable=False, default="")  

    customer_name = Column(String(100), nullable=False, default="Guest")
    customer_phone = Column(String(20), nullable=True)


    pickup_x = Column(Integer, nullable=False)
    pickup_y = Column(Integer, nullable=False)
    delivery_x = Column(Integer, nullable=False)
    delivery_y = Column(Integer, nullable=False)

    status = Column(String(50), nullable=False, default="PENDING")

    restaurant_id = Column(Integer, ForeignKey("nodes.id"), nullable=True)  
    bot_id        = Column(Integer, ForeignKey("bots.id"),  nullable=True)


    estimated_distance = Column(Integer, nullable=True)
    estimated_time     = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())

    bot  = relationship("models.bot.Bot", backref="orders")
    node = relationship("models.node.Node", backref="orders")
