from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.tasks import router as tasks_router
from routes.auth import router as auth_router
from src.api.chat import router as chat_router  # Chat API routes
from db import create_db_and_tables
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Todo Application API",
    description="API for managing user tasks in the Todo application",
    version="1.0.0"
)

# Add CORS middleware to allow frontend domain
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose authorization header to allow JWT token to be accessed by frontend
    expose_headers=["Access-Control-Allow-Origin", "Authorization"]
)

# Include task routes
app.include_router(tasks_router)

# Include auth routes
app.include_router(auth_router)

# Include chat routes
app.include_router(chat_router)

# Add health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.now()}

# Event handler to create tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Application API"}