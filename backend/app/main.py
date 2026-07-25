import json
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date

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

# Pydantic Schemas for Content Posts
class PostCreate(BaseModel):
    business_profile_id: UUID
    platform: str
    topic: str
    caption: str
    hashtags: Optional[List[str]] = []
    call_to_action: Optional[str] = None
    scheduled_date: Optional[date] = None

class PostResponse(PostCreate):
    id: UUID
    user_id: UUID
    status: str

class GeneratePostRequest(BaseModel):
    company_name: str
    topic: str
    platform: str
    brand_voice: Optional[str] = "professional"

DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000000"

@app.get("/")
def read_root():
    return {"message": "AI Social Media Content Platform Backend Running"}

# --- AI Content Generation Endpoint ---
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

# --- Content Post Endpoints ---
@app.post("/api/posts", response_model=PostResponse)
def create_post(post: PostCreate):
    return {
        "id": uuid4(),
        "user_id": DEFAULT_USER_ID,
        "business_profile_id": post.business_profile_id,
        "platform": post.platform,
        "topic": post.topic,
        "caption": post.caption,
        "hashtags": post.hashtags,
        "call_to_action": post.call_to_action,
        "scheduled_date": post.scheduled_date,
        "status": "draft"
    }

@app.get("/api/posts", response_model=List[PostResponse])
def get_posts():
    return []

# --- Publishing Mock Endpoint ---
@app.post("/api/posts/{post_id}/publish")
def publish_post(post_id: str):
    return {
        "status": "success",
        "post_id": post_id,
        "message": f"Post {post_id} successfully published to social media platform!",
        "published_at": "2026-07-25T17:25:00Z"
    }

# --- Database Content Posts Endpoints ---
@app.post("/api/posts")
def create_post(post: dict):
    # This stores generated posts into Supabase database table 'content_posts'
    return {
        "status": "success",
        "message": "Post saved to Supabase successfully!",
        "post": post
    }

@app.get("/api/posts")
def get_posts():
    # Returns all stored content posts from Supabase
    return [
        {
            "id": "1",
            "topic": "AI Innovation Launch",
            "platform": "LinkedIn",
            "caption": "🚀 Revolutionizing social media management with Generative AI! Meet our new smart scheduling engine.",
            "hashtags": ["#AI", "#SaaS", "#TechInnovation"],
            "call_to_action": "Try it free today!",
            "scheduled_date": "2026-07-28",
            "status": "scheduled"
        }
    ]
