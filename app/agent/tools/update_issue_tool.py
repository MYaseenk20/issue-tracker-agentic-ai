from typing import Optional, List, Dict, Any

from langchain_core.tools import tool

from app.api.schemas import IssuePriority, IssueStatus, IssueUpdate


@tool
def update_issue_tool(
        issue_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        root_cause_hint: Optional[str] = None,
        estimated_minutes: Optional[int] = None
) -> Dict[str, Any]:
    """
    Updates an existing issue by ID.

    Args:
        issue_id: The ID of the issue to update (required)
        title: New title (optional)
        description: New description (optional)
        priority: New priority: 'low' | 'medium' | 'high' (optional)
        status: New status: 'open' | 'in_progress' | 'closed' (optional)
        tags: New tags list (optional)
        root_cause_hint: New root cause hint (optional)
        estimated_minutes: New estimated minutes (optional)

    Returns:
        Dict with issue_id and updates to apply

    Examples:
        - "Update issue 5 priority to high"
        - "Change status of issue #12 from open to in_progress"
        - "Mark issue 7 as closed"
        - "Update issue 3 with tags bug and urgent"
    """

    updates = {}

    if title is not None:
        updates["title"] = title

    if description is not None:
        updates["description"] = description

    if priority is not None:
        updates["priority"] = IssuePriority(priority)

    if status is not None:
        updates["status"] = IssueStatus(status)

    if tags is not None:
        updates["tags"] = tags

    if root_cause_hint is not None:
        updates["root_cause_hint"] = root_cause_hint

    if estimated_minutes is not None:
        updates["estimated_minutes"] = estimated_minutes

    issue_update = IssueUpdate(**updates)

    return {
        "issue_id": issue_id,
        "updates": issue_update.model_dump(exclude_none=True)  # Only include non-None fields
    }