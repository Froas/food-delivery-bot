from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.bot import Bot
from models.order import Order
from services.route_algorithm import RouteOptimizer

router = APIRouter()

@router.get("/routes/optimize")
async def optimize_all_routes(db: Session = Depends(get_db)):
    route_optimizer = RouteOptimizer(db)
    results = {}
    
    bots = db.query(Bot).filter(Bot.current_orders > 0).all()
    
    for bot in bots:
        orders = db.query(Order).filter(
            Order.bot_id == bot.id,
            Order.status.in_(['ASSIGNED', 'PICKED_UP'])
        ).all()
        
        if orders:
            route = route_optimizer.optimize_delivery_route(bot, orders)
            results[bot.id] = route
    
    return results

@router.get("/routes/distance")
async def calculate_distance(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    db: Session = Depends(get_db)
):
    route_optimizer = RouteOptimizer(db)
    path = route_optimizer.dijkstra((start_x, start_y), (end_x, end_y))
    
    return {
        "distance": len(path) - 1 if path else -1,
        "path": path,
        "time_seconds": len(path) - 1 if path else -1
    }