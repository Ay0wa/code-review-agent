from pydantic import BaseModel

from src.domain.services.llm_service import LLMService


class ExplainIssueCommand(BaseModel):
    code: str
    issue_description: str


class ExplainIssueUseCase:
    def __init__(self, llm_service: LLMService):
        self._llm_service = llm_service

    def execute(self, command: ExplainIssueCommand) -> str:
        return self._llm_service.explain_issue(
            code=command.code, issue=command.issue_description
        )
