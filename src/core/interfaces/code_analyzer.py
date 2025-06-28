from abc import ABC, abstractmethod
from typing import List

from domain.entities.code_review import Improvement, Issue


class ICodeAnalyzer(ABC):
    @abstractmethod
    def analyze_syntax(self, code: str) -> List[Issue]:
        pass

    @abstractmethod
    def check_style(self, code: str) -> List[Issue]:
        pass

    @abstractmethod
    def detect_smells(self, code: str) -> List[Issue]:
        pass

    @abstractmethod
    def suggest_improvements(self, code: str) -> List[Improvement]:
        pass
