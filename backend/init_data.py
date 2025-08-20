# init_data.py - Updated with blocked paths and restrictions
from sqlalchemy.orm import Session
from core.database import engine, SessionLocal, Base
from models.node import Node
from models.bot import Bot
from models.blocked_path import BlockedPath
from sqlalchemy import text

def init_complete_database():
    """Initialize complete database with all data including blocked paths"""
    # Create tables first
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("🚀 Initializing EagRoute database with enhanced restrictions...")
        
        # Clear existing data
        db.execute(text("""
        TRUNCATE TABLE blocked_paths, orders, bots, nodes
        RESTART IDENTITY CASCADE
        """))
        db.commit()
        
        # Create all 81 nodes in 9x9 grid
        print("📍 Creating 9x9 grid nodes...")
        for y in range(9):
            for x in range(9):
                node = Node(
                    x=x,
                    y=y,
                    node_type='NODE',
                    name=f"Node_{x}_{y}"
                )
                db.add(node)
        
        db.commit()
        print("✅ Grid nodes created")
        
        # Create delivery points (houses) - RESTRICTED FOR TRANSIT
        delivery_points = [
            {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 5, "y": 0},
            {"x": 8, "y": 1}, {"x": 0, "y": 2}, {"x": 7, "y": 3},
            {"x": 3, "y": 4}
        ]
        
        print("🏠 Setting up delivery points (restricted for transit)...")
        for i, point in enumerate(delivery_points):
            node = db.query(Node).filter(
                Node.x == point["x"],
                Node.y == point["y"]
            ).first()
            if node:
                node.node_type = 'HOUSE'
                node.is_delivery_point = True
                node.name = f"House_{i+1}"
        
        db.commit()
        print(f"✅ {len(delivery_points)} delivery points created (restricted for transit)")
        
        # Create restaurants - RESTRICTED FOR TRANSIT
        restaurants = [
            {"x": 2, "y": 3, "type": "RAMEN", "name": "Ramen Ichiban"},
            {"x": 4, "y": 5, "type": "CURRY", "name": "Curry Palace"},
            {"x": 6, "y": 2, "type": "PIZZA", "name": "Pizza Corner"},
            {"x": 1, "y": 5, "type": "SUSHI", "name": "Sushi Zen"},
            {"x": 7, "y": 6, "type": "RAMEN", "name": "Ramen Dragon"},
        ]
        
        print("🏪 Setting up restaurants (restricted for transit)...")
        for restaurant in restaurants:
            node = db.query(Node).filter(
                Node.x == restaurant["x"],
                Node.y == restaurant["y"]
            ).first()
            if node:
                node.node_type = 'RESTAURANT'
                node.is_restaurant = True
                node.restaurant_type = restaurant["type"]
                node.name = restaurant["name"]
        
        db.commit()
        print(f"✅ {len(restaurants)} restaurants created (restricted for transit)")
        
        # Create bot stations - ALLOWED FOR TRANSIT
        bot_stations = [
            {"x": 4, "y": 4, "name": "Central Station"},
        ]
        
        print("🔌 Setting up bot stations (allowed for transit)...")
        for station in bot_stations:
            node = db.query(Node).filter(
                Node.x == station["x"],
                Node.y == station["y"]
            ).first()
            if node:
                node.node_type = 'BOT_STATION'
                node.is_bot_station = True
                node.name = station["name"]
        
        db.commit()
        print(f"✅ {len(bot_stations)} bot stations created (allowed for transit)")
        
        # Create 3 delivery bots
        bot_starting_positions = [
            {"name": "Bot-Alpha", "x": 4, "y": 4},
            {"name": "Bot-Beta", "x": 0, "y": 8},
            {"name": "Bot-Gamma", "x": 8, "y": 0},
        ]
        
        print("🤖 Creating delivery bots...")
        for bot_data in bot_starting_positions:
            bot = Bot(
                name=bot_data["name"],
                current_x=bot_data["x"],
                current_y=bot_data["y"],
                max_capacity=3,
                status='IDLE',
                battery_level=100
            )
            db.add(bot)
        
        db.commit()
        print(f"✅ {len(bot_starting_positions)} bots created")
        
        # Create blocked paths from your data
        blocked_paths_data = [
            {"from_id": 4, "to_id": 12},
            {"from_id": 6, "to_id": 14},
            {"from_id": 8, "to_id": 16},
            {"from_id": 9, "to_id": 17},
            {"from_id": 10, "to_id": 18},
            {"from_id": 17, "to_id": 18},
            {"from_id": 23, "to_id": 24},
            {"from_id": 26, "to_id": 27},
            {"from_id": 27, "to_id": 28},
            {"from_id": 35, "to_id": 36},
            {"from_id": 38, "to_id": 39},
            {"from_id": 43, "to_id": 44},
            {"from_id": 49, "to_id": 50},
            {"from_id": 50, "to_id": 51},
            {"from_id": 54, "to_id": 55},
            {"from_id": 55, "to_id": 56},
            {"from_id": 52, "to_id": 61},
            {"from_id": 54, "to_id": 63},
            {"from_id": 72, "to_id": 73},
        ]
        
        print("🚫 Setting up blocked paths...")
        for path in blocked_paths_data:
            blocked_path = BlockedPath(
                from_node_id=path["from_id"],
                to_node_id=path["to_id"]
            )
            db.add(blocked_path)
            
            # Convert to coordinates for display
            from_x = (path["from_id"] - 1) % 9
            from_y = (path["from_id"] - 1) // 9
            to_x = (path["to_id"] - 1) % 9
            to_y = (path["to_id"] - 1) // 9
            
            print(f"  🚫 ({from_x},{from_y}) ↔ ({to_x},{to_y}) [IDs: {path['from_id']} ↔ {path['to_id']}]")
        
        db.commit()
        print(f"✅ {len(blocked_paths_data)} blocked paths created")
        
        # Print summary
        total_nodes = db.query(Node).count()
        total_bots = db.query(Bot).count()
        total_restaurants = db.query(Node).filter(Node.is_restaurant == True).count()
        total_houses = db.query(Node).filter(Node.is_delivery_point == True).count()
        total_blocked = db.query(BlockedPath).count()
        
        print("\n" + "="*60)
        print("🎉 ENHANCED DATABASE INITIALIZATION COMPLETE!")
        print("="*60)
        print(f"✅ Total nodes: {total_nodes}")
        print(f"🏠 Houses (delivery points - restricted): {total_houses}")
        print(f"🏪 Restaurants (restricted for transit): {total_restaurants}")
        print(f"🔌 Bot stations (allowed for transit): {len(bot_stations)}")
        print(f"🤖 Delivery bots: {total_bots}")
        print(f"🚫 Blocked paths: {total_blocked}")
        print("="*60)
        print("🚀 System Features:")
        print("  ✅ Bots cannot transit through restaurants/houses")
        print("  ✅ Bots can enter restaurants for pickup")
        print("  ✅ Bots can enter houses for delivery")
        print("  ✅ Bot stations allow transit")
        print("  ✅ Blocked paths are enforced")
        print("  ✅ Multi-order optimization")
        print("  ✅ Automatic return to station")
        print("="*60)
        print("📍 Ready to test with Postman/Insomnia!")
        print("🌐 API running at: http://localhost:8000")
        print("📚 API docs at: http://localhost:8000/docs")
        
        # Test the routing system
        print("\n🧪 Testing routing system...")
        test_enhanced_routing(db)
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_enhanced_routing(db: Session):
    """Test the enhanced routing system"""
    try:
        from services.route_algorithm import RouteOptimizer
        
        route_optimizer = RouteOptimizer(db)
        
        print(f"🧪 Testing enhanced routing:")
        print(f"  📊 Loaded {len(route_optimizer.blocked_paths)} blocked path segments")
        print(f"  🏪 Restaurants (restricted): {len(route_optimizer.restricted_nodes['restaurants'])}")
        print(f"  🏠 Houses (restricted): {len(route_optimizer.restricted_nodes['houses'])}")
        print(f"  🔌 Bot stations (allowed): {len(route_optimizer.restricted_nodes['bot_stations'])}")
        
        # Test specific blocked paths
        test_blocked_cases = [
            ((0, 3), (1, 3)),  # ID 4->12: Should be blocked
            ((0, 5), (1, 5)),  # ID 6->14: Should be blocked
            ((0, 7), (1, 7)),  # ID 8->16: Should be blocked
            ((0, 0), (1, 0)),  # Should be allowed
        ]
        
        print("\n  🚫 Testing blocked paths:")
        for from_pos, to_pos in test_blocked_cases:
            is_blocked = route_optimizer.is_path_blocked(from_pos, to_pos)
            status = "🚫 BLOCKED" if is_blocked else "✅ ALLOWED"
            print(f"    {from_pos} → {to_pos}: {status}")
        
        # Test transit restrictions
        restaurant_pos = (2, 3)  # Ramen restaurant
        house_pos = (0, 0)       # House
        station_pos = (4, 4)     # Bot station
        
        print("\n  🚦 Testing transit restrictions:")
        print(f"    Transit through restaurant {restaurant_pos}: {'🚫 BLOCKED' if route_optimizer.is_node_restricted_for_transit(restaurant_pos, (8,8), (0,0)) else '✅ ALLOWED'}")
        print(f"    Transit through house {house_pos}: {'🚫 BLOCKED' if route_optimizer.is_node_restricted_for_transit(house_pos, (8,8), (1,1)) else '✅ ALLOWED'}")
        print(f"    Transit through station {station_pos}: {'🚫 BLOCKED' if route_optimizer.is_node_restricted_for_transit(station_pos, (8,8), (0,0)) else '✅ ALLOWED'}")
        
        # Test pathfinding scenarios
        print("\n  🗺️ Testing pathfinding scenarios:")
        test_routes = [
            ((4, 4), (6, 2), "Bot station to Pizza restaurant"),
            ((6, 2), (0, 0), "Pizza restaurant to House"),
            ((0, 8), (1, 5), "Bot station to Sushi restaurant"),
            ((0, 0), (8, 8), "Diagonal across map"),
        ]
        
        for start, end, description in test_routes:
            path = route_optimizer.dijkstra(start, end)
            if path:
                # Check path validity
                is_valid = route_optimizer.validate_path(path)
                transit_issues = []
                
                # Check for transit violations
                for i in range(1, len(path)-1):  # Skip start and end
                    pos = path[i]
                    if route_optimizer.is_node_restricted_for_transit(pos, end, start):
                        transit_issues.append(pos)
                
                status = "✅ VALID" if is_valid and not transit_issues else "⚠️ ISSUES"
                print(f"    {description}:")
                print(f"      Path: {len(path)-1} steps {status}")
                if transit_issues:
                    print(f"      Transit violations: {transit_issues}")
            else:
                print(f"    {description}: ❌ NO PATH FOUND")
        
        print("  ✅ Routing system test completed")
        
    except Exception as e:
        print(f"  ❌ Error testing routing: {e}")

def reset_database():
    """Reset database by dropping and recreating all tables"""
    from core.database import Base
    print("🔄 Resetting database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database reset complete")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    
    init_complete_database()