from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.api.Database import init_db, get_db
from app.api.models import Issue
from app.api.schemas import IssueUpdate, IssueCreate, IssueResponse

# from app.storage import load_data,save_data
router = APIRouter(prefix="/api/issues" ,tags=["Issues"])


@router.on_event("startup")
def startup_event():
    init_db()

@router.post("/issues", status_code=status.HTTP_201_CREATED, response_model=IssueResponse)
def create_issue(issue: IssueCreate,db:Session = Depends(get_db)):
    db_issue = Issue(**issue.dict())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


@router.get("/issues", response_model=List[IssueResponse])
def get_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    issues = db.query(Issue).offset(skip).limit(limit).all()
    return issues


@router.put("/issues/{issue_uuid}", response_model=IssueResponse)
def update_issue(issue_uuid: str, issue_update: IssueUpdate, db: Session = Depends(get_db)):
    db_issue = db.query(Issue).filter(Issue.uuid == issue_uuid).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    # Update only provided fields
    update_data = issue_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_issue, field, value)

    db_issue.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_issue)
    return db_issue


# Delete issue
@router.delete("/issues/{issue_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_uuid: str, db: Session = Depends(get_db)):
    db_issue = db.query(Issue).filter(Issue.uuid == issue_uuid).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    db.delete(db_issue)
    db.commit()
    return None

@router.get("/issue/{issue_id}",status_code=status.HTTP_200_OK,response_model=IssueResponse)
def get_issue(issue_uuid: str, db: Session = Depends(get_db)):
    db_issue = db.query(Issue).filter(Issue.uuid == issue_uuid).first()
    if not db_issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    return db_issue

@router.get("/")
def health_check():
    return {"status": "healthy", "message": "Issue Tracker API is running"}

# @router.get("/",response_model=list[IssueOut])
# async def get_issues():
#     """Retrieve all issues"""
#     issues = load_data()
#     return issues
#
# @router.post("/",response_model=IssueOut,status_code=status.HTTP_201_CREATED)
# def create_issue(payload: IssueCreate):
#     """
#     Create a new issue
#     The issue is persisted to data/issues.json
#     """
#
#     issues = load_data()
#
#     issue = {
#         "id": str(uuid.uuid4()),
#         "title": payload.title,
#         "description": payload.description,
#         "priority": payload.priority,
#         "status": IssueStatus.open,
#     }
#
#     issues.append(issue)
#     save_data(issues)
#     return issue
#
#
# @router.get("/{issue_id}",response_model=IssueOut)
# def get_issue(issue_id: str):
#     """
#     Get single issue by ID
#     Raises 404 if issue not found
#     """
#
#     issues = load_data()
#
#     for issue in issues:
#        if issue["id"] == issue_id:
#            return issue
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Issue not found")
#
# @router.delete("/{issue_id}",response_model=IssueOut)
# def delete_issue(issue_id:str):
#     """
#     Get single issue by ID
#     """
#
#     issues = load_data()
#     for issue in issues:
#         if issue["id"] == issue_id:
#             issues.pop(issue_id)
#             save_data(issues)
#             return
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Issue not found")
#
# def update_issue(issue_id:str,payload: IssueUpdate):
#     """Update an existing issue by ID."""
#     issues = load_data()
#
#     for issue in issues:
#         if issue["id"] == issue_id:
#             if payload.title is not None:
#                 issue["title"] = payload.title
#             if payload.description is not None:
#                 issue["description"] = payload.description
#             if payload.priority is not None:
#                 issue["priority"] = payload.priority.value
#             if payload.status is not None:
#                 issue["status"] = payload.status.value
#             save_data(issues)
#             return issue
#
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="Issue not found"
#     )
