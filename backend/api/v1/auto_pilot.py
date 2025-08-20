from fastapi import APIRouter, Depends
from services.auto_movement import auto_movement
import asyncio
router = APIRouter()

@router.post("/auto-movement/start")
async def start_auto_movement():
    """Start automatic bot movement"""
    if not auto_movement.is_running:
        asyncio.create_task(auto_movement.start_auto_movement())
        return {"message": "Auto-movement started", "status": "running"}
    return {"message": "Auto-movement already running", "status": "running"}

@router.post("/auto-movement/stop")
async def stop_auto_movement():
    """Stop automatic bot movement"""
    auto_movement.stop_auto_movement()
    return {"message": "Auto-movement stopped", "status": "stopped"}

@router.get("/auto-movement/status")
async def get_auto_movement_status():
    """Get auto-movement system status"""
    return {
        "is_running": auto_movement.is_running,
        "move_interval": auto_movement.move_interval,
        "active_routes": len(auto_movement.bot_routes)
    }

@router.get("/auto-movement/bot/{bot_id}/progress")
async def get_bot_progress(bot_id: int):
    """Get specific bot's movement progress"""
    return auto_movement.get_bot_progress(bot_id)