# app/api/v1/map_api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.node import Node
from models.bot import Bot
from models.order import Order
from schemas.node import NodeResponse
from models.blocked_path import BlockedPath

router = APIRouter()

# Get a map grid
@router.get("/map/grid")
async def get_map_grid(db: Session = Depends(get_db)):

    # Get all nodes
    nodes = db.query(Node).all()
    
    # Get all bots with current positions
    bots = db.query(Bot).all()
    
    # Get active orders
    active_orders = db.query(Order).filter(
        Order.status.in_(['PENDING', 'ASSIGNED', 'PICKED_UP'])
    ).all()
    
    # Create 9x9 grid structure
    grid = {}
    for y in range(9):
        for x in range(9):
            grid[f"{x},{y}"] = {
                "x": x,
                "y": y,
                "node_type": "NODE",
                "is_delivery_point": False,
                "is_restaurant": False,
                "is_bot_station": False,
                "restaurant_type": None,
                "name": f"Node_{x}_{y}",
                "bots": [],
                "active_orders": []
            }
    
    # Fill in node information
    for node in nodes:
        key = f"{node.x},{node.y}"
        if key in grid:
            grid[key].update({
                "node_type": node.node_type,
                "is_delivery_point": node.is_delivery_point,
                "is_restaurant": node.is_restaurant,
                "is_bot_station": node.is_bot_station,
                "restaurant_type": node.restaurant_type,
                "name": node.name or f"Node_{node.x}_{node.y}"
            })
    
    # Add bot positions
    for bot in bots:
        key = f"{bot.current_x},{bot.current_y}"
        if key in grid:
            grid[key]["bots"].append({
                "id": bot.id,
                "name": bot.name,
                "status": bot.status,
                "current_orders": bot.current_orders,
                "battery_level": bot.battery_level
            })
    
    # Add order information (pickup and delivery locations)
    for order in active_orders:
        pickup_key = f"{order.pickup_x},{order.pickup_y}"
        delivery_key = f"{order.delivery_x},{order.delivery_y}"
        
        order_info = {
            "id": order.id,
            "customer_name": order.customer_name,
            "restaurant_type": order.restaurant_type,
            "status": order.status,
            "bot_id": order.bot_id
        }
        
        if pickup_key in grid:
            grid[pickup_key]["active_orders"].append({
                **order_info,
                "location_type": "pickup"
            })
        
        if delivery_key in grid:
            grid[delivery_key]["active_orders"].append({
                **order_info,
                "location_type": "delivery"
            })
    
    return {
        "grid": grid,
        "grid_size": 9,
        "total_nodes": len(nodes),
        "total_bots": len(bots),
        "active_orders": len(active_orders)
    }

# Get all Nodes
@router.get("/map/nodes", response_model=List[NodeResponse])
async def get_all_nodes(db: Session = Depends(get_db)):

    return db.query(Node).all()

# Get all Restaurants
@router.get("/map/restaurants")
async def get_restaurants(db: Session = Depends(get_db)):

    restaurants = db.query(Node).filter(Node.is_restaurant == True).all()
    
    return [
        {
            "id": r.id,
            "x": r.x,
            "y": r.y,
            "restaurant_type": r.restaurant_type,
            "name": r.name
        }
        for r in restaurants
    ]

# Get all Delivery point
@router.get("/map/delivery-points")
async def get_delivery_points(db: Session = Depends(get_db)):

    houses = db.query(Node).filter(Node.is_delivery_point == True).all()
    
    return [
        {
            "id": h.id,
            "x": h.x,
            "y": h.y,
            "name": h.name
        }
        for h in houses
    ]

# Get map statistics
@router.get("/map/stats")
async def get_map_stats(db: Session = Depends(get_db)):

    total_nodes = db.query(Node).count()
    restaurants = db.query(Node).filter(Node.is_restaurant == True).count()
    houses = db.query(Node).filter(Node.is_delivery_point == True).count()
    bot_stations = db.query(Node).filter(Node.is_bot_station == True).count()
    
    total_bots = db.query(Bot).count()
    idle_bots = db.query(Bot).filter(Bot.status == 'IDLE').count()
    busy_bots = db.query(Bot).filter(Bot.status == 'BUSY').count()
    
    pending_orders = db.query(Order).filter(Order.status == 'PENDING').count()
    active_orders = db.query(Order).filter(Order.status.in_(['ASSIGNED', 'PICKED_UP'])).count()
    delivered_orders = db.query(Order).filter(Order.status == 'DELIVERED').count()
    
    return {
        "map": {
            "total_nodes": total_nodes,
            "restaurants": restaurants,
            "houses": houses,
            "bot_stations": bot_stations
        },
        "bots": {
            "total": total_bots,
            "idle": idle_bots,
            "busy": busy_bots
        },
        "orders": {
            "pending": pending_orders,
            "active": active_orders,
            "delivered": delivered_orders
        }
    }


# Get blocked path
@router.get("/map/blocked-paths")
async def get_blocked_paths(db: Session = Depends(get_db)):

    blocked_paths = db.query(BlockedPath).all()
    
    visualization_data = []
    for blocked in blocked_paths:
        from_x = (blocked.from_node_id - 1) % 9
        from_y = (blocked.from_node_id - 1) // 9
        to_x = (blocked.to_node_id - 1) % 9
        to_y = (blocked.to_node_id - 1) // 9
        
        visualization_data.append({
            "from_x": from_x, "from_y": from_y,
            "to_x": to_x, "to_y": to_y,
            "direction": _get_direction(from_x, from_y, to_x, to_y)
        })
    
    return {
        "total_blocked": len(blocked_paths),
        "blocked_segments": visualization_data
    }

# Get direction for blocked path
def _get_direction(from_x: int, from_y: int, to_x: int, to_y: int) -> str:
    
    dx = to_x - from_x
    dy = to_y - from_y
    
    if dx == 1 and dy == 0:
        return "right"
    elif dx == -1 and dy == 0:
        return "left"
    elif dx == 0 and dy == 1:
        return "down"
    elif dx == 0 and dy == -1:
        return "up"
    else:
        return "diagonal"