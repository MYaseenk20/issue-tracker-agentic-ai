from datetime import datetime
from enum import Enum
from pydantic import BaseModel,Field
from typing import Optional, List


class IssuePriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class IssueStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"



class IssueBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: IssuePriority = IssuePriority.medium
    status: IssueStatus = IssueStatus.open
    tags: List[str] = Field(default_factory=list)
    root_cause_hint: Optional[str] = None
    estimated_minutes: Optional[int] = Field(None, ge=0)

class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[IssuePriority] = None
    status: Optional[IssueStatus] = None
    tags: Optional[List[str]]  = None
    root_cause_hint: Optional[str] = None
    estimated_minutes: Optional[int] = Field(None, ge=0)


class IssueResponse(IssueBase):
    uuid: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # F

# class IssueCreate(BaseModel):
#     title : str = Field(min_length=1,max_length=100)
#     description: str = Field(min_length=5, max_length=2000)
#     priority: IssuePriority = IssuePriority.medium
#
# class IssueUpdate(BaseModel):
#     title: Optional[str] = Field(default=None, max_length=100)
#     description: Optional[str] = Field(
#         default=None, min_length=5, max_length=2000)
#     priority: Optional[IssuePriority] = None
#     status: Optional[IssueStatus] = None
#
# class IssueOut(BaseModel):
#     id: str
#     title: str
#     description: str
#     priority: IssuePriority
#     status: IssueStatus

