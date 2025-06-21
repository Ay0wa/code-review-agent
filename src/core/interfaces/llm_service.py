from abc import ABC, abstractmethod
from typing import Any, Dict

from src.domain.entities.code_review import CodeReview


class ILLMService(ABC):

    @abstractmethod
    async def review_code(self, code: str, context: str = "") -> CodeReview:
        pass

    @abstractmethod
    async def quick_check(self, code: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def explain_issue(self, code: str, issue: str) -> str:
        pass

    @abstractmethod
    async def compare_versions(self, original: str, improved: str) -> str:
        pass
