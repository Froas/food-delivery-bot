from typing import List, Optional
from sqlalchemy.orm import Session
from models.bot import Bot
from models.order import Order
from services.route_algorithm import RouteOptimizer

class BotManager:
    def __init__(self, db: Session):
        self.db = db
        self.route_optimizer = RouteOptimizer(db)
    
    def get_available_bots(self) -> List[Bot]:

        return self.db.query(Bot).filter(
            Bot.status.in_(['IDLE', 'BUSY']),
            Bot.current_orders < Bot.max_capacity
        ).all()
    
    def assign_order_to_best_bot(self, order: Order) -> Optional[Bot]:

        available_bots = self.get_available_bots()
        
        if not available_bots:
            print(f"No available bots for order {order.id}")
            return None
        
        best_bot = None
        min_cost = float('inf')
        
        for bot in available_bots:

            pickup_pos = (order.pickup_x, order.pickup_y)
            bot_pos = (bot.current_x, bot.current_y)
            
            path = self.route_optimizer.dijkstra(bot_pos, pickup_pos)
            distance = len(path) - 1 if path else float('inf')
            

            cost = distance
            if bot.status == 'BUSY':
                cost += 2  
            
            if cost < min_cost:
                min_cost = cost
                best_bot = bot
        
        if best_bot:

            best_bot.current_orders += 1
            if best_bot.current_orders >= best_bot.max_capacity:
                best_bot.status = 'BUSY'
            else:
                best_bot.status = 'BUSY'  

            
            order.bot_id = best_bot.id
            order.status = 'ASSIGNED'
            order.estimated_distance = min_cost
            order.estimated_time = min_cost
            
            self.db.commit()
            print(f"Order {order.id} assigned to bot {best_bot.id} (distance: {min_cost})")
        
        return best_bot
    
    def get_bot_efficiency(self, bot: Bot) -> dict:

        total_orders = self.db.query(Order).filter(Order.bot_id == bot.id).count()
        delivered_orders = self.db.query(Order).filter(
            Order.bot_id == bot.id,
            Order.status == 'DELIVERED'
        ).count()
        
        current_orders = self.db.query(Order).filter(
            Order.bot_id == bot.id,
            Order.status.in_(['ASSIGNED', 'PICKED_UP'])
        ).all()
        
        total_distance = 0
        if current_orders:
            route = self.route_optimizer.optimize_delivery_route(bot, current_orders)
            total_distance = route['total_distance']
        
        return {
            "bot_id": bot.id,
            "total_orders": total_orders,
            "delivered_orders": delivered_orders,
            "current_load": f"{bot.current_orders}/{bot.max_capacity}",
            "current_route_distance": total_distance,
            "battery_level": bot.battery_level,
            "status": bot.status
        }
    
    def rebalance_orders(self) -> dict:
        """Redistribute orders among bots for better efficiency"""

        pending_orders = self.db.query(Order).filter(Order.status == 'PENDING').all()
        
        results = {
            "reassigned_orders": 0,
            "pending_orders": len(pending_orders),
            "assignments": []
        }
        
        for order in pending_orders:
            assigned_bot = self.assign_order_to_best_bot(order)
            if assigned_bot:
                results["reassigned_orders"] += 1
                results["assignments"].append({
                    "order_id": order.id,
                    "bot_id": assigned_bot.id,
                    "distance": order.estimated_distance
                })
        
        return results