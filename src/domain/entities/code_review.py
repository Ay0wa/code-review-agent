from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Severity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class IssueType(Enum):
    SYNTAX = "syntax"
    STYLE = "style"
    SMELL = "smell"
    SECURITY = "security"


class Issue(BaseModel):
    description: str
    severity: Severity
    issue_type: IssueType
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


class Improvement(BaseModel):
    description: str
    category: str
    priority: int


class CodeReview(BaseModel):
    code: str
    context: str
    issues: List[Issue]
    improvements: List[Improvement]
    score: int
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)

    @property
    def critical_issues_count(self) -> int:
        return len([i for i in self.issues if i.severity == Severity.CRITICAL])

    @property
    def warning_issues_count(self) -> int:
        return len([i for i in self.issues if i.severity == Severity.WARNING])

    @property
    def has_critical_issues(self) -> bool:
        return self.critical_issues_count > 0
