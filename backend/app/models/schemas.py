"""
AI Desktop Assistant — Pydantic Schemas

Request/response models for the API layer.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    PLANNING = "planning"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    AGENT = "agent"


# ── Chat ─────────────────────────────────────────────


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = None


class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    task_id: Optional[str] = None
    requires_approval: bool = False


# ── Tasks ────────────────────────────────────────────


class TaskStepSchema(BaseModel):
    id: int
    step_number: int
    agent_name: str
    action: str
    description: str
    status: StepStatus
    output: Optional[str] = None
    duration_ms: Optional[int] = None
    screenshot_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TaskSchema(BaseModel):
    id: int
    user_input: str
    status: TaskStatus
    plan_summary: Optional[str] = None
    result: Optional[str] = None
    steps: List[TaskStepSchema] = []
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskApproval(BaseModel):
    approved: bool
    feedback: Optional[str] = None


# ── Workflows ────────────────────────────────────────


class WorkflowStep(BaseModel):
    action: str
    tool: str
    parameters: Dict = {}
    description: str = ""


class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    trigger_phrase: str = ""
    steps: List[WorkflowStep] = []


class WorkflowSchema(BaseModel):
    id: int
    name: str
    description: str
    trigger_phrase: str
    steps: List[WorkflowStep]
    run_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


# ── Voice ────────────────────────────────────────────


class TranscriptionResponse(BaseModel):
    text: str
    language: Optional[str] = None
    duration_seconds: Optional[float] = None


class SynthesisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    voice: str = "en-US-AriaNeural"


# ── Settings ─────────────────────────────────────────


class SettingUpdate(BaseModel):
    key: str
    value: str
    category: str = "general"


class SettingSchema(BaseModel):
    key: str
    value: str
    category: str

    class Config:
        from_attributes = True


# ── WebSocket Events ────────────────────────────────


class AgentEvent(BaseModel):
    event_type: str  # "step_start", "step_complete", "step_error", "task_complete", "screenshot"
    task_id: int
    step_number: Optional[int] = None
    agent_name: Optional[str] = None
    message: str = ""
    data: Dict = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
