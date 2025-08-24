# services/route_algorithm.py - Enhanced with restrictions
import heapq
from typing import List, Dict, Tuple, Optional, Set
from sqlalchemy.orm import Session
from models.node import Node
from models.order import Order
from models.bot import Bot
from models.blocked_path import BlockedPath
from core.config import settings

class RouteOptimizer:
    def __init__(self, db: Session):
        self.db = db
        self.grid_size = settings.grid_size
        self.blocked_paths = self._load_blocked_paths()
        self.restricted_nodes = self._load_restricted_nodes()
    
    def _load_blocked_paths(self) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
        blocked_paths = set()
        
        # Get blocked paths from database
        db_blocked_paths = self.db.query(BlockedPath).all()
        print(f"Loading {len(db_blocked_paths)} blocked paths from database")
        
        for blocked in db_blocked_paths:
            # Convert node IDs to coordinates using the grid formula
            # ID = y * grid_size + x + 1, so: x = (ID - 1) % grid_size, y = (ID - 1) // grid_size
            from_id = blocked.from_node_id
            to_id = blocked.to_node_id
            
            from_x = (from_id - 1) % self.grid_size
            from_y = (from_id - 1) // self.grid_size
            to_x = (to_id - 1) % self.grid_size  
            to_y = (to_id - 1) // self.grid_size
            
            from_pos = (from_x, from_y)
            to_pos = (to_x, to_y)
            
            # Add both directions as blocked
            blocked_paths.add((from_pos, to_pos))
            blocked_paths.add((to_pos, from_pos))
            
            print(f"Blocked path: {from_pos} ↔ {to_pos} (IDs: {from_id} ↔ {to_id})")
        
        return blocked_paths
    
    def _load_restricted_nodes(self) -> Dict[str, Set[Tuple[int, int]]]:
        restricted = {
            'restaurants': set(),
            'houses': set(),
            'bot_stations': set()
        }
        
        # Get all special nodes
        restaurants = self.db.query(Node).filter(Node.is_restaurant == True).all()
        houses = self.db.query(Node).filter(Node.is_delivery_point == True).all()
        bot_stations = self.db.query(Node).filter(Node.is_bot_station == True).all()
        
        for restaurant in restaurants:
            restricted['restaurants'].add((restaurant.x, restaurant.y))
        
        for house in houses:
            restricted['houses'].add((house.x, house.y))
            
        for station in bot_stations:
            restricted['bot_stations'].add((station.x, station.y))
        
        print(f"Loaded {len(restricted['restaurants'])} restaurants as restricted transit")
        print(f"Loaded {len(restricted['houses'])} houses as restricted transit")
        print(f"Loaded {len(restricted['bot_stations'])} bot stations")
        
        return restricted
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                neighbors.append((nx, ny))
        
        return neighbors
    
    def is_path_blocked(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        
        return (from_pos, to_pos) in self.blocked_paths
    
    def is_node_restricted_for_transit(self, position: Tuple[int, int], destination: Tuple[int, int], 
                                    start: Tuple[int, int]) -> bool:
        
        # Allow start and destination positions always
        if position == destination or position == start:
            return False
        
        # Check if position is a restaurant or house (restricted for transit)
        if (position in self.restricted_nodes['restaurants'] or 
            position in self.restricted_nodes['houses']):
            return True
        
        # Bot stations are allowed for transit
        return False
    
    def dijkstra(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:

        if start == end:
            return [start]
        
        distances = {start: 0}
        previous = {}
        pq = [(0, start)]
        visited = set()
        
        print(f"Finding path: {start} → {end}")
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == end:
                # Reconstruct path
                path = []
                while current in previous:
                    path.append(current)
                    current = previous[current]
                path.append(start)
                result_path = path[::-1]
                print(f"Path found: {len(result_path)-1} steps")
                return result_path
            
            for neighbor in self.get_neighbors(current[0], current[1]):
                if neighbor in visited:
                    continue
                
                # Check if path is blocked
                if self.is_path_blocked(current, neighbor):
                    continue
                
                # Check if neighbor is restricted for transit
                if self.is_node_restricted_for_transit(neighbor, end, start):
                    continue
                
                distance = current_dist + 1 
                
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current
                    heapq.heappush(pq, (distance, neighbor))
        
        print(f"No path found from {start} to {end}")
        return []  
    
    def calculate_total_distance(self, points: List[Tuple[int, int]]) -> int:
        # Calculate total distance for a sequence of points
        if len(points) < 2:
            return 0
        
        total = 0
        for i in range(len(points) - 1):
            path = self.dijkstra(points[i], points[i + 1])
            if not path:
                return float('inf')  
            total += len(path) - 1
        
        return total
    
    def optimize_delivery_route(self, bot: Bot, orders: List[Order]) -> Dict:
        # Optimize route for multiple pickups and deliveries 
        if not orders:
            return {
                "route_points": [],
                "total_distance": 0,
                "estimated_time": 0,
                "detailed_path": []
            }
        
        # Start from bot current position
        current_pos = (bot.current_x, bot.current_y)
        route_points = [{"x": current_pos[0], "y": current_pos[1], "type": "start", "order_id": None}]
        

        # FIFO
        detailed_path = [current_pos]
        total_distance = 0
        
        for order in orders:
            pickup_pos = (order.pickup_x, order.pickup_y)
            delivery_pos = (order.delivery_x, order.delivery_y)
            
            # Go to pickup if not picked up yet
            if order.status == 'ASSIGNED':
                path_to_pickup = self.dijkstra(current_pos, pickup_pos)
                if path_to_pickup:
                    # Add intermediate points to detailed path
                    detailed_path.extend(path_to_pickup[1:])
                    total_distance += len(path_to_pickup) - 1
                    current_pos = pickup_pos
                    
                    route_points.append({
                        "x": pickup_pos[0],
                        "y": pickup_pos[1],
                        "type": "pickup",
                        "order_id": order.id,
                        "restaurant_type": order.restaurant_type
                    })
                else:
                    print(f"No path to pickup {pickup_pos} for order {order.id}")
            
            # Go to delivery
            path_to_delivery = self.dijkstra(current_pos, delivery_pos)
            if path_to_delivery:
                detailed_path.extend(path_to_delivery[1:])
                total_distance += len(path_to_delivery) - 1
                current_pos = delivery_pos
                
                route_points.append({
                    "x": delivery_pos[0],
                    "y": delivery_pos[1],
                    "type": "delivery",
                    "order_id": order.id,
                    "customer_name": order.customer_name
                })
            else:
                print(f"No path to delivery {delivery_pos} for order {order.id}")
        
        return {
            "route_points": route_points,
            "total_distance": total_distance,
            "estimated_time": total_distance,  
            "detailed_path": detailed_path
        }
    
    def find_nearest_restaurant(self, position: Tuple[int, int], restaurant_type: str) -> Optional[Tuple[int, int]]:
        
        restaurants = self.db.query(Node).filter(
            Node.is_restaurant == True,
            Node.restaurant_type == restaurant_type.upper()
        ).all()
        
        if not restaurants:
            return None
        
        nearest = None
        min_distance = float('inf')
        
        for restaurant in restaurants:
            restaurant_pos = (restaurant.x, restaurant.y)
            path = self.dijkstra(position, restaurant_pos)
            distance = len(path) - 1 if path else float('inf')
            
            if distance < min_distance:
                min_distance = distance
                nearest = restaurant_pos
        
        return nearest
    
    def validate_path(self, path: List[Tuple[int, int]]) -> bool:
        
        if len(path) < 2:
            return True
        
        for i in range(len(path) - 1):
            current = path[i]
            next_pos = path[i + 1]
            
            # Check if path segment is blocked
            if self.is_path_blocked(current, next_pos):
                print(f"Path validation failed: blocked segment {current} → {next_pos}")
                return False
            

            if i > 0 and i < len(path) - 1:  
                if self.is_node_restricted_for_transit(current, path[-1], path[0]):
                    print(f"Path validation failed: transit through restricted node {current}")
                    return False
        
        return True
    
    def get_alternative_routes(self, start: Tuple[int, int], end: Tuple[int, int], 
        count: int = 3) -> List[List[Tuple[int, int]]]:


        main_route = self.dijkstra(start, end)
        if main_route:
            return [main_route]
        return []