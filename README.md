# EagRoute - Food Delivery Bot System
> **Coding Assignment Submission**

A sophisticated food delivery simulation platform featuring autonomous bots, intelligent routing algorithms, and real-time order management. Built with **FastAPI + React/TypeScript + PostgreSQl**** to demonstrate full-stack development capabilities.


## **Quick Demo**

**Start the application in 30 seconds:**

```bash
git clone <repository-url>
cd eagroute
cp .env.example .env
docker-compose up --build
```

**Then visit:**
- **Application**: http://localhost:5173 
- **API Docs**: http://localhost:8000/docs
- **Test API**: Import `api_test.json` into Postman


**Key Technical Decisions:**
- **FastAPI** for high-performance async API with automatic OpenAPI documentation
- **PostgreSQL** for enterprise-grade database with ACID compliance and advanced indexing
- **SQLAlchemy ORM** for database abstraction, relationship mapping, and query optimization
- **Pydantic** for comprehensive data validation and serialization
- **Socket.IO** for reliable real-time bidirectional communication with auto-reconnection
- **React + TypeScript** for type-safe frontend development

## **Core Features Demonstrated**

### 1. **Intelligent Route Optimization**
- Implemented **Dijkstra's algorithm** for shortest path finding
- Dynamic **blocked path handling** from CSV data
- Real-time **route recalculation** when paths change

### 2. **Autonomous Bot System**
- **Multi-bot coordination** with capacity management
- **Automatic order assignment** based on proximity and availability  
- **State management** for bot status (IDLE, BUSY, MAINTENANCE)

### 3. **Order Management System**
- **Complete order lifecycle**: PENDING → ASSIGNED → PICKED_UP → DELIVERED
- **Restaurant validation** with capacity limits
- **Background task processing** for order assignment

### 4. **Real-time Visualization**
- **Interactive 9x9 grid map** showing live system state
- **Socket.IO integration** for instant bidirectional updates with auto-reconnection
- **Event-driven architecture** for efficient real-time communication
- **Multi-layer display** (bots, orders, restaurants, delivery points)

##  Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          Docker                                        │ 
│                                                                        │
│   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│   │   Frontend      │    │    Backend      │    │   Database      │    │
│   │  (React/TS)     │◄──►│   (FastAPI)     │◄──►│  (SQLAlchemy)   │    │
│   │                 │    │                 │    │                 │    │
│   │ • Grid Map      │    │ • Bot Manager   │    │ • Bots          │    │
│   │ • Order Forms   │    │ • Route Algo    │    │ • Orders        │    │ 
│   │ • Real-time UI  │    │ • Auto Movement │    │ • Nodes         │    │
│   │                 │    │ • API Endpoints │    │ • Blocked Paths │    │
│   └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

```

## Project Structure

```
EagRoute/
├── backend/                    # FastAPI Backend
│   ├── api/v1/                # API Endpoints
│   │   ├── auto_pilot.py         # Auto-movement control
│   │   ├── bots.py               # Bot management
│   │   ├── map.py                # Map & grid operations  
│   │   ├── orders.py             # Order management
│   │   ├── routes.py             # Route optimization
│   │   └── websocket.py          # Real-time communication
│   ├── core/                  # Core Configuration
│   │   ├── config.py             # App settings
│   │   └── database.py           # Database connection
│   ├── models/                # SQLAlchemy Models
│   │   ├── bot.py                # Bot entity
│   │   ├── order.py              # Order entity
│   │   ├── node.py               # Map node entity
│   │   └── blocked_path.py       # Path restrictions
│   ├── schemas/               # Pydantic Schemas
│   │   ├── bot.py                # Bot validation
│   │   ├── order.py              # Order validation
│   │   └── node.py               # Node validation
│   ├── services/              # Business Logic
│   │   ├── auto_movement.py      # Movement automation
│   │   ├── bot_manager.py        # Bot coordination
│   │   └── route_algorithm.py    # Pathfinding algorithms
│   ├── init_data.py              # Database initialization
│   ├── init_blocked_paths.py     # Path setup
│   └── main.py                   # FastAPI application
│
├── frontend/                   # React Frontend
│   ├── src/                   
│   │   ├── components/        # UI Components
│   │   │   ├── GridMap.tsx       # Interactive map
│   │   │   ├── OrderForm.tsx     # Order creation
│   │   │   ├── OrderList.tsx     # Order tracking
│   │   │   └── SystemStats.tsx   # System monitoring
│   │   ├── hooks/             # Custom hooks
│   │   │   └── userApi.ts        # API integration
│   │   ├── services/          # API services
│   │   │   └── api.ts            # HTTP client
│   │   ├── types/             # TypeScript definitions
│   │   │   └── index.ts          # Type declarations
│   │   └── App.tsx               # Main application
│   └── package.json              # Dependencies
│
├─── 
│   ├── docker-compose.yml        # Multi-container setup
│   ├── .env.example             # Environment template
│   ├── BlockedPaths.csv         # Path restrictions data
│   └── sample_data.csv          # Initial sample data
└── README.md                    # This file
```

## **Testing & Validation**

### **Comprehensive API Testing**
- **60+ test cases** in Postman collection (`api_test.json`)
- **Error handling** validation (404, 400, validation errors)
- **Integration testing** for complete delivery workflows
- **Edge case testing** 

### **Test Categories**
```bash
   System Health 
   Bot Management 
   Order Lifecycle 
   Route Optimization 
   Auto-Movement System 
   Error Handling 
   Integration Scenarios 
```

### **Key Test Scenarios**
- Order creation with validation
- Bot movement and collision detection  
- Route optimization with blocked paths
- Restaurant capacity management
- Real-time status updates

## **Development Highlights**

### **Backend Excellence**
- **Async/await architecture** for handling thousands of concurrent requests
- **PostgreSQL integration** with connection pooling and transaction management  
- **Pydantic validation** with custom validators and automatic error responses
- **SQLAlchemy ORM** with lazy loading, eager loading, and relationship optimization
- **Dependency injection** with FastAPI's DI system for clean architecture
- **Background tasks** for non-blocking operations 
- **Comprehensive error handling** with proper HTTP status codes and detailed error messages

### **Frontend Sophistication** 
- **TypeScript** for type safety and better developer experience
- **Custom hooks** for API state management and Socket.IO integration
- **Real-time updates** via Socket.IO with automatic reconnection handling
- **Event-driven UI updates** for responsive user experience
- **Responsive design** with Tailwind CSS
- **Component reusability** with proper props interfaces


##  **Deployment Ready**

- **Docker containerization** for both frontend and backend
- **docker-compose** orchestration with proper networking
- **Environment configuration** via `.env` files
- **Production-ready** settings with CORS configuration


## **How to Evaluate**

### **1. Quick Start **
```bash
docker-compose up --build
# Visit http://localhost:5173
```

### **2. API Testing**
```bash
# Import api_test.json into Postman
# Run the complete test suite
```

### **3. Code Review Focus Areas**
- **Algorithm implementation** in `services/route_algorithm.py`
- **API design** in `api/v1/` directory
- **Database models** and relationships in `models/`
- **Real-time features** in `main.py` (Socket.IO integration)
- **Frontend architecture** in `src/components/`

### **4. Feature Demonstration**
1. Create multiple orders through the UI
2. Watch automatic bot assignment
3. Enable auto-movement to see bots navigate
4. Observe real-time updates across the interface
5. Test error scenarios (invalid locations, capacity limits)


## **Assignment Requirements Met**

 **Full-stack implementation** (FastAPI + React)  
 **Database design** with proper relationships  
 **API development** with comprehensive endpoints  
 **Algorithm implementation** (pathfinding, optimization)  
 **Real-time features** (WebSocket integration)  
 **Error handling** and validation  
 **Testing** with comprehensive test suite  
 **Documentation** with clear setup instructions  
 **Containerization** for easy deployment  

---

**Time Investment:** ~40 hours | **Test Coverage:** 60+ API tests

  **Project Status & IP Notice**

> This repository contains my personal implementation of a food-delivery simulation created for a coding assignment.

- Copyright © 2025 https://github.com/froas.
- Licensed under the MIT License
