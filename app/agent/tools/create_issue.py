from typing import Optional, List

from langchain_core.tools import tool
from sqlalchemy.orm import Session
from fastapi import Depends

from app.api.Database import get_db
from app.api.models import Issue
from app.api.schemas import IssueCreate, IssuePriority, IssueStatus


@tool
def create_issue_tool(title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    status: str = "open",
    tags: Optional[List[str]] = None,
    root_cause_hint: Optional[str] = None,
    estimated_minutes: Optional[int] = None):
    """
       Creates an issue (validated by IssueCreate).
       Returns JSON matching IssueCreate.
       """

    issue = IssueCreate(
        title=title,
        description=description,
        priority=IssuePriority(priority),
        status=IssueStatus(status),
        tags=tags or [],
        root_cause_hint=root_cause_hint,
        estimated_minutes=estimated_minutes
    )
    print(issue)
    return issue.model_dump()