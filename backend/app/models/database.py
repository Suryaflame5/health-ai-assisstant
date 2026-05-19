"""
AI Desktop Assistant — SQLAlchemy ORM Models

Database table definitions for PostgreSQL.
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
    Float,
    func,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class Task(Base):
    """Tracks top-level agent tasks initiated by the user."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_input = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="pending")
    plan_json = Column(JSON, nullable=True)
    plan_summary = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    steps = relationship("TaskStep", back_populates="task", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="task", cascade="all, delete-orphan")
    action_logs = relationship("ActionLog", back_populates="task", cascade="all, delete-orphan")


class TaskStep(Base):
    """Individual execution steps within a task."""

    __tablename__ = "task_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    agent_name = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(Text, nullable=False, default="")
    status = Column(String(20), nullable=False, default="pending")
    output = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    screenshot_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    task = relationship("Task", back_populates="steps")


class Conversation(Base):
    """Chat message history linked to tasks."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    role = Column(String(20), nullable=False)  # user, assistant, system, agent
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())

    task = relationship("Task", back_populates="conversations")


class Workflow(Base):
    """Saved reusable automation workflows."""

    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    description = Column(Text, nullable=False, default="")
    trigger_phrase = Column(String(500), nullable=False, default="")
    steps_json = Column(JSON, nullable=False, default=list)
    run_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ActionLog(Base):
    """Audit trail of every desktop automation action performed."""

    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    action_type = Column(String(50), nullable=False)  # click, type, navigate, file_op, etc.
    tool_name = Column(String(100), nullable=False)
    target = Column(Text, nullable=True)
    parameters_json = Column(JSON, nullable=True)
    result = Column(Text, nullable=True)
    success = Column(Boolean, nullable=False, default=True)
    screenshot_path = Column(String(500), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    timestamp = Column(DateTime, server_default=func.now())

    task = relationship("Task", back_populates="action_logs")


class Setting(Base):
    """User-configurable settings stored in the database."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), nullable=False, unique=True)
    value = Column(Text, nullable=False, default="")
    category = Column(String(50), nullable=False, default="general")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
