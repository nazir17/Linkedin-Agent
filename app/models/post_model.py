from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.configs.database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), index=True)
    content = Column(Text)
    summary = Column(Text)
    source_urls = Column(Text)
    posted = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())