import asyncio
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from models.bot import Bot
from models.order import Order
from models.node import Node
from services.route_algorithm import RouteOptimizer
from core.database import SessionLocal

class AutoMovementService:
    def __init__(self):
        self.is_running = False
        self.move_interval = 2.0  
        self.bot_routes: Dict[int, List[Tuple[int, int]]] = {} 
        self.bot_route_index: Dict[int, int] = {} 
        self.bot_returning_to_station: Dict[int, bool] = {} 
        self.bot_stations = []  
        self.bot_planned_routes: Dict[int, List[dict]] = {}  
        self.bot_completed_waypoints: Dict[int, set] = {}  
    
    async def start_auto_movement(self):
        # Start automatic bot movement system
        self.is_running = True
        self._load_bot_stations()
        print("Auto-movement system started!")
        print(f"Found {len(self.bot_stations)} bot stations")
        
        while self.is_running:
            try:
                await self._process_all_bots()
                await asyncio.sleep(self.move_interval)
            except Exception as e:
                print(f"Auto-movement error: {e}")
                import traceback
                traceback.print_exc()
                await asyncio.sleep(1)
    
    def stop_auto_movement(self):
        # Stop automatic bot movement
        self.is_running = False
        self.bot_routes.clear()
        self.bot_route_index.clear()
        self.bot_returning_to_station.clear()
        self.bot_planned_routes.clear()
        self.bot_completed_waypoints.clear()
        print("Auto-movement system stopped!")
    
    def _load_bot_stations(self):
        # Load all bot stations from database
        db = SessionLocal()
        try:
            stations = db.query(Node).filter(Node.is_bot_station == True).all()
            self.bot_stations = [(station.x, station.y, station.name) for station in stations]
            print(f"Loaded bot stations: {[(s[0], s[1]) for s in self.bot_stations]}")
        finally:
            db.close()
    
    def _find_nearest_station(self, bot_position: Tuple[int, int], db: Session) -> Optional[Tuple[int, int]]:
        # Find the nearest bot station to the given position
        if not self.bot_stations:
            return None
        
        route_optimizer = RouteOptimizer(db)
        nearest_station = None
        min_distance = float('inf')
        
        for station_x, station_y, station_name in self.bot_stations:
            station_pos = (station_x, station_y)
            path = route_optimizer.dijkstra(bot_position, station_pos)
            distance = len(path) - 1 if path else float('inf')
            
            if distance < min_distance:
                min_distance = distance
                nearest_station = station_pos
        
        return nearest_station
    
    def _plan_multi_order_route(self, bot: Bot, orders: List[Order], db: Session) -> List[dict]:
        # Plan optimal route for multiple orders using pickup-first strategy
        if not orders:
            return []
        
        route_optimizer = RouteOptimizer(db)
        current_pos = (bot.current_x, bot.current_y)
        planned_waypoints = []
        
        # Separate orders by status
        pickup_orders = [o for o in orders if o.status == 'ASSIGNED']
        delivery_orders = [o for o in orders if o.status == 'PICKED_UP']
        
        print(f"Bot {bot.id} planning route: {len(pickup_orders)} pickups, {len(delivery_orders)} deliveries")
        
        # Get completed waypoints for this bot
        completed = self.bot_completed_waypoints.get(bot.id, set())
        print(f"Bot {bot.id} completed waypoints: {completed}")
        
        # First Phase: Add all remaining pickups
        remaining_pickups = pickup_orders.copy()
        while remaining_pickups:
            nearest_order = None
            min_distance = float('inf')
            
            for order in remaining_pickups:
                pickup_pos = (order.pickup_x, order.pickup_y)
                waypoint_key = f"pickup_{order.id}_{pickup_pos[0]}_{pickup_pos[1]}"
                
                # Skip if already completed
                if waypoint_key in completed:
                    print(f"Skipping completed pickup: {waypoint_key}")
                    continue
                
                path = route_optimizer.dijkstra(current_pos, pickup_pos)
                distance = len(path) - 1 if path else float('inf')
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_order = order
            
            if nearest_order:
                pickup_pos = (nearest_order.pickup_x, nearest_order.pickup_y)
                waypoint_key = f"pickup_{nearest_order.id}_{pickup_pos[0]}_{pickup_pos[1]}"
                
                # Only add if not completed
                if waypoint_key not in completed:
                    planned_waypoints.append({
                        'position': pickup_pos,
                        'type': 'pickup',
                        'order_id': nearest_order.id,
                        'restaurant_type': nearest_order.restaurant_type,
                        'customer_name': nearest_order.customer_name,
                        'waypoint_key': waypoint_key
                    })
                    current_pos = pickup_pos
                    print(f" Added pickup waypoint: {waypoint_key}")
                
                remaining_pickups.remove(nearest_order)
            else:
                break  # No more valid pickups
        
        # Second Phase: Add all deliveries
        all_delivery_orders = delivery_orders + pickup_orders  
        remaining_deliveries = all_delivery_orders.copy()
        
        while remaining_deliveries:
            nearest_order = None
            min_distance = float('inf')
            
            for order in remaining_deliveries:
                delivery_pos = (order.delivery_x, order.delivery_y)
                waypoint_key = f"delivery_{order.id}_{delivery_pos[0]}_{delivery_pos[1]}"
                
                # Skip if already completed
                if waypoint_key in completed:
                    print(f"Skipping completed delivery: {waypoint_key}")
                    continue
                
                # Check if pickup is completed for this order (CRITICAL FIX)
                pickup_key = f"pickup_{order.id}_{order.pickup_x}_{order.pickup_y}"
                
                # For ASSIGNED orders, pickup must be completed OR order status must be PICKED_UP
                if order.status == 'ASSIGNED' and pickup_key not in completed:
                    print(f"Skipping delivery {waypoint_key}, pickup {pickup_key} not completed yet")
                    continue  # Pickup not done yet
                
                path = route_optimizer.dijkstra(current_pos, delivery_pos)
                distance = len(path) - 1 if path else float('inf')
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_order = order
            
            if nearest_order:
                delivery_pos = (nearest_order.delivery_x, nearest_order.delivery_y)
                waypoint_key = f"delivery_{nearest_order.id}_{delivery_pos[0]}_{delivery_pos[1]}"
                
                # Only add if not completed
                if waypoint_key not in completed:
                    planned_waypoints.append({
                        'position': delivery_pos,
                        'type': 'delivery',
                        'order_id': nearest_order.id,
                        'customer_name': nearest_order.customer_name,
                        'waypoint_key': waypoint_key
                    })
                    current_pos = delivery_pos
                    print(f"Added delivery waypoint: {waypoint_key}")
                
                remaining_deliveries.remove(nearest_order)
            else:
                break  
        
        print(f"Bot {bot.id} final plan: {len(planned_waypoints)} waypoints")
        return planned_waypoints
    
    async def _process_all_bots(self):
        # Process movement for all active bots
        db = SessionLocal()
        try:
            # Get all bots (including idle ones that might need to return to station)
            all_bots = db.query(Bot).all()
            
            for bot in all_bots:
                await self._process_single_bot(bot, db)
            
            db.commit()
        finally:
            db.close()
    
    async def _process_single_bot(self, bot: Bot, db: Session):
        # Process movement for a single bot
        # Get bot's current orders
        orders = db.query(Order).filter(
            Order.bot_id == bot.id,
            Order.status.in_(['ASSIGNED', 'PICKED_UP'])
        ).order_by(Order.created_at).all()
        
        print(f"Processing Bot {bot.id} at ({bot.current_x},{bot.current_y}) - {len(orders)} orders")
        
        # If bot has orders, handle delivery tasks
        if orders:
            self.bot_returning_to_station[bot.id] = False
            await self._move_bot_with_multi_order_plan(bot, orders, db)
        else:
            # No orders - clear completed waypoints and check if bot needs to return to station
            self.bot_completed_waypoints[bot.id] = set()
            await self._handle_idle_bot(bot, db)
    
    async def _move_bot_with_multi_order_plan(self, bot: Bot, orders: List[Order], db: Session):
        # Move bot according to multi-order plan
        bot_id = bot.id
        
        # ALWAYS recalculate plan to ensure we have current state
        print(f"Bot {bot_id} recalculating multi-order plan")
        new_plan = self._plan_multi_order_route(bot, orders, db)
        self.bot_planned_routes[bot_id] = new_plan
        
        # Clear current route to force recalculation
        self._clear_bot_route(bot_id)
        
        if new_plan:
            print(f"🗺️ Bot {bot_id} multi-order plan:")
            for i, waypoint in enumerate(new_plan):
                completed = self.bot_completed_waypoints.get(bot_id, set())
                status = "OK" if waypoint['waypoint_key'] in completed else "⏳"
                print(f"   {i+1}. {status} {waypoint['type'].upper()} at {waypoint['position']} (Order #{waypoint['order_id']})")
        else:
            print(f"Failed Bot {bot_id} has no waypoints to plan")
            return
        
        # Get next destination from plan
        next_destination = self._get_next_destination_from_plan(bot, db)
        if not next_destination:
            print(f"Failed Bot {bot_id} has no more destinations")
            return
        
        print(f"Bot {bot_id} next destination: {next_destination}")
        
        # Calculate or get cached route to next destination
        route = await self._get_or_calculate_route(bot, next_destination, db, "multi_order")
        if not route or len(route) <= 1:
            print(f"Bot {bot_id} no valid route to {next_destination}")
            return
        
        # Move bot one step along the route
        await self._execute_next_move(bot, route, db)
    
    def _get_next_destination_from_plan(self, bot: Bot, db: Session) -> Optional[Tuple[int, int]]:
        # Get next destination from planned route 
        bot_id = bot.id
        
        if bot_id not in self.bot_planned_routes or not self.bot_planned_routes[bot_id]:
            print(f"Bot {bot_id} has no planned routes")
            return None
        
        current_pos = (bot.current_x, bot.current_y)
        completed = self.bot_completed_waypoints.get(bot_id, set())
        
        print(f"Bot {bot_id} searching next destination from {len(self.bot_planned_routes[bot_id])} waypoints")
        print(f"Bot {bot_id} completed waypoints: {completed}")
        
        # Find next unvisited waypoint
        for i, waypoint in enumerate(self.bot_planned_routes[bot_id]):
            waypoint_key = waypoint['waypoint_key']
            waypoint_pos = waypoint['position']
            
            print(f"Checking waypoint {i+1}: {waypoint_key} at {waypoint_pos}")
            
            # Skip if already completed
            if waypoint_key in completed:
                print(f" Skipping completed waypoint: {waypoint_key}")
                continue
            
            # For delivery waypoints, check if pickup is completed
            if waypoint['type'] == 'delivery':
                pickup_key = f"pickup_{waypoint['order_id']}_{waypoint_pos[0]}_{waypoint_pos[1]}"
                
                # Get the actual pickup coordinates from the order
                order = db.query(Order).filter(Order.id == waypoint['order_id']).first()
                if order:
                    # Use actual pickup coordinates from order
                    actual_pickup_key = f"pickup_{order.id}_{order.pickup_x}_{order.pickup_y}"
                    
                    # Check if pickup is completed OR order status is PICKED_UP
                    pickup_completed = (actual_pickup_key in completed) or (order.status == 'PICKED_UP')
                    
                    if not pickup_completed:
                        print(f"Skipping delivery {waypoint_key}, pickup {actual_pickup_key} not completed yet (order status: {order.status})")
                        continue  # Pickup not done yet
                    else:
                        print(f" Pickup completed for delivery {waypoint_key}")
            
            print(f"Next destination found: {waypoint_pos} (waypoint: {waypoint_key})")
            return waypoint_pos
        
        print(f" No valid next destination found for Bot {bot_id}")
        return None
    
    def _mark_waypoint_completed(self, bot: Bot, position: Tuple[int, int], waypoint_type: str, order_id: int):
        """Mark a waypoint as completed"""
        bot_id = bot.id
        waypoint_key = f"{waypoint_type}_{order_id}_{position[0]}_{position[1]}"
        
        if bot_id not in self.bot_completed_waypoints:
            self.bot_completed_waypoints[bot_id] = set()
        
        self.bot_completed_waypoints[bot_id].add(waypoint_key)
        print(f"ot {bot_id} completed waypoint: {waypoint_key}")
        
        # Clear the current route to force recalculation on next move
        self._clear_bot_route(bot_id)
        print(f"Bot {bot_id} cleared route cache after waypoint completion")
    
    async def _handle_idle_bot(self, bot: Bot, db: Session):
        """Handle bot that has no orders - return to nearest station"""
        current_pos = (bot.current_x, bot.current_y)
        
        # Check if bot is already at a station
        if self._is_at_bot_station(current_pos):
            bot.status = 'IDLE'
            self.bot_returning_to_station[bot.id] = False
            self._clear_bot_route(bot.id)
            return
        
        # If not returning to station yet, start the return journey
        if not self.bot_returning_to_station.get(bot.id, False):
            nearest_station = self._find_nearest_station(current_pos, db)
            if nearest_station:
                self.bot_returning_to_station[bot.id] = True
                print(f"Bot {bot.id} starting return to station {nearest_station}")
        
        # Move towards station if returning
        if self.bot_returning_to_station.get(bot.id, False):
            nearest_station = self._find_nearest_station(current_pos, db)
            if nearest_station:
                route = await self._get_or_calculate_route(bot, nearest_station, db, "station")
                if route and len(route) > 1:
                    await self._execute_next_move(bot, route, db)
                    
                    # Check if reached station
                    if (bot.current_x, bot.current_y) == nearest_station:
                        print(f"Bot {bot.id} returned to station {nearest_station}")
                        bot.status = 'IDLE'
                        bot.battery_level = min(100, bot.battery_level + 10)
                        self.bot_returning_to_station[bot.id] = False
                        self._clear_bot_route(bot.id)
    
    def _is_at_bot_station(self, position: Tuple[int, int]) -> bool:
        """Check if position is at a bot station"""
        return any(position == (station[0], station[1]) for station in self.bot_stations)
    
    async def _get_or_calculate_route(self, bot: Bot, destination: Tuple[int, int], db: Session, route_type: str = "delivery") -> List[Tuple[int, int]]:
        """Get cached route or calculate new one"""
        bot_id = bot.id
        current_pos = (bot.current_x, bot.current_y)
        
        # Always recalculate if no route or route is invalid
        needs_new_route = (
            bot_id not in self.bot_routes or 
            not self.bot_routes[bot_id] or
            len(self.bot_routes[bot_id]) == 0 or
            self.bot_routes[bot_id][-1] != destination or
            self.bot_route_index.get(bot_id, 0) >= len(self.bot_routes[bot_id]) - 1 or
            (len(self.bot_routes[bot_id]) > 0 and 
            self.bot_route_index.get(bot_id, 0) < len(self.bot_routes[bot_id]) and
            self.bot_routes[bot_id][self.bot_route_index.get(bot_id, 0)] != current_pos)
        )
        
        if needs_new_route:
            # Calculate new route
            route_optimizer = RouteOptimizer(db)
            new_route = route_optimizer.dijkstra(current_pos, destination)
            
            if new_route:
                self.bot_routes[bot_id] = new_route
                self.bot_route_index[bot_id] = 0
                
                if route_type == "station":
                    print(f"Bot {bot_id} new route to station: {current_pos} → {destination} ({len(new_route)-1} steps)")
                else:
                    print(f"Bot {bot_id} new route to waypoint: {current_pos} → {destination} ({len(new_route)-1} steps)")
            else:
                print(f"No route found for Bot {bot_id} from {current_pos} to {destination}")
                return []
        
        return self.bot_routes.get(bot_id, [])
    
    async def _execute_next_move(self, bot: Bot, route: List[Tuple[int, int]], db: Session):
        """Move bot to next position in route"""
        bot_id = bot.id
        current_index = self.bot_route_index.get(bot_id, 0)
        
        # Check if at destination
        if current_index >= len(route) - 1:
            print(f"Bot {bot_id} reached destination!")
            await self._handle_destination_reached(bot, db)
            self._clear_bot_route(bot_id)
            return
        
        # Move to next step
        next_index = current_index + 1
        next_position = route[next_index]
        
        old_pos = (bot.current_x, bot.current_y)
        bot.current_x, bot.current_y = next_position[0], next_position[1]
        self.bot_route_index[bot_id] = next_index
        
        # Show current orders in movement log
        orders_info = f"({bot.current_orders} orders)"
        
        if self.bot_returning_to_station.get(bot_id, False):
            print(f"Bot {bot_id}: {old_pos} → ({bot.current_x},{bot.current_y}) [returning to station {next_index}/{len(route)-1}]")
        else:
            print(f"Bot {bot_id}: {old_pos} → ({bot.current_x},{bot.current_y}) [multi-order {next_index}/{len(route)-1}] {orders_info}")
        
        # Check if reached pickup/delivery location
        await self._check_location_events(bot, db)
    
    async def _handle_destination_reached(self, bot: Bot, db: Session):
        """Handle when bot reaches its destination"""
        current_pos = (bot.current_x, bot.current_y)
        
        print(f"Bot {bot.id} handling destination reached at {current_pos}")
        
        # Check if reached a bot station
        if self._is_at_bot_station(current_pos):
            if self.bot_returning_to_station.get(bot.id, False):
                print(f"Bot {bot.id} arrived at station {current_pos}")
                bot.status = 'IDLE'
                bot.battery_level = min(100, bot.battery_level + 20)
                self.bot_returning_to_station[bot.id] = False
                self._clear_planned_route(bot.id)
                return
        
        # Check orders at this location
        orders = db.query(Order).filter(
            Order.bot_id == bot.id,
            Order.status.in_(['ASSIGNED', 'PICKED_UP'])
        ).all()
        
        print(f"Bot {bot.id} checking {len(orders)} orders at {current_pos}")
        
        for order in orders:
            # Check if this is a pickup location
            if (order.status == 'ASSIGNED' and 
                current_pos == (order.pickup_x, order.pickup_y)):
                
                print(f"Bot {bot.id} executing pickup for order {order.id}")
                order.status = 'PICKED_UP'
                self._mark_waypoint_completed(bot, current_pos, "pickup", order.id)
                print(f"Bot {bot.id} picked up order {order.id} at {current_pos} [total: {bot.current_orders} orders]")
                break
            
            # Check if this is a delivery location
            elif (order.status == 'PICKED_UP' and 
                current_pos == (order.delivery_x, order.delivery_y)):
                
                print(f"Bot {bot.id} executing delivery for order {order.id}")
                order.status = 'DELIVERED'
                bot.current_orders -= 1
                bot.battery_level = max(1, bot.battery_level - 5)
                self._mark_waypoint_completed(bot, current_pos, "delivery", order.id)
                
                print(f"Bot {bot.id} delivered order {order.id} at {current_pos} [remaining: {bot.current_orders} orders]")
                
                # Check if all orders are completed
                remaining_orders = db.query(Order).filter(
                    Order.bot_id == bot.id,
                    Order.status.in_(['ASSIGNED', 'PICKED_UP'])
                ).count()
                
                if remaining_orders == 0:
                    bot.status = 'IDLE'
                    self._clear_planned_route(bot.id)
                    print(f"Bot {bot.id} completed all orders, will return to station")
                break
    
    async def _check_location_events(self, bot: Bot, db: Session):
        """Check if bot has reached any significant locations"""
        await self._handle_destination_reached(bot, db)
    
    def _clear_bot_route(self, bot_id: int):
        """Clear cached route for a bot"""
        if bot_id in self.bot_routes:
            del self.bot_routes[bot_id]
        if bot_id in self.bot_route_index:
            del self.bot_route_index[bot_id]
    
    def _clear_planned_route(self, bot_id: int):
        """Clear planned multi-order route for a bot"""
        if bot_id in self.bot_planned_routes:
            del self.bot_planned_routes[bot_id]
        if bot_id in self.bot_completed_waypoints:
            del self.bot_completed_waypoints[bot_id]
        self._clear_bot_route(bot_id)
    
    def get_bot_progress(self, bot_id: int) -> Dict:
        """Get bot's movement progress"""
        progress = {
            "bot_id": bot_id,
            "status": "idle",
            "returning_to_station": self.bot_returning_to_station.get(bot_id, False)
        }
        
        # Add planned route info
        if bot_id in self.bot_planned_routes:
            completed = self.bot_completed_waypoints.get(bot_id, set())
            waypoints_with_status = []
            
            for wp in self.bot_planned_routes[bot_id]:
                wp_copy = wp.copy()
                wp_copy['completed'] = wp['waypoint_key'] in completed
                waypoints_with_status.append(wp_copy)
            
            progress["planned_waypoints"] = waypoints_with_status
            progress["total_waypoints"] = len(self.bot_planned_routes[bot_id])
            progress["completed_waypoints"] = len(completed)
        
        # Add current route info
        if bot_id in self.bot_routes:
            route = self.bot_routes[bot_id]
            current_index = self.bot_route_index.get(bot_id, 0)
            
            progress.update({
                "status": "moving",
                "route": route,
                "current_step": current_index,
                "total_steps": len(route) - 1,
                "progress_percent": round((current_index / (len(route) - 1)) * 100, 1) if len(route) > 1 else 100,
                "current_position": route[current_index] if current_index < len(route) else None,
                "destination": route[-1] if route else None
            })
        
        return progress
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        db = SessionLocal()
        try:
            bots = db.query(Bot).all()
            
            status = {
                "total_bots": len(bots),
                "idle_bots": 0,
                "busy_bots": 0,
                "returning_to_station": 0,
                "at_stations": 0,
                "bot_details": []
            }
            
            for bot in bots:
                bot_pos = (bot.current_x, bot.current_y)
                at_station = self._is_at_bot_station(bot_pos)
                returning = self.bot_returning_to_station.get(bot.id, False)
                
                if bot.status == 'IDLE':
                    status["idle_bots"] += 1
                else:
                    status["busy_bots"] += 1
                
                if returning:
                    status["returning_to_station"] += 1
                
                if at_station:
                    status["at_stations"] += 1
                
                # Get planned route info
                planned_waypoints = self.bot_planned_routes.get(bot.id, [])
                completed_waypoints = len(self.bot_completed_waypoints.get(bot.id, set()))
                
                status["bot_details"].append({
                    "id": bot.id,
                    "name": bot.name,
                    "position": bot_pos,
                    "status": bot.status,
                    "current_orders": bot.current_orders,
                    "battery_level": bot.battery_level,
                    "at_station": at_station,
                    "returning_to_station": returning,
                    "planned_waypoints": len(planned_waypoints),
                    "completed_waypoints": completed_waypoints,
                    "waypoint_details": planned_waypoints
                })
            
            return status
        finally:
            db.close()


auto_movement = AutoMovementService()