
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from middleware.internal_secret import InternalSecretMiddleware
from contextlib import asynccontextmanager
import socketio
from core.database import engine, create_tables
from api.v1 import orders, bots, routes, map, auto_pilot
from core.config import settings
import uvicorn
from services.auto_movement import auto_movement
import asyncio


if not auto_movement.is_running:
        asyncio.create_task(auto_movement.start_auto_movement())
        print("autopilot is running")
else:
    print("autopilot is already running")

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*"
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    create_tables()
    print("Database tables created")
    yield

    print("Application shutting down")

app = FastAPI(
    title="EagRoute API",
    description="Delivery Bot Route Optimization System",
    version="1.5.0",
    lifespan=lifespan
)
app.add_middleware(
    InternalSecretMiddleware
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# auto_pilot = AutoPilotService()

# # Add to main.py
# async def start_auto_pilot():
#     """Start auto-pilot as background task"""
#     asyncio.create_task(auto_pilot.start_auto_pilot())

app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
app.include_router(bots.router, prefix="/api/v1", tags=["bots"])
app.include_router(routes.router, prefix="/api/v1", tags=["routes"])
app.include_router(map.router, prefix="/api/v1", tags=["map"])
app.include_router(auto_pilot.router, prefix="/api/v1", tags=["auto_pilot"])


socket_app = socketio.ASGIApp(sio, app)

@app.get("/")
async def root():
    return {"message": "EagRoute API is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

@sio.event
async def subscribe_updates(sid):
    await sio.emit('subscribed', {'status': 'success'}, room=sid)

if __name__ == "__main__":
    
    uvicorn.run("main:socket_app", host="0.0.0.0", port=8000, reload=True)
