from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, ConfigDict

# Evidence Schemas
class EvidenceBase(BaseModel):
    evidence_type: str = "pr" # "pr", "commit", "branch", "ci_check"
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    reference_id: Optional[str] = None
    author_username: Optional[str] = None
    author_avatar: Optional[str] = None
    meta_json: Optional[str] = None

class EvidenceCreate(EvidenceBase):
    pass

class EvidenceResponse(EvidenceBase):
    id: int
    card_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Activity Log Schema
class ActivityLogResponse(BaseModel):
    id: int
    card_id: int
    action: str
    actor: str
    details: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Card Schemas
class CardBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "To Do" # "To Do", "In Progress", "Done"
    priority: str = "Medium"
    task_type: str = "feature"
    assignee_name: Optional[str] = None
    assignee_username: Optional[str] = None
    assignee_avatar: Optional[str] = None
    estimation_hours: Optional[float] = 2.0
    story_points: Optional[int] = 2
    diff_loc: Optional[int] = 0
    is_scope_creep: Optional[bool] = False
    scope_creep_ratio: Optional[float] = 1.0
    is_stale_pr: Optional[bool] = False
    days_inactive: Optional[float] = 0.0
    repo_name: Optional[str] = None
    branch_name: Optional[str] = None
    pr_number: Optional[int] = None
    pr_url: Optional[str] = None
    pr_state: Optional[str] = None
    origin: Optional[str] = "github_pr"

class CardCreate(CardBase):
    initial_evidence: Optional[EvidenceCreate] = None

class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    task_type: Optional[str] = None
    assignee_name: Optional[str] = None
    assignee_username: Optional[str] = None
    assignee_avatar: Optional[str] = None
    estimation_hours: Optional[float] = None
    story_points: Optional[int] = None
    diff_loc: Optional[int] = None
    is_scope_creep: Optional[bool] = None
    is_stale_pr: Optional[bool] = None
    pr_state: Optional[str] = None

class CardResponse(CardBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    evidences: List[EvidenceResponse] = []
    activities: List[ActivityLogResponse] = []
    model_config = ConfigDict(from_attributes=True)

# Board Schemas
class BoardColumn(BaseModel):
    id: str # "to_do", "in_progress", "done"
    title: str # "To Do", "In Progress", "Done"
    count: int
    cards: List[CardResponse]

class BoardResponse(BaseModel):
    total_cards: int
    columns: Dict[str, BoardColumn]
    stats: Dict[str, Any] # e.g. stale_count, scope_creep_count, active_devs

# Chat Schemas
class ChatRequest(BaseModel):
    message: str
    context_repo: Optional[str] = None

class ChatCardExtraction(BaseModel):
    title: str
    description: str
    assignee_name: Optional[str] = None
    task_type: str = "feature"
    priority: str = "Medium"
    estimation_hours: float = 2.0
    target_column: str = "To Do"
    matched_branch_or_pr: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    card_created: Optional[CardResponse] = None
    extracted_data: Optional[ChatCardExtraction] = None

# Demo Simulator Schemas
class DemoSimulatePRRequest(BaseModel):
    pr_number: int = 42
    title: str = "feat(auth): Add IBM Cloud SSO & OAuth2 session verification"
    description: str = "Implements SSO integration with IBM Cloud App ID, adds token refresh handling and unit tests."
    author_username: str = "firza-dev"
    author_name: str = "Firza Pratama"
    branch_name: str = "feat/ibm-sso-auth"
    repo_name: str = "ibm-bob/smart-tracker"
    additions: int = 185
    deletions: int = 24
    action: str = "opened" # "opened", "synchronize", "closed"
    merged: bool = False
