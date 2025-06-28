from abc import ABC, abstractmethod


class ITool(ABC):
    @abstractmethod
    def execute(self, code: str) -> str:
        raise NotImplementedError("Need to define method execute")
