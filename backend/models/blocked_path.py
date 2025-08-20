from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class BlockedPath(Base):
    __tablename__ = "blocked_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    from_node_id = Column(Integer, ForeignKey('nodes.id'), nullable=False)
    to_node_id = Column(Integer, ForeignKey('nodes.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    from_node = relationship("Node", foreign_keys=[from_node_id])
    to_node = relationship("Node", foreign_keys=[to_node_id])

