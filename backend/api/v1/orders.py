from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.order import Order
from models.node import Node
from schemas.order import OrderCreate, OrderUpdate, OrderResponse
from services.bot_manager import BotManager
from core.database import SessionLocal
from models.bot import Bot

router = APIRouter()

@router.post("/orders/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):  
    pickup_node = db.query(Node).filter(
        Node.x == order.pickup_x,
        Node.y == order.pickup_y,
        Node.is_restaurant == True,
        Node.restaurant_type == order.restaurant_type.upper()
    ).first()
    
    if not pickup_node:
        raise HTTPException(
            status_code=400,
            detail=f"No {order.restaurant_type} restaurant found at position ({order.pickup_x}, {order.pickup_y})"
        )
    
    delivery_node = db.query(Node).filter(
        Node.x == order.delivery_x,
        Node.y == order.delivery_y,
        Node.is_delivery_point == True
    ).first()
    
    if not delivery_node:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid delivery location at position ({order.delivery_x}, {order.delivery_y})"
        )
    
    import datetime
    time_threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=30)
    recent_orders = db.query(Order).filter(
        Order.pickup_x == order.pickup_x,
        Order.pickup_y == order.pickup_y,
        Order.status.in_(['PENDING', 'ASSIGNED', 'PICKED_UP']),
        Order.created_at >= time_threshold
    ).count()
    
    if recent_orders >= 3:
        raise HTTPException(
            status_code=429,
            detail="Restaurant is at capacity. Please try again later."
        )
    
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    background_tasks.add_task(assign_order_to_bot, db_order.id)
    
    return db_order

async def assign_order_to_bot(order_id: int):

    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order and order.status == 'PENDING':
            bot_manager = BotManager(db)
            assigned_bot = bot_manager.assign_order_to_best_bot(order)
            
            if assigned_bot:
                print(f"Order {order_id} assigned to bot {assigned_bot.id}")
                
            else:
                print(f"No available bot for order {order_id}")
    finally:
        db.close()

@router.get("/orders/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status.upper())
    
    orders = query.offset(skip).limit(limit).all()
    return orders

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get specific order by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for field, value in order_update.model_dump(exclude_unset=True).items():
        if hasattr(order, field):
            setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    
    return order

@router.delete("/orders/{order_id}")
async def cancel_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status in ['DELIVERED', 'CANCELLED']:
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel order that is already delivered or cancelled"
        )
    
    order.status = 'CANCELLED'
    
    if order.bot_id:
        bot = db.query(Bot).filter(Bot.id == order.bot_id).first()
        if bot:
            bot.current_orders -= 1
            if bot.current_orders < bot.max_capacity and bot.status == 'BUSY':
                bot.status = 'IDLE'
    
    db.commit()
    
    return {"message": "Order cancelled successfully"}
