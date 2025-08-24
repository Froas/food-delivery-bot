# init_blocked_paths.py - Script to initialize blocked paths
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.blocked_path import BlockedPath
from services.route_algorithm import RouteOptimizer

def init_blocked_paths():

    db = SessionLocal()
    
    try:
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
        
        print(f" Initializing {len(blocked_paths_data)} blocked paths...")
        

        db.query(BlockedPath).delete()
        

        for path_data in blocked_paths_data:
            
            existing = db.query(BlockedPath).filter(
                BlockedPath.from_node_id == path_data["from_id"],
                BlockedPath.to_node_id == path_data["to_id"]
            ).first()
            
            if not existing:
                blocked_path = BlockedPath(
                    from_node_id=path_data["from_id"],
                    to_node_id=path_data["to_id"]
                )
                db.add(blocked_path)
                
                
                from_x = (path_data["from_id"] - 1) % 9
                from_y = (path_data["from_id"] - 1) // 9
                to_x = (path_data["to_id"] - 1) % 9
                to_y = (path_data["to_id"] - 1) // 9
                
                print(f" Added: ({from_x},{from_y}) ↔ ({to_x},{to_y}) [IDs: {path_data['from_id']} ↔ {path_data['to_id']}]")
        
        db.commit()
        
        # Verify what was added
        total_blocked = db.query(BlockedPath).count()
        print(f"Successfully initialized {total_blocked} blocked paths in database")
        
        # Show some examples of coordinate conversion
        print("\n Examples of ID to coordinate conversion:")
        for i in [4, 12, 27, 50, 73]:
            x = (i - 1) % 9
            y = (i - 1) // 9
            print(f"  ID {i} = ({x}, {y})")
        
    except Exception as e:
        print(f"Error initializing blocked paths: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_blocked_paths():


    
    db = SessionLocal()
    try:
        route_optimizer = RouteOptimizer(db)
        
        print(f"\n Testing blocked path system:")
        print(f"  Loaded {len(route_optimizer.blocked_paths)} blocked path segments")
        print(f"  Restaurants: {len(route_optimizer.restricted_nodes['restaurants'])}")
        print(f"  Houses: {len(route_optimizer.restricted_nodes['houses'])}")
        
        # Test a few specific blocked paths
        test_cases = [
            ((0, 3), (1, 3)), 
            ((0, 5), (1, 5)),  
            ((0, 0), (1, 0)),  
        ]
        
        for from_pos, to_pos in test_cases:
            is_blocked = route_optimizer.is_path_blocked(from_pos, to_pos)
            status = "BLOCKED" if is_blocked else "ALLOWED"
            print(f"  {from_pos} → {to_pos}: {status}")
        
        # Test pathfinding with restrictions
        print(f"\n Testing pathfinding:")
        test_routes = [
            ((0, 0), (8, 8)),  # Diagonal across map
            ((4, 4), (6, 2)),  # Bot station to pizza restaurant
            ((2, 3), (0, 0)),  # Ramen restaurant to house
        ]
        
        for start, end in test_routes:
            path = route_optimizer.dijkstra(start, end)
            if path:
                print(f"  {start} → {end}: Found path with {len(path)-1} steps")
                # Check if path avoids restaurants/houses for transit
                transit_violations = []
                for i in range(1, len(path)-1):  # Skip start and end
                    pos = path[i]
                    if route_optimizer.is_node_restricted_for_transit(pos, end, start):
                        transit_violations.append(pos)
                
                if transit_violations:
                    print(f"Transit violations: {transit_violations}")
                else:
                    print(f"Path respects transit restrictions")
            else:
                print(f"  {start} → {end}: No path found")
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing blocked paths system...")
    init_blocked_paths()
    test_blocked_paths()
    print("Blocked paths system ready!")