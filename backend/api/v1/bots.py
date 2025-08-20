# app/api/v1/bots.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models.bot import Bot
from models.order import Order
from schemas.bot import BotCreate, BotUpdate, BotResponse
from services.route_algorithm import RouteOptimizer

router = APIRouter()

@router.post("/bots/", response_model=BotResponse)
async def create_bot(bot: BotCreate, db: Session = Depends(get_db)):
    """Create a new delivery bot"""
    db_bot = Bot(**bot.model_dump())
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

@router.get("/bots/", response_model=List[BotResponse])
async def get_bots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all bots"""
    bots = db.query(Bot).offset(skip).limit(limit).all()
    return bots

@router.get("/bots/{bot_id}", response_model=BotResponse)
async def get_bot(bot_id: int, db: Session = Depends(get_db)):
    """Get specific bot by ID"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot

@router.put("/bots/{bot_id}", response_model=BotResponse)
async def update_bot(
    bot_id: int,
    bot_update: BotUpdate,
    db: Session = Depends(get_db)
):
    """Update bot status, position, or other properties"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    for field, value in bot_update.model_dump(exclude_unset=True).items():
        if hasattr(bot, field):
            setattr(bot, field, value)
    
    db.commit()
    db.refresh(bot)
    
    return bot

@router.get("/bots/{bot_id}/route")
async def get_bot_route(bot_id: int, db: Session = Depends(get_db)):
    """Get optimized route for a specific bot"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Get assigned orders
    orders = db.query(Order).filter(
        Order.bot_id == bot_id,
        Order.status.in_(['ASSIGNED', 'PICKED_UP'])
    ).all()
    
    if not orders:
        return {"route_points": [], "total_distance": 0, "estimated_time": 0}
    
    # Calculate optimized route
    route_optimizer = RouteOptimizer(db)
    route = route_optimizer.optimize_delivery_route(bot, orders)
    
    return route

@router.post("/bots/{bot_id}/move")
async def move_bot(
    bot_id: int,
    x: int,
    y: int,
    db: Session = Depends(get_db)
):
    """Move bot to new position"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Validate position
    if not (0 <= x < 9 and 0 <= y < 9):
        raise HTTPException(status_code=400, detail="Invalid position")
    
    old_x, old_y = bot.current_x, bot.current_y
    bot.current_x = x
    bot.current_y = y
    db.commit()
    
    # Check if bot reached pickup/delivery location
    await check_bot_location_updates(bot, db)
    
    return {
        "message": f"Bot moved from ({old_x}, {old_y}) to ({x}, {y})",
        "new_position": {"x": x, "y": y},
        "bot_id": bot_id
    }

@router.get("/bots/{bot_id}/orders")
async def get_bot_orders(bot_id: int, db: Session = Depends(get_db)):
    """Get all orders assigned to a specific bot"""
    bot = db.query(Bot).filter(Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    orders = db.query(Order).filter(Order.bot_id == bot_id).all()
    return orders

async def check_bot_location_updates(bot: Bot, db: Session):
    """Check if bot reached any pickup or delivery locations"""
    orders = db.query(Order).filter(
        Order.bot_id == bot.id,
        Order.status.in_(['ASSIGNED', 'PICKED_UP'])
    ).all()
    
    for order in orders:
        # Check pickup
        if (order.status == 'ASSIGNED' and 
            bot.current_x == order.pickup_x and 
            bot.current_y == order.pickup_y):
            order.status = 'PICKED_UP'
            print(f"Bot {bot.id} picked up order {order.id}")
        
        # Check delivery
        elif (order.status == 'PICKED_UP' and 
            bot.current_x == order.delivery_x and 
            bot.current_y == order.delivery_y):
            order.status = 'DELIVERED'
            bot.current_orders -= 1
            
            # Update bot status if no more orders
            if bot.current_orders == 0:
                bot.status = 'IDLE'
            elif bot.current_orders < bot.max_capacity:
                bot.status = 'IDLE'
            
            print(f"Bot {bot.id} delivered order {order.id}")
    
    db.commit()