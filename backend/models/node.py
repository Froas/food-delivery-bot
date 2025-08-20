from sqlalchemy import Column, Integer, String, Boolean, Enum, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from core.database import Base
import enum

class NodeType(str, enum.Enum):
    NODE = "NODE"
    HOUSE = "HOUSE"
    RESTAURANT = "RESTAURANT"
    BOT_STATION = "BOT_STATION"

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    name = Column(String(100), nullable=True)

    node_type = Column(Enum(NodeType), nullable=False, default=NodeType.NODE)

    is_delivery_point = Column(Boolean, nullable=False, default=False)
    is_restaurant = Column(Boolean, nullable=False, default=False)
    is_bot_station = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    restaurant_type = Column(String, nullable=True)

    __table_args__ = (UniqueConstraint("x", "y", name="uq_nodes_x_y"),)
