from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class BusinessProfileBase(BaseModel):
    company_name: str
    industry: Optional[str] = None
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None
    platforms: Optional[List[str]] = []

class BusinessProfileCreate(BusinessProfileBase):
    pass

class BusinessProfileResponse(BusinessProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
