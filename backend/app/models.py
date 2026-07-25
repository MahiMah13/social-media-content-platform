import uuid
from sqlalchemy import Column, String, Text, ARRAY, JSON, DateTime, ForeignKey, Date, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    target_audience = Column(Text)
    brand_voice = Column(String(100))
    business_goals = Column(Text)
    platforms = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ContentCalendar(Base):
    __tablename__ = "content_calendars"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posts = relationship("Post", back_populates="calendar", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calendar_id = Column(UUID(as_uuid=True), ForeignKey("content_calendars.id", ondelete="CASCADE"))
    platform = Column(String(50), nullable=False)
    post_date = Column(DateTime(timezone=True), nullable=False)
    caption = Column(Text)
    hashtags = Column(ARRAY(String))
    cta = Column(Text)
    image_prompt = Column(Text)
    status = Column(String(50), default="scheduled")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    calendar = relationship("ContentCalendar", back_populates="posts")

class AIHistory(Base):
    __tablename__ = "ai_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(JSON, nullable=False)
    model_used = Column(String(50), default="gemini-1.5-flash")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
