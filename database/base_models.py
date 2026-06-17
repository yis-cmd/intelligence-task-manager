from pydantic import BaseModel, Field
from enum import StrEnum


class AgentRank(StrEnum):
    JUNIOR = "Junior"
    SENIOR = "Senior"
    COMMANDER = "Commander"


class MissionStatus(StrEnum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AgentCreate(BaseModel):
    name: str
    specialty: str
    is_active: bool = True
    completed_missions: int = 0
    failed_missions: int = 0
    agent_rank: AgentRank


class Agent(AgentCreate):
    id: int


class AgentUpdate(BaseModel):
    name: str | None = None
    specialty: str | None = None
    is_active: bool | None = None
    completed_missions: int | None = Field(ge=0, default=None)
    failed_missions: int | None = Field(ge=0, default=None)
    agent_rank: AgentRank | None = None


class MissionCreate(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int = Field(ge=1, le=10)
    importance: int = Field(ge=1, le=10)
    status: MissionStatus = Field(default=MissionStatus.NEW)

class MissionRiskLevel(MissionCreate):
    risk_level: RiskLevel


class Mission(MissionCreate):
    id: int
    risk_level: RiskLevel
    assigned_agent_id: int | None = None


class MissionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    difficulty: int | None = Field(ge=1, le=10, default=None)
    importance: int | None = Field(ge=1, le=10, default=None)
    status: MissionStatus | None = None
    assigned_agent_id: int | None = None
