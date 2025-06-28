from abc import ABC, abstractmethod


class ILLMService(ABC):
    @abstractmethod
    def full_code_review_response(self, code: str) -> str:
        pass

    @abstractmethod
    def quick_check_response(self, code: str) -> str:
        pass

    @abstractmethod
    def explain_issue_response(self, code: str, issue: str) -> str:
        pass

    @abstractmethod
    def compare_versions_response(self, original: str, improved: str) -> str:
        pass
