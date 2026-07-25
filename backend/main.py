from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Initialize database models
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Media Content Platform API",
    description="Backend API for AI-Powered Social Media Content Calendar",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Social Media Content Platform API is running!"}
