from sqlalchemy import Column, String, Text, ARRAY, Date, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100))
    target_audience = Column(Text)
    brand_voice = Column(String(100))
    platforms = Column(ARRAY(Text))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ContentPost(Base):
    __tablename__ = "content_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    business_profile_id = Column(UUID(as_uuid=True), ForeignKey("business_profiles.id", ondelete="CASCADE"))
    platform = Column(String(50), nullable=False)
    topic = Column(Text, nullable=False)
    caption = Column(Text, nullable=False)
    hashtags = Column(ARRAY(Text))
    call_to_action = Column(Text)
    scheduled_date = Column(Date)
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
