# EagRoute - Food Delivery Bot System
> **Coding Assignment Submission**

A sophisticated food delivery simulation platform featuring autonomous bots, intelligent routing algorithms, and real-time order management. Built with **FastAPI + React/TypeScript + PostgreSQL** to demonstrate full-stack development capabilities.

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
- **Test API**: Import `api_test.json` into Postman or use Insomnia collection

## **Key Technical Decisions**
- **FastAPI** for high-performance async API with automatic OpenAPI documentation
- **PostgreSQL** for enterprise-grade database with ACID compliance and advanced indexing
- **SQLAlchemy ORM** for database abstraction, relationship mapping, and query optimization
- **Pydantic** for comprehensive data validation and serialization
- **Socket.IO** for reliable real-time bidirectional communication with auto-reconnection
- **React + TypeScript** for type-safe frontend development
- **Custom Security Middleware** for API authentication with internal secret validation

## **Core Features Demonstrated**

### 1. **Security & Authentication**
- **Internal Secret Middleware** for API endpoint protection
- **Request validation** with custom headers
- **Selective endpoint protection** 
- **Environment-based configuration** for security keys

### 2. **Intelligent Route Optimization**
- Implemented **Dijkstra's algorithm** for shortest path finding
- Dynamic **blocked path handling** from CSV data
- Real-time **route recalculation** when paths change

### 3. **Autonomous Bot System**
- **Multi-bot coordination** with capacity management
- **Automatic order assignment** based on proximity and availability  
- **State management** for bot status (IDLE, BUSY, MAINTENANCE)

### 4. **Order Management System**
- **Complete order lifecycle**: PENDING → ASSIGNED → PICKED_UP → DELIVERED
- **Restaurant validation** with capacity limits
- **Background task processing** for order assignment

### 5. **Real-time Visualization**
- **Interactive 9x9 grid map** showing live system state
- **Socket.IO integration** for instant bidirectional updates with auto-reconnection
- **Event-driven architecture** for efficient real-time communication
- **Multi-layer display** (bots, orders, restaurants, delivery points)

## Architecture

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
│   │ • Security      │    │ • API Endpoints │    │ • Blocked Paths │    │
│   │                 │    │ • Middleware    │    │                 │    │
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
│   ├── middleware/            # Custom Middleware
│   │   └── internal_secret.py    # API authentication middleware
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
│   │   │   └── api.ts            # HTTP client with auth
│   │   ├── types/             # TypeScript definitions
│   │   │   └── index.ts          # Type declarations
│   │   └── App.tsx               # Main application
│   └── package.json              # Dependencies
│
│
├──── docker-compose.yml        # Multi-container setup
├──── .env.example             # Environment template
├──── BlockedPaths.csv         # Path restrictions data
├──── sample_data.csv          # Initial sample data
└── README.md                    # This file
```

## **API Authentication**

All API endpoints (except `/docs` and `/health`) require authentication via the `x-internal-secret` header.

### **Required Header:**
```http
x-internal-secret: your-secret-key-from-env
```

### **Environment Setup:**
```env
# Backend
PASS_KEY=your-secret-key-here

# Frontend
VITE_INTERNAL_SECRET=your-secret-key-here
```

## **Testing & Validation**

### **API Testing with Postman**

1. **Import Collection:**
   ```bash
   # Import api_test.json into Postman
   ```

2. **Set Environment Variables:**
   ```json
   {
     "base_url": "http://localhost:8000",
     "internal_secret": "your-secret-key-from-env"
   }
   ```

3. **Configure Headers:**
   - Add to Collection/Folder level:
   ```http
   x-internal-secret: {{internal_secret}}
   ```

### **API Testing with Insomnia**

1. **Create New Request Collection**

2. **Base Environment Setup:**
   ```json
   {
     "base_url": "http://localhost:8000",
     "internal_secret": "VNMKLDSjfdjfafdfds-19rfdsdf9"
   }
   ```

3. **Required Headers for All Requests:**
   ```http
   Content-Type: application/json
   x-internal-secret: {{ _.internal_secret }}
   ```

4. **Sample Requests:**

   **GET All Bots:**
   ```http
   GET {{ _.base_url }}/api/v1/bots/
   x-internal-secret: {{ _.internal_secret }}
   ```

   **POST Create Order:**
   ```http
   POST {{ _.base_url }}/api/v1/orders/
   x-internal-secret: {{ _.internal_secret }}
   Content-Type: application/json

   {
     "restaurant_type": "pizza",
     "restaurant_name": "Mario's Pizza",
     "customer_name": "John Doe",
     "customer_phone": "+1234567890",
     "pickup_x": 2,
     "pickup_y": 2,
     "delivery_x": 7,
     "delivery_y": 7
   }
   ```

   **GET System Stats:**
   ```http
   GET {{ _.base_url }}/api/v1/map/stats
   x-internal-secret: {{ _.internal_secret }}
   ```

5. **Testing Endpoints:**

   | Category | Endpoint | Method | Description |
   |----------|----------|--------|-------------|
   | **Health** | `/health` | GET | No auth required |
   | **Bots** | `/api/v1/bots/` | GET | List all bots |
   | **Orders** | `/api/v1/orders/` | GET/POST | Order management |
   | **Map** | `/api/v1/map/grid` | GET | Get grid data |
   | **Routes** | `/api/v1/routes/optimize` | GET | Route optimization |

### **Comprehensive Testing Suite**
- **60+ test cases** covering all endpoints
- **Error handling** validation (401, 404, 400, validation errors)
- **Integration testing** for complete delivery workflows
- **Security testing** for authentication middleware
- **Edge case testing** for boundary conditions

### **Test Categories**
```bash
 System Health & Security
 Bot Management & Movement  
 Order Lifecycle Management
 Route Optimization & Pathfinding
 Auto-Movement System
 Error Handling & Validation
 Integration Scenarios
```

### **Key Test Scenarios**
- Authentication header validation
- Order creation with validation
- Bot movement and collision detection  
- Route optimization with blocked paths
- Restaurant capacity management
- Real-time status updates
- Middleware security enforcement

## **Development Highlights**

### **Security Implementation**
- **Custom middleware** for API authentication
- **Environment-based secrets** for production security
- **Selective endpoint protection** maintaining public health checks
- **CORS configuration** for cross-origin requests
- **Header validation** with proper error responses

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
- **Environment variable handling** with Vite for secure API communication
- **Custom hooks** for API state management and Socket.IO integration
- **Real-time updates** via Socket.IO with automatic reconnection handling
- **Event-driven UI updates** for responsive user experience
- **Responsive design** with Tailwind CSS
- **Component reusability** with proper props interfaces

## **Deployment Ready**

- **Docker containerization** for both frontend and backend
- **docker-compose** orchestration with proper networking
- **Environment configuration** via `.env` files
- **Production-ready** settings with CORS configuration
- **Security middleware** properly configured for production
- **Build arguments** for environment variables

## **How to Evaluate**

### **1. Quick Start**
```bash
docker-compose up --build
# Visit http://localhost:5173
```

### **2. API Testing Options**

**Option A: Postman**
```bash
# Import api_test.json into Postman
# Set environment variable: internal_secret = your-key
# Run the complete test suite
```

**Option B: Insomnia**
```bash
# Create new workspace
# Set base environment with internal_secret
# Import requests from documentation above
# Test all endpoints with authentication
```

### **3. Code Review Focus Areas**
- **Security middleware** in `middleware/internal_secret.py`
- **Algorithm implementation** in `services/route_algorithm.py`
- **API design** in `api/v1/` directory
- **Database models** and relationships in `models/`
- **Real-time features** in `main.py` (Socket.IO integration)
- **Frontend security** in `src/services/api.ts`

### **4. Feature Demonstration**
1. **Test authentication** - try requests with/without headers
2. **Create multiple orders** through the UI
3. **Watch automatic bot assignment** with proper authorization
4. **Enable auto-movement** to see bots navigate
5. **Observe real-time updates** across the interface
6. **Test security scenarios** (missing headers, invalid secrets)

## **Assignment Requirements Met**

 **Full-stack implementation** (FastAPI + React)  
 **Database design** with proper relationships  
 **API development** with comprehensive endpoints  
 **Security implementation** with authentication middleware  
 **Algorithm implementation** (pathfinding, optimization)  
 **Real-time features** (WebSocket integration)  
 **Error handling** and validation  
 **Testing** with comprehensive test suite (Postman + Insomnia)  
 **Documentation** with clear setup instructions  
 **Containerization** for easy deployment  

---

**Time Investment:** ~40 hours | **Test Coverage:** 60+ API tests | **Security:** Custom middleware authentication

## **Project Status & IP Notice**

> This repository contains my personal implementation of a food-delivery simulation created for a coding assignment.

- Copyright © 2025 https://github.com/froas.
- Licensed under the MIT License