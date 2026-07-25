import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from app.schemas import BusinessProfileCreate, BusinessProfileResponse
from app.ai_service import generate_social_post

app = FastAPI(title="AI Social Media Content Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GeneratePostRequest(BaseModel):
    company_name: str
    topic: str
    platform: str
    brand_voice: Optional[str] = "professional"

@app.get("/")
def read_root():
    return {"message": "AI Social Media Content Platform Backend Running"}

@app.post("/api/generate")
def generate_post(req: GeneratePostRequest):
    try:
        raw_result = generate_social_post(
            company_name=req.company_name,
            topic=req.topic,
            platform=req.platform,
            brand_voice=req.brand_voice
        )
        return json.loads(raw_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
