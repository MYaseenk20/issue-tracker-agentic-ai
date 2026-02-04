import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Issue(Base):
    __tablename__ = "issues"
    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String(50), nullable=False, default="medium")
    status = Column(String(50), nullable=False, default="open")
    tags = Column(JSON, nullable=False, default=list)
    root_cause_hint = Column(String, nullable=True)
    estimated_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Issue(uuid={self.uuid}, title={self.title}, status={self.status})>"
