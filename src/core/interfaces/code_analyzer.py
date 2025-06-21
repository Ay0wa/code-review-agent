from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.code_review import Improvement, Issue


class ICodeAnalyzer(ABC):

    @abstractmethod
    async def analyze_syntax(self, code: str) -> List[Issue]:
        pass

    @abstractmethod
    async def check_style(self, code: str) -> List[Issue]:
        pass

    @abstractmethod
    async def detect_smells(self, code: str) -> List[Issue]:
        pass

    @abstractmethod
    async def suggest_improvements(self, code: str) -> List[Improvement]:
        pass
