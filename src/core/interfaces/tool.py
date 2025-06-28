from abc import ABC, abstractmethod
from typing import List

from domain.entities.code_review import Issue


class ITool(ABC):
    @abstractmethod
    def execute(self, code: str) -> str:
        raise NotImplementedError("Need to define method execute")
