from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class CardModel(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="To Do", nullable=False, index=True) # "To Do", "In Progress", "Done"
    priority = Column(String(50), default="Medium", nullable=False) # "Low", "Medium", "High", "Critical"
    task_type = Column(String(50), default="feature", nullable=False) # "feature", "bugfix", "refactor", "chore", "docs"
    
    # Assignee details
    assignee_name = Column(String(100), nullable=True)
    assignee_username = Column(String(100), nullable=True)
    assignee_avatar = Column(String(255), nullable=True)

    # Estimations & Scope
    estimation_hours = Column(Float, default=2.0)
    story_points = Column(Integer, default=2)
    diff_loc = Column(Integer, default=0) # Lines of code changed (additions + deletions)
    is_scope_creep = Column(Boolean, default=False)
    scope_creep_ratio = Column(Float, default=1.0)

    # Stale tracking (Bonus #6)
    is_stale_pr = Column(Boolean, default=False)
    days_inactive = Column(Float, default=0.0)

    # Primary GitHub correlation
    repo_name = Column(String(255), nullable=True)
    branch_name = Column(String(255), nullable=True)
    pr_number = Column(Integer, nullable=True, index=True)
    pr_url = Column(String(500), nullable=True)
    pr_state = Column(String(50), nullable=True) # "open", "merged", "closed"

    # Card origin
    origin = Column(String(50), default="github_pr") # "github_pr", "github_branch", "chat", "manual", "doc_spec"

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    evidences = relationship("EvidenceModel", back_populates="card", cascade="all, delete-orphan", order_by="desc(EvidenceModel.created_at)")
    activities = relationship("ActivityLogModel", back_populates="card", cascade="all, delete-orphan", order_by="desc(ActivityLogModel.created_at)")


class EvidenceModel(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_type = Column(String(50), nullable=False) # "pr", "commit", "branch", "ci_check", "manual_note"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)
    reference_id = Column(String(100), nullable=True) # PR number or commit hash SHA
    author_username = Column(String(100), nullable=True)
    author_avatar = Column(String(255), nullable=True)
    meta_json = Column(Text, nullable=True) # extra JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    card = relationship("CardModel", back_populates="evidences")


class ActivityLogModel(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String(100), nullable=False) # "created", "status_changed", "evidence_attached", "pr_merged", "alarm_raised"
    actor = Column(String(100), default="system")
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    card = relationship("CardModel", back_populates="activities")
