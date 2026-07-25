from fastapi import APIRouter
from .auth import router as auth_router
from .vehicles import router as vehicles_router
from .parking import router as parking_router
from .logs import router as logs_router
from .dashboard import router as dashboard_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(vehicles_router, prefix="/vehicles", tags=["Vehicles"])
api_router.include_router(parking_router, prefix="/parking", tags=["Parking"])
api_router.include_router(logs_router, prefix="/logs", tags=["Entry Logs"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
