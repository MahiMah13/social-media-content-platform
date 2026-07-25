from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.database.models import BusinessProfile, Base
from app.schemas import BusinessProfileCreate, BusinessProfileResponse

app = FastAPI(title="AI Social Media Content Platform API")

# Allow CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Social Media Content Platform Backend Running"}

# Dummy placeholder for current user ID until Auth middleware is wired up
DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000000"

@app.post("/api/business-profile", response_model=BusinessProfileResponse)
def create_business_profile(profile: BusinessProfileCreate):
    return {
        "id": "11111111-1111-1111-1111-111111111111",
        "user_id": DEFAULT_USER_ID,
        "company_name": profile.company_name,
        "industry": profile.industry,
        "target_audience": profile.target_audience,
        "brand_voice": profile.brand_voice,
        "platforms": profile.platforms,
        "created_at": "2026-07-25T10:00:00Z",
        "updated_at": "2026-07-25T10:00:00Z"
    }

@app.get("/api/business-profile", response_model=List[BusinessProfileResponse])
def get_business_profiles():
    return []
