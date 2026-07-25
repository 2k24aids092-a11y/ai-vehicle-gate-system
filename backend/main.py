from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from config import CORS_ORIGINS, DEBUG, HOST, PORT, UPLOAD_FOLDER
from database import Base, engine
from app.routes import api_router
import os

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("\n" + "="*60)
    print("  AI SMART VEHICLE GATE ACCESS SYSTEM")
    print("  Backend Starting...")
    print("="*60)
    yield
    # Shutdown
    print("\n" + "="*60)
    print("  Backend Shutting Down...")
    print("="*60)

app = FastAPI(
    title="Vehicle Gate System API",
    description="AI-powered vehicle gate access management system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

# Include API routes
app.include_router(api_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Vehicle Gate System API"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "service": "AI Smart Vehicle Gate Access System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
